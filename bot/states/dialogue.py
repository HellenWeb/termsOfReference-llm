from aiogram.fsm.state import State, StatesGroup

class DialogueStates(StatesGroup):
    interviewing = State()          
    reviewing = State()
    generating = State()
