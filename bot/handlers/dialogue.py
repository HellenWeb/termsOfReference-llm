import re
from pathlib import Path
from tempfile import TemporaryDirectory
import logging
from aiogram import Router, F
from bot.config import get_settings
from bot.services.llm import OpenAICompatibleLLMService
from bot.services.tz_generator import TZGenerator
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from docx import Document
from fpdf import FPDF
from bot.states.dialogue import DialogueStates


router = Router(name=__name__)
logger = logging.getLogger(__name__)
_FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
_INLINE_PATTERN = re.compile(
    r"\*\*(.+?)\*\*|__(.+?)__|\*(.+?)\*|_(.+?)_"
)


def _parse_inline_markdown(text: str) -> list[tuple[str, bool, bool]]:
    """Возвращает список (фрагмент_текста, bold, italic) для строки с инлайн-markdown."""
    runs: list[tuple[str, bool, bool]] = []
    pos = 0
    for match in _INLINE_PATTERN.finditer(text):
        if match.start() > pos:
            runs.append((text[pos:match.start()], False, False))
        bold_double, bold_underscore, italic_star, italic_underscore = match.groups()
        if bold_double is not None:
            runs.append((bold_double, True, False))
        elif bold_underscore is not None:
            runs.append((bold_underscore, True, False))
        elif italic_star is not None:
            runs.append((italic_star, False, True))
        else:
            runs.append((italic_underscore, False, True))
        pos = match.end()
    if pos < len(text):
        runs.append((text[pos:], False, False))
    return runs


def _strip_list_prefix(line: str) -> tuple[str, bool]:
    """Убирает маркер списка ("- "/"* ") и сообщает, был ли он найден."""
    if line.startswith("- ") or line.startswith("* "):
        return line[2:], True
    return line, False


def _render_docx_line(doc: Document, line: str) -> None:
    text, is_list_item = _strip_list_prefix(line)
    paragraph = doc.add_paragraph(style="List Bullet" if is_list_item else None)
    for run_text, bold, italic in _parse_inline_markdown(text):
        run = paragraph.add_run(run_text)
        run.bold = bold
        run.italic = italic


def _save_as_docx(tz_text: str, docx_path: Path) -> None:
    doc = Document()
    doc.add_heading("Техническое задание", level=0)
    for line in tz_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("### "):
            doc.add_heading(line[4:], level=3)
        elif line.startswith("## "):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("# "):
            doc.add_heading(line[2:], level=1)
        else:
            _render_docx_line(doc, line)
    doc.save(docx_path)


def _register_pdf_fonts(pdf: FPDF) -> None:
    pdf.add_font("Unicode", "", str(_FONTS_DIR / "DejaVuSans.ttf"))
    pdf.add_font("Unicode", "B", str(_FONTS_DIR / "DejaVuSans-Bold.ttf"))
    pdf.add_font("Unicode", "I", str(_FONTS_DIR / "DejaVuSans-Oblique.ttf"))
    pdf.add_font("Unicode", "BI", str(_FONTS_DIR / "DejaVuSans-BoldOblique.ttf"))


def _render_pdf_line(pdf: FPDF, line: str, *, h: float) -> None:
    text, is_list_item = _strip_list_prefix(line)
    if is_list_item:
        text = f"• {text}"
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=pdf.epw, h=h, text=text, markdown=True)


def _save_as_pdf(tz_text: str, pdf_path: Path) -> None:
    pdf = FPDF(format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    _register_pdf_fonts(pdf)
    pdf.set_font("Unicode", size=11)

    pdf.set_font("Unicode", style="B", size=16)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=pdf.epw, h=10, text="Техническое задание")
    pdf.ln(3)
    pdf.set_font("Unicode", size=11)

    for line in tz_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("### "):
            pdf.set_font("Unicode", style="B", size=12)
            _render_pdf_line(pdf, line[4:], h=8)
            pdf.set_font("Unicode", size=11)
        elif line.startswith("## "):
            pdf.set_font("Unicode", style="B", size=13)
            _render_pdf_line(pdf, line[3:], h=8)
            pdf.set_font("Unicode", size=11)
        elif line.startswith("# "):
            pdf.set_font("Unicode", style="B", size=15)
            _render_pdf_line(pdf, line[2:], h=9)
            pdf.set_font("Unicode", size=11)
        else:
            _render_pdf_line(pdf, line, h=7)
    pdf.output(str(pdf_path))


def _save_tz_files(tz_text: str, output_dir: Path) -> tuple[Path, Path]:
    docx_path = output_dir / "technical_specification.docx"
    pdf_path = output_dir / "technical_specification.pdf"
    _save_as_docx(tz_text, docx_path)
    _save_as_pdf(tz_text, pdf_path)
    return docx_path, pdf_path

def get_tz_generator() -> TZGenerator:
    settings = get_settings()
    llm = OpenAICompatibleLLMService(
        api_key=settings.llm_api_key.get_secret_value(),
        base_url=settings.llm_base_url,
        model=settings.llm_model,
    )
    return TZGenerator(llm)

@router.callback_query(F.data == "start_interview")
async def start_interview(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(DialogueStates.interviewing)
    await state.update_data(history=[], answers={})

    generator = get_tz_generator()
    first_question = await generator.generate_next_message([
        {"role": "user", "content": "Начни интервью. Задай первый вопрос о проекте."}
    ])

    await state.update_data(history=[{"role": "assistant", "content": first_question}])

    await callback.message.answer(f"👋 Отлично, давайте вместе подготовим ТЗ!\n\n💬 {first_question}")

@router.message(StateFilter(DialogueStates.interviewing))
async def process_answer(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        history = data.get("history", [])
        answers = data.get("answers", {})

        answer = message.text or ""
        history.append({"role": "user", "content": answer})
        answers[f"answer_{len(answers)+1}"] = answer

        generator = get_tz_generator()
        next_response = await generator.generate_next_message(history)

        if next_response.strip().upper().startswith("DONE"):
            await state.set_state(DialogueStates.generating)
            await state.update_data(history=history, answers=answers)
            await message.answer("✅ Спасибо за ответы! Уже собираю ваше техническое задание 📄✨")

            tz_text = await generator.generate_tz(answers, history)
            with TemporaryDirectory(prefix="telegram-tz-") as temp_dir:
                docx_path, pdf_path = _save_tz_files(tz_text, Path(temp_dir))
                await message.answer(
                    "🎉 Готово! Ваше техническое задание подготовлено.\n"
                    "📎 Прикрепила версии в DOCX и PDF — выберите удобную!"
                )
                await message.answer_document(
                    FSInputFile(docx_path), caption="📝 Техническое задание (DOCX)"
                )
                await message.answer_document(
                    FSInputFile(pdf_path), caption="📄 Техническое задание (PDF)"
                )
            await state.clear()
            return

        history.append({"role": "assistant", "content": next_response})
        await state.update_data(history=history, answers=answers)
        await message.answer(f"💬 {next_response}")
    except Exception:
        logger.exception("Ошибка при обработке ответа или подготовке/отправке ТЗ")
        await state.set_state(DialogueStates.interviewing)
        await message.answer(
            "😔 Не получилось обработать ответ или подготовить файлы. "
            "Ваши ответы сохранены — попробуйте ещё раз чуть позже. "
            "Если ошибка повторится, сообщите администратору бота."
        )
