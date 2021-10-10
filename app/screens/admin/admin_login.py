import PySimpleGUI as sg

from app.auth import set_current_user, Admin
from app.database.utils import initialise_mysql_database, validate_administrator_login
from app.screens.admin.admin_dashboard import administrator_screen
from app.screens.admin.admin_register import administrator_register_screen
from app.utils import setup_window

ID_VAL = 'id_val'
PASSWORD_VAL = 'password_val'
WRONG_ENTRY = 'wrong_entry'


def administrator_login_screen(intro_window):
    layout = [
        [sg.Column(
            [[sg.Text('Administrator ID:')],
             [sg.Input(key=ID_VAL, size=53)],
             [sg.Text('Password:')],
             [sg.Input(key=PASSWORD_VAL, size=53)],
             [sg.Text(key=WRONG_ENTRY)],
             [sg.Button('Login', size=25),
              sg.Button('Register', size=25)],
             [sg.Button('Initialise Database', size=52, pad=((6, 0), (25, 0)))]],
            pad=25
        )]
    ]

    window = setup_window('Administrator Login', layout, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        elif event == "Register":
            window.close()
            administrator_register_screen(intro_window)
            break

        elif event == 'Login':
            administrator = validate_administrator_login(values[ID_VAL], values[PASSWORD_VAL])
            if administrator:
                intro_window.close()
                window.close()
                set_current_user(administrator)
                administrator_screen()
                break
            else:
                window[WRONG_ENTRY].update(
                    'You have entered the wrong ID or password.', text_color='red')

        elif event == 'Initialise Database':
            initialise_mysql_database()

    window.close()
