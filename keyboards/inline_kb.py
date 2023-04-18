from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


inline_menu_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
menu_status_button: InlineKeyboardButton = InlineKeyboardButton(text="Статус диалога",
                                                                callback_data="dialog_status")
menu_first_dep_button: InlineKeyboardButton = InlineKeyboardButton(text="Первый депозит",
                                                                   callback_data="first_deposit")
menu_second_dep_button: InlineKeyboardButton = InlineKeyboardButton(text="Депозит",
                                                                    callback_data="other_deposits")
menu_start_cap_button: InlineKeyboardButton = InlineKeyboardButton(text="Стартовый капитал",
                                                                   callback_data="start_capital")
inline_menu_kb_builder.row(menu_status_button).row(menu_first_dep_button).row(menu_second_dep_button).row(menu_start_cap_button)
inline_menu_kb: InlineKeyboardMarkup = inline_menu_kb_builder.as_markup(resize_keyboard=True)


inline_status_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
status_button_new: InlineKeyboardButton = InlineKeyboardButton(text="Новый",
                                                               callback_data="status_new")
status_button_registration: InlineKeyboardButton = InlineKeyboardButton(text="Регистрация",
                                                                        callback_data="status_registration")
status_button_working: InlineKeyboardButton = InlineKeyboardButton(text="В работе",
                                                                   callback_data="status_working")
status_button_passed: InlineKeyboardButton = InlineKeyboardButton(text="Не ЦА",
                                                                  callback_data="status_passed")
status_back_button: InlineKeyboardButton = InlineKeyboardButton(text="Назад",
                                                                callback_data="status_back")
inline_status_kb_builder.row(status_button_new, status_button_registration).row(status_button_working, status_button_passed).row(status_back_button)
inline_status_kb: InlineKeyboardMarkup = inline_status_kb_builder.as_markup(resize_keyboard=True)


inline_back_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
back_button: InlineKeyboardButton = InlineKeyboardButton(text="Назад",
                                                         callback_data="back")
inline_back_kb_builder.row(back_button)
kb_back: InlineKeyboardMarkup = inline_back_kb_builder.as_markup(resize_keyboard=True)


inline_kb_channel_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
channel_button1: InlineKeyboardButton = InlineKeyboardButton(text="Crypto HYPE 😎💰 Futures Trading",
                                                             callback_data="crypto_hype")
channel_button2: InlineKeyboardButton = InlineKeyboardButton(text="Crypto Reality",
                                                             callback_data="crypto_reality")
channel_button3: InlineKeyboardButton = InlineKeyboardButton(text="Crypto Party — 🟡 Binance | Futures",
                                                             callback_data="crypto_party")
channel_button4: InlineKeyboardButton = InlineKeyboardButton(text="🚀 To the Moon - Crypto & Trading",
                                                             callback_data="moon")
channel_button5: InlineKeyboardButton = InlineKeyboardButton(text="BTC Empire | Crypto Futures Trading",
                                                             callback_data="btc_empire")
inline_kb_channel_builder.row(channel_button1).row(channel_button2).row(channel_button3).row(channel_button4).row(channel_button5)
ikb_channels: InlineKeyboardMarkup = inline_kb_channel_builder.as_markup(resize_keyboard=True)