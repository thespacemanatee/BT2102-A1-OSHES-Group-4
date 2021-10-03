import PySimpleGUI as sg

from app.screens.administrator_login import administrator_login_screen
from app.screens.customer_login import customer_login_screen
from app.constants import ASCII_LOGO
from app.utils import setup_window, window_size


def intro_screen():
    layout_column = [[sg.Text(ASCII_LOGO)],
                     [sg.Text("Welcome to OSHES.")],
                     [sg.Text("Are you a customer or an administrator?")],
                     [sg.Button('Customer', size=25), sg.Button(
                         'Administrator', size=25)]
                     ]
    layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
              [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
               sg.Column(layout_column, vertical_alignment='center', justification='center', k='-C-')]]

    window = setup_window('OSHES - Group 4', layout)
    window['-C-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        # goes to screens/login.py - open customer login window or admin login window
        elif event == "Customer":
            customer_login_screen(window)
        elif event == "Administrator":
            administrator_login_screen(window)
