import PySimpleGUI as sg

from app.constants import CUSTOMER_NAME
from app.database.setup import Products, Items


def customer_screen():
    # all the different tabs
    # tab1 main and logout
    main_layout = [[sg.Text(f'Welcome, {CUSTOMER_NAME}. Please click on the tabs to access other functions.')],
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

    search_layout = [[sg.Text('Search for an item:')],
                     [sg.Input()],  # match against any field?
                     [sg.Text(
                         'guys which one should we use for filters???', text_color='orange')],
                     [sg.Text(
                         'NOTE: incomplete and currently only showing filter for "Category".')],
                     [sg.Text('Category'), sg.Combo(
                         ['Lights', 'Locks'])],
                     [sg.Text('Category'), sg.OptionMenu(
                         ['Lights', 'Locks'])],
                     [sg.Button('Search!')]
                     ]
    # tab3 request/services
    request_layout = [[sg.Text('request servicing for your purchased item here')]
                      # also show purchased items
                      ]
    # tab group
    tabs = [[sg.TabGroup([[sg.Tab('Logout', main_layout)],
                          [sg.Tab('Search', search_layout)],
                          [sg.Tab('Request', request_layout)]
                          ]
                         )]
            ]

    window = sg.Window(f"{CUSTOMER_NAME}'s session", tabs)

    while True:
        event, values = window.read()
        if event in ('Log Out', sg.WIN_CLOSED):
            break

        elif event == "Search!":
            res = Items.find({"Model": "Light1"})
            for product in res:
                print(product)

    window.close()
