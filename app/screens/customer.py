import PySimpleGUI as sg

from app.constants import CUSTOMER_NAME
from app.database.setup import Products, Items
from app.database.utils import get_categories, get_models
from app.utils import setup_window, window_size

MODEL_OPTION = 'model_option'
CATEGORY_OPTION = 'category_option'
SEARCH_BUTTON = 'search_button'
MODEL_RADIO = 'model_radio'
CATEGORY_RADIO = 'category_radio'
COLOR_CHECKBOX = 'color_checkbox'
FACTORY_CHECKBOX = 'factory_checkbox'
POWER_SUPPLY_CHECKBOX = 'power_supply_checkbox'
PURCHASE_STATUS_CHECKBOX = 'purchase_status_checkbox'
PRODUCTION_YEAR_CHECKBOX = 'production_year_checkbox'
SERVICE_STATUS_CHECKBOX = 'service_status_checkbox'


def customer_screen():
    # all the different tab_layout
    # tab1 main and logout
    main_layout = [[sg.Text(f'Welcome, {CUSTOMER_NAME}. Please click on the tabs to access other functions.')],
                   [sg.Button('Log Out')]
                   ]
    # tab2 search & purchase
    # filters in the dropdown menu; filter by item attributes
    attributes = ['Color',
                  'Factory',
                  'PowerSupply',
                  'PurchaseStatus',
                  'ProductionYear',
                  'ServiceStatus']

    categories = get_categories()
    category_row = [sg.Radio('Category', CATEGORY_RADIO, default=True, enable_events=True, key=CATEGORY_RADIO, size=10),
                    sg.OptionMenu(categories, default_value=categories[0], disabled=False, key=CATEGORY_OPTION,
                                  size=10)]

    models = get_models()
    model_row = [sg.Radio('Model', MODEL_RADIO, default=False, enable_events=True, key=MODEL_RADIO, size=10),
                 sg.OptionMenu(models, default_value=models[0], disabled=True, key=MODEL_OPTION, size=10)]

    filter_row = [sg.Checkbox('Color', key=COLOR_CHECKBOX),
                  sg.Checkbox('Factory', key=FACTORY_CHECKBOX),
                  sg.Checkbox('Power Supply', key=POWER_SUPPLY_CHECKBOX),
                  sg.Checkbox('Purchase Status', key=PURCHASE_STATUS_CHECKBOX),
                  sg.Checkbox('Production Year', key=PRODUCTION_YEAR_CHECKBOX),
                  sg.Checkbox('Service Status', key=SERVICE_STATUS_CHECKBOX)
                  ]

    search_layout = [[sg.Text('Search by:')],
                     category_row,
                     model_row,
                     [sg.Text('Filters:')],
                     filter_row,
                     [sg.Button('Search', key=SEARCH_BUTTON)]
                     ]
    # tab3 request/services
    request_layout = [[sg.Text('request servicing for your purchased item here')]
                      # also show purchased items
                      ]
    # tab group
    tab_layout = [[sg.TabGroup([[sg.Tab('Logout', main_layout)],
                                [sg.Tab('Search', search_layout)],
                                [sg.Tab('Request', request_layout)]
                                ], size=window_size
                               )]
                  ]

    window = setup_window(f"{CUSTOMER_NAME}'s session", tab_layout)

    while True:
        event, values = window.read()
        if event in ('Log Out', sg.WIN_CLOSED):
            break

        elif event == CATEGORY_RADIO:
            window[MODEL_RADIO].update(value=False)
            window[MODEL_OPTION].update(disabled=True)
            window[CATEGORY_OPTION].update(disabled=False)

        elif event == MODEL_RADIO:
            window[CATEGORY_RADIO].update(value=False)
            window[MODEL_OPTION].update(disabled=False)
            window[CATEGORY_OPTION].update(disabled=True)

        elif event == SEARCH_BUTTON:
            res = Items.find({"Model": "Light1"})
            for product in res:
                print(product)

    window.close()
