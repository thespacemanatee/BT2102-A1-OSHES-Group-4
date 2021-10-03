import PySimpleGUI as sg

from app.screens.admin.admin_dashboard import administrator_screen
from app.utils import setup_window
from app.constants import ADMINISTRATOR_ID, PASSWORD


def administrator_login_screen(intro_window):
    # admin login window
    layout_column = [[sg.Text('Administrator ID:')],
                     [sg.Input(key='id')],
                     [sg.Text('Password:')],
                     [sg.Input(key='pass')],
                     [sg.Text(key='wrong_entry')],
                     [sg.Button('Login', size=25),
                      sg.Button('Cancel', size=25)]
                     ]

    layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
              [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
               sg.Column(layout_column, vertical_alignment='center', justification='center', k='-C-')]]

    window = setup_window('Administrator Login', layout)
    window['-C-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)

    while True:
        event, values = window.read()

        if event == "Cancel":
            break

        elif event == sg.WIN_CLOSED:
            intro_window.close()
            break

        # check admin ID and password against database
        elif values['id'] == ADMINISTRATOR_ID and values['pass'] == PASSWORD:
            window.close()
            intro_window.close()
            administrator_screen()
        else:
            window['wrong_entry'].update(
                'You have entered the wrong ID or password.', text_color='red')

    window.close()
