import PySimpleGUI as sg

from app.components.centered_component import centered_component, COLUMN, EXPAND_1, EXPAND_2
from app.constants import ASCII_LOGO
from app.database.utils import cancel_requests_after_deadline
from app.screens.admin.admin_login import administrator_login_screen
from app.screens.customer.cust_login import customer_login_screen
from app.utils import setup_window

INTRO_WINDOW_SIZE = (800, 700)


def intro_screen():
    cancel_requests_after_deadline()
    center_component = [sg.Column([[sg.Text(ASCII_LOGO)],
                                   [sg.Text("Welcome to OSHES.")],
                                   [sg.Text("Are you a customer or an administrator?")],
                                   [sg.Button('Customer', size=25), sg.Button(
                                       'Administrator', size=25)]
                                   ])]
    layout = centered_component(centered_children=center_component)

    window = setup_window('OSHES - Group 4', layout, size=INTRO_WINDOW_SIZE)
    window[COLUMN].expand(True, True, True)
    window[EXPAND_1].expand(True, True, True)
    window[EXPAND_2].expand(True, False, True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        # goes to screens/admin_login.py - open customer login window or admin login window
        elif event == "Customer":
            customer_login_screen(window)
        elif event == "Administrator":
            administrator_login_screen(window)
