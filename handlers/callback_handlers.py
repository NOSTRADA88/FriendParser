from aiogram import Router, types, Bot
from config_data.config import Config, load_config
from aiogram.filters import Text, StateFilter
from aiogram.filters.state import State
from aiogram.fsm.context import FSMContext
from keyboards.inline_kb import inline_menu_kb, inline_status_kb
from handlers.fsm_handlers import ForwardUser
from middleware.data_base import DataBase

config: Config = load_config()
router: Router = Router()
bot: Bot = Bot(token=config.tg_bot.token)
db: DataBase = DataBase("middleware/DataBase.db")


class Status(ForwardUser):
    user_id: State = ForwardUser.user_id
    user_name: State = ForwardUser.user_name
    dialog_status: State = State()


@router.callback_query(Text(text="dialog_status"))
async def callback_dialog_status(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Выберите статус диалога:",
                           reply_markup=inline_status_kb)
    await state.set_state(Status.dialog_status)


@router.callback_query(Text(text="status_new"), StateFilter(Status.dialog_status))
async def callback_dialog_status_new(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(status_new=0)
    status_new_data = await state.get_data()
    await callback.answer()
    await callback.message.edit_text(text=f'Вы поставили Статус: "Новый" для пользователя {status_new_data["user_name"]}\n\nВыберите что хотите добавить',
                           reply_markup=inline_menu_kb)
    db.add_client_status(status_new_data["user_id"], callback.from_user.id, status_new_data["status_new"])
    await state.update_data(status_new="")


@router.callback_query(Text(text="status_registration"), StateFilter(Status.dialog_status))
async def callback_dialog_status_registration(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(status_registration=1)
    status_registration_data = await state.get_data()
    await callback.answer()
    await callback.message.edit_text(text=f'Вы поставили Статус: "Регистрация" для пользователя {status_registration_data["user_name"]}\n\nВыберите что хотите добавить',
                           reply_markup=inline_menu_kb)
    db.add_client_status(status_registration_data["user_id"], callback.from_user.id, status_registration_data["status_registration"])
    await state.update_data(status_registration="")


@router.callback_query(Text(text="status_working"), StateFilter(Status.dialog_status))
async def callback_working_status(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(status_working=2)
    status_working_data = await state.get_data()
    await callback.answer()
    await callback.message.edit_text(text=f'Вы поставили Статус: "В работе" для пользователя {status_working_data["user_name"]}\n\nВыберите что хотите добавить',
                           reply_markup=inline_menu_kb)
    db.add_client_status(status_working_data["user_id"], callback.from_user.id, status_working_data["status_working"])
    await state.update_data(status_working="")


@router.callback_query(Text(text="status_passed"), StateFilter(Status.dialog_status))
async def callback_working_status(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(status_passed=3)
    status_passed_data = await state.get_data()
    await callback.answer()
    await callback.message.edit_text(text=f'Вы поставили Статус: "Не ЦА" для пользователя {status_passed_data["user_name"]}\n\nВыберите что хотите добавить',
                           reply_markup=inline_menu_kb)
    db.add_client_status(status_passed_data["user_id"], callback.from_user.id, status_passed_data["status_passed"])
    await state.update_data(status_passed="")

