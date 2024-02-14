from aiogram.fsm.state import StatesGroup,State



class RegisterStates(StatesGroup):

    regEmail=State()
    regName=State()
    regBirthYear=State()