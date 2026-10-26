from dataclasses import dataclass
from datetime import datetime

from bot.domain.enums import GenerationStatus


@dataclass(slots=True, frozen=True)
class GenerationTaskData:
    id: str
    user_id: int
    status: GenerationStatus
    error_message: str | None = None
    result_url: str | None = None
    created_at: datetime | None = None
