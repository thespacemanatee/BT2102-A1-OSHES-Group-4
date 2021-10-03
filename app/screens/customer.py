import PySimpleGUI as sg

from constants import CUSTOMER_NAME


def customer_screen():
    # all the different tabs
    # tab1 main and logout
    cust_main_layout = [[sg.Text(f'Welcome, {CUSTOMER_NAME}. Please click on the tabs to access other functions.')],
                        [sg.Button('Log Out')]
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

    cust_search_layout = [[sg.Text('Search for an item:')],
                          [sg.Input()],  # match against any field?
                          [sg.Text(
                              'guys which one should we use for filters???', text_color='orange')],
                          [sg.Text(
                              'NOTE: incomplete and currently only showing filter for "Category".')],
                          [sg.Text('Category'), sg.Combo(
                              ['Lights', 'Locks'])],
                          [sg.Text('Category'), sg.OptionMenu(
                              ['Lights', 'Locks'])],
                          [sg.Button('Apply filters and search')]
                          ]
    # tab3 request/services
    cust_request_layout = [[sg.Text('request servicing for your purchased item here')]
                           # also show purchased items
                           ]
    # tab group
    cust_tabs = [[sg.TabGroup([[sg.Tab('Logout', cust_main_layout)],
                               [sg.Tab('Search', cust_search_layout)],
                               [sg.Tab('Request', cust_request_layout)]
                               ]
                              )]
                 ]

    cust_main_window = sg.Window(f"{CUSTOMER_NAME}'s session", cust_tabs)
    cust_main_event, cust_main_values = cust_main_window.read()
    if cust_main_event == 'Log Out':
        cust_main_window.close()
