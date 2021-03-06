import PySimpleGUI as sg

from app.auth import set_current_user, Customer
from app.database.utils import validate_customer_login
from app.screens.customer.cust_dashboard import customer_screen
from app.screens.customer.cust_register import customer_register_screen
from app.utils import setup_window

ID_VAL = 'id_val'
PASSWORD_VAL = 'password_val'
WRONG_ENTRY = 'wrong_entry'


def customer_login_screen(intro_window):
    layout = [
        [sg.Column(
            [[sg.Text('Customer ID:')],
             [sg.Input(key=ID_VAL, size=53)],
             [sg.Text('Password:')],
             [sg.Input(key=PASSWORD_VAL, size=53)],
             [sg.Text(key=WRONG_ENTRY)],
             [sg.Button('Login', size=25),
              sg.Button('Register', size=25)],
             ],
            pad=25
        )]
    ]

    window = setup_window('Customer Login', layout, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        elif event == "Register":
            window.close()
            customer_register_screen(intro_window)
            break

        elif event == 'Login':
            customer = validate_customer_login(values[ID_VAL],
                                               values[PASSWORD_VAL])
            if values[ID_VAL] == '' and values[PASSWORD_VAL] == '':
                window[WRONG_ENTRY].update(
                    'Please enter your Login Information', text_color='red')    
            elif values[ID_VAL] == '':
                window[WRONG_ENTRY].update(
                    'Please enter your Customer ID.', text_color='red')
            elif values[PASSWORD_VAL] == '':
                window[WRONG_ENTRY].update(
                    'Please enter your password.', text_color='red')
            elif customer:
                intro_window.close()
                window.close()
                set_current_user(customer)
                customer_screen()
                break
            else:
                window[WRONG_ENTRY].update(
                    'You have entered the wrong ID or password.', text_color='red')

    window.close()
