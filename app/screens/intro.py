import PySimpleGUI as sg

from screens.administrator_login import administrator_login_screen
from screens.customer_login import customer_login_screen
from constants import ASCII_LOGO
from utils import setup_window


def intro_screen():
    layout_column = [[sg.Text(ASCII_LOGO, justification='center')],
                     [sg.Text("Welcome to OSHES.")],
                     [sg.Text("Are you a customer or an administrator?")],
                     [sg.Button('Customer', size=25), sg.Button(
                         'Administrator', size=25)]
                     ]
    layout = [[sg.Column(layout_column, element_justification='center')]]
    window = setup_window('OSHES - Group 4', layout)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        # goes to screens/login.py - open customer login window or admin login window
        elif event == "Customer":
            customer_login_screen(window)
        elif event == "Administrator":
            administrator_login_screen(window)
