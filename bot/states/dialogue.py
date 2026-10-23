"""FSM states for collecting project requirements."""

from aiogram.fsm.state import State, StatesGroup


class DialogueStates(StatesGroup):
    """Planned stages of the requirements-gathering conversation."""

    waiting_for_project_name = State()
    waiting_for_project_description = State()
    waiting_for_target_audience = State()
    waiting_for_core_features = State()
    waiting_for_constraints = State()
    reviewing_answers = State()
