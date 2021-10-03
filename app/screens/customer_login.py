import PySimpleGUI as sg

from screens.customer import customer_screen
from utils import setup_window
from constants import CUSTOMER_ID, PASSWORD


def customer_login_screen():
    # customer login window
    layout = [[sg.Text('Customer ID:')],
              [sg.Input(key='id')],
              [sg.Text('Password:')],
              [sg.Input(key='pass')],
              [sg.Text(key='wrong_entry')],
              [sg.Button('Login', size=(25)),
               sg.Button('Cancel', size=(25))]
              ]
    window = setup_window('Customer Login', layout)

    while True:
        event, values = window.read()
        # print(cust_login_values)
        # check customer ID and password against database
        if values['id'] == CUSTOMER_ID and values['pass'] == PASSWORD:
            customer_screen()
            break
        else:
            window['wrong_entry'].update(
                'You have entered the wrong ID or password.')

        if event == "Cancel":
            break

    window.close()
