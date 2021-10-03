import PySimpleGUI as pg

from constants import ADMIN_NAME


def administrator_screen():
    # all diff tabs
    # tab1 main and logout
    admin_main_layout = [[pg.Text('Welcome, '+ADMIN_NAME+'. '
                                  'Please click on the tabs to access other functions.')],
                         [pg.Button('Log Out')]
                         ]
    # tab2 database initialisation
    admin_database_layout = [[pg.Text('database init here')]
                             ]
    # tab3 search + additional info + sold/unsold items
    admin_search_layout = [[pg.Text('search here')]
                           ]
    # tab4 request/service
    admin_request_layout = [[pg.Text('request here')]
                            ]
    # tab5 customers pending payment
    admin_payment_layout = [[pg.Text('payment pending here')]
                            ]
    # tab group
    admin_tabs = [[pg.TabGroup([[pg.Tab('Logout', admin_main_layout)],
                                [pg.Tab('Database initialisation',
                                        admin_database_layout)],
                                [pg.Tab('Search', admin_search_layout)],
                                [pg.Tab('Request', admin_request_layout)],
                                [pg.Tab('Payment pending', admin_payment_layout)]
                                ]
                               )]
                  ]
    admin_main_window = pg.Window(ADMIN_NAME+"'s session", admin_tabs)
    admin_main_event, admin_main_values = admin_main_window.read()
