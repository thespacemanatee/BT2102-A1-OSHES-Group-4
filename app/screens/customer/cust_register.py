import PySimpleGUI as sg

from app.auth import set_current_user, Customer
from app.database.utils import is_cust_username_taken, insert_customer
from app.screens.customer.cust_dashboard import customer_screen
from app.utils import setup_window

GENDERS = ['Male', 'Female', 'Others']

USERNAME_VAL = 'username_val'
NAME_VAL = 'name_val'
GENDER_VAL = 'gender_val'
EMAIL_ADDRESS_VAL = 'email_address_val'
PHONE_NUMBER_VAL = 'phone_number_val'
ADDRESS_VAL = 'address_val'
PASSWORD_VAL = 'password_val'
WRONG_ENTRY = 'wrong_entry'


def customer_register_screen(intro_window):
    layout = [[sg.Column([
        [sg.Text('Customer ID:')],
        [sg.Input(key=USERNAME_VAL, size=53)],
        [sg.Text('Name:')],
        [sg.Input(key=NAME_VAL, size=53)],
        [sg.Text('Gender:')],
        [sg.OptionMenu(values=GENDERS, key=GENDER_VAL, size=10)],
        [sg.Text('Email Address:')],
        [sg.Input(key=EMAIL_ADDRESS_VAL, size=53)],
        [sg.Text('Address:')],
        [sg.Input(key=ADDRESS_VAL, size=53)],
        [sg.Text('Phone Number:')],
        [sg.Input(key=PHONE_NUMBER_VAL, size=53)],
        [sg.Text('Password:')],
        [sg.Input(key=PASSWORD_VAL, size=53)],
        [sg.Text(key=WRONG_ENTRY)],
        [sg.Button('Register', size=25),
         sg.Button('Cancel', size=25)]
    ], pad=25)]]

    window = setup_window('Customer Registration', layout, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        elif event == 'Cancel':
            break

        elif event == 'Register' and values[USERNAME_VAL] and values[NAME_VAL] and values[GENDER_VAL] and \
                values[EMAIL_ADDRESS_VAL] and values[PHONE_NUMBER_VAL] and values[ADDRESS_VAL] and values[PASSWORD_VAL]:
            try:
                if values[PHONE_NUMBER_VAL]:
                    username = values[USERNAME_VAL]
                    if is_cust_username_taken(username):
                        raise ValueError('Username taken')
                    name = values[NAME_VAL]
                    gender = values[GENDER_VAL]
                    email = values[EMAIL_ADDRESS_VAL]
                    address = values[ADDRESS_VAL]
                    phone = int(values[PHONE_NUMBER_VAL])
                    password = values[PASSWORD_VAL]
                    insert_customer(username, name, gender, email, address, phone, password)
                    set_current_user(Customer(username, name, gender, email, address, phone))
                    window.close()
                    intro_window.close()
                    customer_screen()
                break
            except ValueError as e:
                if str(e) == 'Username taken':
                    window[WRONG_ENTRY].update(
                        'Username already taken.', text_color='red')
                else:
                    window[WRONG_ENTRY].update(
                        'Please make sure phone number is a number.', text_color='red')

        else:
            window[WRONG_ENTRY].update(
                'Please make sure every field is completed.', text_color='red')

    window.close()
