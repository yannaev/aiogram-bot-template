from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    get_user = State()
    block_user = State()
    unblock_user = State()
