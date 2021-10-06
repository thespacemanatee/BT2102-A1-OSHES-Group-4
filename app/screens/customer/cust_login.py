import PySimpleGUI as sg

from app.screens.customer.cust_dashboard import customer_screen
from app.utils import setup_window
from app.constants import CUSTOMER_ID, PASSWORD

ID_VAL = 'id_val'
PASSWORD_VAL = 'password_val'
WRONG_ENTRY = 'wrong_entry'


def customer_login_screen(intro_window):
    # customer login window
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
            # TODO
            pass

        # check customer ID and password against database
        elif values[ID_VAL] == CUSTOMER_ID and values['pass'] == PASSWORD:
            window.close()
            intro_window.close()
            customer_screen()
        else:
            window[WRONG_ENTRY].update(
                'You have entered the wrong ID or password.', text_color='red')

    window.close()
