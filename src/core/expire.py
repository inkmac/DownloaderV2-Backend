import json
import sys
from datetime import datetime, timedelta
from typing import TypedDict

from PySide6.QtCore import QSettings
from cryptography.fernet import Fernet

settings = QSettings("Downloader", "MyApp")
DATA_CONFIG_KEY = "data_config"
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

SECRET_KEY = b'6TymdYXbZq9GO3F1RMz4aOt8mW0zGyeTIHuogmKsVzE='
fernet = Fernet(SECRET_KEY)


class ExpireConfig(TypedDict):
    first_used_time: str
    expire_day: int
    expire_date_time: str
    latest_used_time: str
    is_expired: bool


def format_date_time(date_time: datetime) -> str:
    return date_time.strftime(DATETIME_FORMAT)


def parse_date_time(date_time: str) -> datetime:
    return datetime.strptime(date_time, DATETIME_FORMAT)


def read_config() -> ExpireConfig | None:
    try:
        encrypted = settings.value(DATA_CONFIG_KEY, defaultValue=None)
        if encrypted is None:
            return None

        decrypted = fernet.decrypt(str(encrypted).encode())
        return json.loads(decrypted.decode())
    except Exception:
        sys.exit(1)


def write_config(data: ExpireConfig):
    try:
        bytes_data = json.dumps(data).encode()
        encrypted = fernet.encrypt(bytes_data).decode()

        settings.setValue(DATA_CONFIG_KEY, encrypted)
        settings.sync()   # 确保立即写入磁盘
    except Exception:
        sys.exit(1)


def is_config_initialized() -> bool:
    return read_config() is not None


def initialize_config(expire_day: int = 30):
    if is_config_initialized():
        return

    first_used_time = datetime.now()
    expire_date_time = datetime.now() + timedelta(days=expire_day)
    data: ExpireConfig = {
        'first_used_time': format_date_time(first_used_time),
        'expire_day': expire_day,
        'expire_date_time': format_date_time(expire_date_time),
        'latest_used_time': format_date_time(first_used_time),
        'is_expired': False
    }
    write_config(data)


def save_current_time(current_time: datetime) -> bool:
    """
    :return: True if the software is expired checked with `current_time` or system time error,
        False if the software is not expired
    """
    data = read_config()

    latest_used_time: datetime = parse_date_time(data['latest_used_time'])
    expire_date_time: datetime = parse_date_time(data['expire_date_time'])

    # 检查时间是否异常, 系统时间是否被修改提前
    # 如果异常, 直接设置为expired
    if current_time < latest_used_time:
        data['is_expired'] = True
        return True

    # 检测当前时间是否过期
    if current_time > expire_date_time:
        data['is_expired'] = True
        return True

    data['latest_used_time'] = format_date_time(current_time)

    write_config(data)
    return False


def is_expired() -> bool:
    data = read_config()

    is_expire: bool = data['is_expired']
    if is_expire:
        return True

    return False


__all__ = ['initialize_config', 'save_current_time', 'is_expired']