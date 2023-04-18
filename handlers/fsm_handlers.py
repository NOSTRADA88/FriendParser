from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Text, Command
from keyboards.inline_kb import inline_menu_kb, kb_back, ikb_channels
from aiogram import Router, types, F
from aiogram.fsm.state import default_state
from middleware.data_base import DataBase
from datetime import datetime
from config_data.config import Config, load_config

router: Router = Router()
db: DataBase = DataBase("middleware/DataBase.db")
config: Config = load_config()


class ForwardUser(StatesGroup):
    user_id: State = State()
    user_name: State = State()


class FirstDeposit(ForwardUser):
    first_deposit: State = State()
    user_id: State = ForwardUser.user_id
    user_name: State = ForwardUser.user_name


class Deposit(ForwardUser):
    deposit: State = State()
    user_id: State = ForwardUser.user_id
    user_name: State = ForwardUser.user_name


class StartCapital(ForwardUser):
    start_capital: State = State()
    user_id: State = ForwardUser.user_id
    user_name: State = ForwardUser.user_name


class AddManager(StatesGroup):
    user_id: State = State()
    channel_name: State = State()


class DeleteManger(StatesGroup):
    user_id: State = State()


@router.callback_query(Text(text="back"))
async def callback_return_back(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Выберите кнопку", reply_markup=inline_menu_kb)


@router.callback_query(Text(text="status_back"))
async def callback_return_back(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Выберите кнопку", reply_markup=inline_menu_kb)


@router.message(Command(commands='stop'), ~StateFilter(default_state))
async def process_cancel_command_state(message: types.Message, state: FSMContext):
    await message.answer(text="Вы закончили работу с ботом, чтобы начать работу с новым клиентом перешлите сообщение")
    await state.clear()


@router.message(F.forward_from)
async def get_forward_user_id(message: types.Message, state: FSMContext):
    await message.answer(text=f"Заносим информацию по {message.forward_from.username}", reply_markup=inline_menu_kb)
    await state.update_data(user_id=message.forward_from.id, user_name="@"+str(message.forward_from.username))
    db.add_date(manager_id=message.chat.id, user_id=message.forward_from.id, date=datetime.now().strftime("%d-%m-%Y"))


@router.callback_query(Text(text="first_deposit"))
async def callback_first_deposit(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text='Введите первый депозит в формате: 100,00', reply_markup=kb_back)
    await state.set_state(FirstDeposit.first_deposit)


@router.message(StateFilter(FirstDeposit.first_deposit))
async def state_first_deposit(message: types.Message, state: FSMContext):
    if "," in message.text:
        await state.update_data(first_deposit=message.text)
        first_deposit_data = await state.get_data()
        await message.answer(
            text=f"Вы ввели депозит для {first_deposit_data['user_name']}: {first_deposit_data['first_deposit']}\n\nВыберите что хотите добавить",
            reply_markup=inline_menu_kb)
        db.add_first_deposit(first_deposit_data['user_id'],message.from_user.id, first_deposit_data['first_deposit'])
        await state.update_data(first_deposit="")
    else:
        await message.answer("Введите первый депозит правильно!\nВ формате: 100,00")


@router.callback_query(Text(text="other_deposits"))
async def callback_deposit(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text='Введите депозит в формате: 100,00', reply_markup=kb_back)
    await state.set_state(Deposit.deposit)


@router.message(StateFilter(Deposit.deposit))
async def state_deposit(message: types.Message, state: FSMContext):
    if "," in message.text:
        await state.update_data(deposit=message.text)
        deposit_data = await state.get_data()
        await message.answer(text=f"Вы ввели депозит для {deposit_data['user_name']}: {deposit_data['deposit']}\n\nВыберите что хотите добавить",
                             reply_markup=inline_menu_kb)
        db.add_other_deposit(deposit_data['user_id'], message.from_user.id, deposit_data['deposit'])
        await state.update_data(deposit="")
    else:
        await message.answer("Введите депозит правильно!\nВ формате: 100,00")


@router.callback_query(Text(text="start_capital"))
async def callback_deposit(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text='Введите стартовый капитал в формате: 100(целое число)', reply_markup=kb_back)
    await state.set_state(StartCapital.start_capital)


@router.message(StateFilter(StartCapital.start_capital))
async def state_deposit(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(start_capital=message.text)
        start_capital_data = await state.get_data()
        await message.answer(
            text=f"Вы ввели стартовый капитал для {start_capital_data['user_name']}: {start_capital_data['start_capital']}\n\nВыберите что хотите добавить",
            reply_markup=inline_menu_kb)
        db.add_start_capital(start_capital_data['user_id'], message.from_user.id, start_capital_data['start_capital'])
        await state.update_data(start_capital="")
    else:
        await message.answer("Введите стартовый капитал правильно!\nВ формате: 100", reply_markup=kb_back)


@router.message(Command(commands='add'))
async def process_add_manager_command(message: types.Message, state: FSMContext):
    for admin in str(config.admins.admin_list).split(","):
        if message.from_user.id == int(admin):
            try:
                await message.answer(text="отправьте мне id пользователя которого хотите сделать менеджером")
                await state.set_state(AddManager.user_id)
            except:
                await message.answer("Простите, у вас нет доступа к этой команде.")


@router.message(StateFilter(AddManager.user_id))
async def add_manager(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(add_manager_id=message.text)
        add_manager_id_data = await state.get_data()
        await message.answer(text=f'Выберите канал в который вы хотите добавить менеджера с id:{add_manager_id_data["add_manager_id"]}', reply_markup=ikb_channels)
        await state.set_state(AddManager.channel_name)
    else:
        await message.answer(text='Похоже вы пытаетесь отпрвить мне некорректный id')


@router.callback_query(StateFilter(AddManager.channel_name))
async def add_channel_to_manager(callback: types.CallbackQuery, state: FSMContext):
    match callback.data:
        case "crypto_hype":
            await state.update_data(add_channel=callback.data)
            add_manager_id_data = await state.get_data()
            try:
                db.add_manager(channel_name="Crypto HYPE 😎💰 Futures Trading",
                               manager_id=add_manager_id_data['add_manager_id'],
                               date=datetime.now().strftime("%d-%m-%Y"))
                db.add_manager_to_channel("Crypto HYPE 😎💰 Futures Trading")
                await callback.message.answer(text=f"Вы добавили менеджера с id:{add_manager_id_data['add_manager_id']} в канал Crypto HYPE 😎💰 Futures Trading")
            except:
                await callback.message.answer(text=f"вы пытаетесь добавить менеджера с id:{add_manager_id_data['add_manager_id']}, который уже назначен менджером другого канала")
        case "crypto_reality":
            await state.update_data(add_channel=callback.data)
            add_manager_id_data = await state.get_data()
            try:
                db.add_manager(channel_name="Crypto Reality",
                               manager_id=add_manager_id_data['add_manager_id'],
                               date=datetime.now().strftime("%d-%m-%Y"))
                db.add_manager_to_channel("Crypto Reality")
                await callback.message.answer(text=f"Вы добавили менеджера с id:{add_manager_id_data['add_manager_id']} в канал Crypto Reality")
            except:
                await callback.message.answer(text=f"вы пытаетесь добавить менеджера с id:{add_manager_id_data['add_manager_id']}, который уже назначен менджером другого канала")
        case "moon":
            await state.update_data(add_channel=callback.data)
            add_manager_id_data = await state.get_data()
            try:
                db.add_manager(channel_name="🚀 To the Moon - Crypto & Trading",
                               manager_id=add_manager_id_data['add_manager_id'],
                               date=datetime.now().strftime("%d-%m-%Y"))
                db.add_manager_to_channel("🚀 To the Moon - Crypto & Trading")
                await callback.message.answer(text=f"Вы добавили менеджера с id:{add_manager_id_data['add_manager_id']} в канал 🚀 To the Moon - Crypto & Trading")
            except:
                await callback.message.answer(text=f"вы пытаетесь добавить менеджера с id:{add_manager_id_data['add_manager_id']}, который уже назначен менджером другого канала")
        case "crypto_party":
            await state.update_data(add_channel=callback.data)
            add_manager_id_data = await state.get_data()
            try:
                db.add_manager(channel_name="Crypto Party — 🟡 Binance | Futures",
                               manager_id=add_manager_id_data['add_manager_id'],
                               date=datetime.now().strftime("%d-%m-%Y"))
                db.add_manager_to_channel("Crypto Party — 🟡 Binance | Futures")
                await callback.message.answer(text=f"Вы добавили менеджера с id:{add_manager_id_data['add_manager_id']} в канал Crypto Party — 🟡 Binance | Futures")
            except:
                await callback.message.answer(text=f"вы пытаетесь добавить менеджера с id:{add_manager_id_data['add_manager_id']}, который уже назначен менджером другого канала")
        case "btc_empire":
            await state.update_data(add_channel=callback.data)
            add_manager_id_data = await state.get_data()
            try:
                db.add_manager(channel_name="BTC Empire | Crypto Futures Trading",
                               manager_id=add_manager_id_data['add_manager_id'],
                               date=datetime.now().strftime("%d-%m-%Y"))
                db.add_manager_to_channel("BTC Empire | Crypto Futures Trading")
                await callback.message.answer(text=f"Вы добавили менеджера с id:{add_manager_id_data['add_manager_id']} в канал BTC Empire | Crypto Futures Trading")
            except:
                await callback.message.answer(text=f"вы пытаетесь добавить менеджера с id:{add_manager_id_data['add_manager_id']}, который уже назначен менджером другого канала")
        case _:
            await callback.message.answer(text="Простите, вы пытаетесь выбрать канал, которого нет в списке. Попробуйте ещё раз!")
    await state.clear()


@router.message(Command(commands='remove'))
async def process_add_manager_command(message: types.Message, state: FSMContext):
    for admin in str(config.admins.admin_list).split(","):
        if message.from_user.id == int(admin):
            try:
                await message.answer(text=f'Отправьте мне id менеджере которого хотите удалить')
                await state.set_state(DeleteManger.user_id)
            except:
                await message.answer("Простите, у вас нет доступа к этой команде.")


@router.message(StateFilter(DeleteManger.user_id))
async def add_manager(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(delete_manager_id=message.text)
        delete_manager_id_data = await state.get_data()
        db.delete_manager(delete_manager_id_data['delete_manager_id'])
        await message.answer(text=f'Администратор с id:{delete_manager_id_data["delete_manager_id"]} был удалён')
        await state.clear()
    else:
        await message.answer(text='Похоже вы пытаетесь отпрвить мне некорректный id')