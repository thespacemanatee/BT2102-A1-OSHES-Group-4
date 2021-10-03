import PySimpleGUI as sg

from screens.administrator import administrator_screen
from utils import setup_window
from constants import ADMINISTRATOR_ID, PASSWORD


def administrator_login_screen(intro_window):
    # admin login window
    layout = [[sg.Text('Administrator ID:')],
              [sg.Input(key='id')],
              [sg.Text('Password:')],
              [sg.Input(key='pass')],
              [sg.Text(key='wrong_entry')],
              [sg.Button('Login', size=25),
               sg.Button('Cancel', size=25)]
              ]

    window = setup_window('Customer Login', layout)

    while True:
        event, values = window.read()

        if event in ("Cancel", sg.WIN_CLOSED):
            break
        
        # check admin ID and password against database
        elif values['id'] == ADMINISTRATOR_ID and values['pass'] == PASSWORD:
            window.close()
            intro_window.close()
            administrator_screen()
        else:
            window['wrong_entry'].update(
                'You have entered the wrong ID or password.')

    window.close()
