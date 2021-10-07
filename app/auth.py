from typing import Union

current_user = None


class Admin:
    def __init__(self, admin_id, name, gender, phone):
        self.id = admin_id
        self.name = name
        self.gender = gender
        self.phone = phone


class Customer:
    def __init__(self, cust_id, name, gender, email, address, phone):
        self.id = cust_id
        self.name = name
        self.gender = gender
        self.email = email
        self.address = address
        self.phone = phone


def set_current_user(user: Union[Admin, Customer]):
    global current_user
    current_user = user


def get_current_user() -> Union[Admin, Customer, None]:
    return current_user
