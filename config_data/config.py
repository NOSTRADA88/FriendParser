from dataclasses import dataclass
from typing import List
from environs import Env


@dataclass
class Admin:
    admin_list: List[str]


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    admins: Admin


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), admins=Admin(admin_list=env('ADMIN_IDS')))
