import PySimpleGUI as pg

from screens.administrator import administrator_screen
from screens.customer import customer_screen

from constants import ADMINISTRATOR_ID, CUSTOMER_ID, PASSWORD


def login_screen(intro_event, intro_values):
    # open customer login window or admin login window
    if intro_event == 'Customer':
        # customer login window
        cust_login_layout = [[pg.Text("Customer ID:")],
                             [pg.Input(key='id')],
                             [pg.Text("Password:")],
                             [pg.Input(key='pass')],
                             [pg.Text(key='wrong_entry')],
                             [pg.Button('OK')]
                             ]
        cust_login_window = pg.Window('Customer Login', cust_login_layout)
        cust_login_event, cust_login_values = cust_login_window.read()
        # print(cust_login_values)
        # check customer ID and password against database
        if cust_login_values['id'] == CUSTOMER_ID and cust_login_values['pass'] == PASSWORD:
            cust_login_window.close()
            customer_screen()
        else:
            cust_login_window['wrong_entry'].update(
                'You have entered the wrong ID or password.')

    else:
        # admin login window
        admin_login_layout = [[pg.Text("Administrator ID:")],
                              [pg.Input(key='id')],
                              [pg.Text("Password:")],
                              [pg.Input(key='pass')],
                              [pg.Text(key='wrong_entry')],
                              [pg.Button('OK')]
                              ]

        admin_login_window = pg.Window('Customer Login', admin_login_layout)

        admin_login_event, admin_login_values = admin_login_window.read()
        # check admin ID and password against database
        if admin_login_values['id'] == ADMINISTRATOR_ID and admin_login_values['pass'] == PASSWORD:
            admin_login_window.close()
            administrator_screen()
        else:
            admin_login_window['wrong_entry'].update(
                'You have entered the wrong ID or password.')
