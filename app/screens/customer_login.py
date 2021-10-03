import PySimpleGUI as sg

from app.screens.customer import customer_screen
from app.utils import setup_window
from app.constants import CUSTOMER_ID, PASSWORD


def customer_login_screen(intro_window):
    # customer login window
    layout_column = [[sg.Text('Customer ID:')],
                     [sg.Input(key='id', size=53)],
                     [sg.Text('Password:')],
                     [sg.Input(key='pass', size=53)],
                     [sg.Text(key='wrong_entry')],
                     [sg.Button('Login', size=25),
                      sg.Button('Cancel', size=25)]
                     ]

    layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
              [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
               sg.Column(layout_column, vertical_alignment='center', justification='center', k='-C-')]]

    window = setup_window('Customer Login', layout)
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

        # check customer ID and password against database
        elif values['id'] == CUSTOMER_ID and values['pass'] == PASSWORD:
            window.close()
            intro_window.close()
            customer_screen()
        else:
            window['wrong_entry'].update(
                'You have entered the wrong ID or password.')

    window.close()
