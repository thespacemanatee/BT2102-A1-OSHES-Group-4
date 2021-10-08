from typing import Union

from app.models.administrator import Admin
from app.models.customer import Customer

current_user = None


def set_current_user(user: Union[Admin, Customer]):
    global current_user
    current_user = user


def get_current_user() -> Union[Admin, Customer, None]:
    return current_user
