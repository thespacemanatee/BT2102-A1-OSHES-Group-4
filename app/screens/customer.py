import PySimpleGUI as pg

from constants import CUSTOMER_NAME


def customer_screen():
    # all the different tabs
    # tab1 main and logout
    cust_main_layout = [[pg.Text(f'Welcome, {CUSTOMER_NAME}. Please click on the tabs to access other functions.')],
                        [pg.Button('Log Out')]
                        ]
    # tab2 search & purchase
    # filters in the dropdown menu; filter by item attributes
    attributes = ['ItemID',
                  'Category',
                  'Color',
                  'Factory',
                  'PowerSupply',
                  'PurchaseStatus',
                  'ProductionYear',
                  'Model',
                  'ServiceStatus']

    cust_search_layout = [[pg.Text('Search for an item:')],
                          [pg.Input()],  # match against any field?
                          [pg.Text(
                              'guys which one should we use for filters???', text_color='orange')],
                          [pg.Text(
                              'NOTE: incomplete and currently only showing filter for "Category".')],
                          [pg.Text('Category'), pg.Combo(
                              ['Lights', 'Locks'])],
                          [pg.Text('Category'), pg.OptionMenu(
                              ['Lights', 'Locks'])],
                          [pg.Button('Apply filters and search')]
                          ]
    # tab3 request/services
    cust_request_layout = [[pg.Text('request servicing for your purchased item here')]
                           # also show purchased items
                           ]
    # tab group
    cust_tabs = [[pg.TabGroup([[pg.Tab('Logout', cust_main_layout)],
                               [pg.Tab('Search', cust_search_layout)],
                               [pg.Tab('Request', cust_request_layout)]
                               ]
                              )]
                 ]

    cust_main_window = pg.Window(f"{CUSTOMER_NAME}'s session", cust_tabs)
    cust_main_event, cust_main_values = cust_main_window.read()
    if cust_main_event == 'Log Out':
        cust_main_window.close()
