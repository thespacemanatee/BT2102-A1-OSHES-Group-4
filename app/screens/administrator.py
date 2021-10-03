import PySimpleGUI as sg

from constants import ADMIN_NAME


def administrator_screen():
    # all diff tabs
    # tab1 main and logout
    admin_main_layout = [[sg.Text(f'Welcome, {ADMIN_NAME}. Please click on the tabs to access other functions.')],
                         [sg.Button('Log Out')]
                         ]
    # tab2 database initialisation
    admin_database_layout = [[sg.Text('database init here')]
                             ]
    # tab3 search + additional info + sold/unsold items
    admin_search_layout = [[sg.Text('search here')]
                           ]
    # tab4 request/service
    admin_request_layout = [[sg.Text('request here')]
                            ]
    # tab5 customers pending payment
    admin_payment_layout = [[sg.Text('payment pending here')]
                            ]
    # tab group
    admin_tabs = [[sg.TabGroup([[sg.Tab('Logout', admin_main_layout)],
                                [sg.Tab('Database initialisation',
                                        admin_database_layout)],
                                [sg.Tab('Search', admin_search_layout)],
                                [sg.Tab('Request', admin_request_layout)],
                                [sg.Tab('Payment pending', admin_payment_layout)]
                                ]
                               )]
                  ]
    admin_main_window = sg.Window(f"{ADMIN_NAME}'s session", admin_tabs)
    admin_main_event, admin_main_values = admin_main_window.read()
    if admin_main_event == 'Log Out':
        admin_main_window.close()
