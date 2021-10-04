import PySimpleGUI as sg

from app.constants import CUSTOMER_NAME
from app.database.utils import get_categories, get_models, get_colors, get_factories, get_power_supplies, \
    get_production_years, get_filtered_results
from app.utils import setup_window, window_size

RESET_BUTTON = 'reset_button'
MODEL_OPTION = 'model_option'
CATEGORY_OPTION = 'category_option'
SEARCH_BUTTON = 'search_button'
MODEL_RADIO = 'model_radio'
CATEGORY_RADIO = 'category_radio'
COLOR_CHECKBOX = 'color_checkbox'
FACTORY_CHECKBOX = 'factory_checkbox'
POWER_SUPPLY_CHECKBOX = 'power_supply_checkbox'
PRODUCTION_YEAR_CHECKBOX = 'production_year_checkbox'
PRODUCTION_YEARS_CHECKBOX_VAL = 'production_years_checkbox_val'
POWER_SUPPLY_CHECKBOX_VAL = 'power_supply_checkbox_val'
FACTORY_CHECKBOX_VAL = 'factory_checkbox_val'
COLOR_CHECKBOX_VAL = 'color_checkbox_val'

table_headers = [
    'Category',
    'Model',
    'Price',
    'Warranty',
    'Stock'
]


def customer_screen():
    main_layout = [[sg.Text(f'Welcome, {CUSTOMER_NAME}.', font=('Arial', 32))]]

    categories = get_categories()
    cat = categories if len(categories) > 0 else ['Null']
    category_row = [sg.Radio('Category', CATEGORY_RADIO, default=True, enable_events=True, key=CATEGORY_RADIO, size=10),
                    sg.OptionMenu(cat, default_value=cat[0], disabled=False, key=CATEGORY_OPTION,
                                  size=10)]

    models = get_models()
    mod = models if len(models) > 0 else ['Null']
    model_row = [sg.Radio('Model', MODEL_RADIO, default=False, enable_events=True, key=MODEL_RADIO, size=10),
                 sg.OptionMenu(mod, default_value=mod[0], disabled=True, key=MODEL_OPTION, size=10)]

    colors = get_colors()
    col = categories if len(categories) > 0 else ['Null']
    colors_filter_row = sg.Column([[sg.Checkbox('Color', key=COLOR_CHECKBOX),
                                    sg.OptionMenu(col, default_value=col[0], key=COLOR_CHECKBOX_VAL)]])

    factories = get_factories()
    fac = factories if len(factories) > 0 else ['Null']
    factories_filter_row = sg.Column([[sg.Checkbox('Factory', key=FACTORY_CHECKBOX),
                                       sg.OptionMenu(fac, default_value=fac[0], key=FACTORY_CHECKBOX_VAL)]])
    
    power_supplies = get_power_supplies()
    pow_sup = power_supplies if len(power_supplies) > 0 else ['Null']
    power_supplies_filter_row = sg.Column([[sg.Checkbox('Power Supply', key=POWER_SUPPLY_CHECKBOX),
                                            sg.OptionMenu(pow_sup, default_value=pow_sup[0],
                                                          key=POWER_SUPPLY_CHECKBOX_VAL)]])

    production_years = get_production_years()
    prod = production_years if len(production_years) > 0 else ['Null']
    production_years_filter_row = sg.Column([[sg.Checkbox('Production Years', key=PRODUCTION_YEAR_CHECKBOX),
                                              sg.OptionMenu(prod, default_value=prod[0],
                                                            key=PRODUCTION_YEARS_CHECKBOX_VAL)]])

    table_layout = [sg.Table(values=get_filtered_results(), headings=table_headers,
                             auto_size_columns=False,
                             display_row_numbers=True,
                             justification='left',
                             num_rows=20,
                             alternating_row_color='lightyellow',
                             key='-TABLE-',
                             row_height=35,
                             col_widths=[19, 19, 19, 19, 19],
                             tooltip='Search Results',
                             enable_events=True)]

    search_layout = [[sg.Text('Search by:', font=('Arial', 24), pad=(0, 10))],
                     category_row,
                     model_row,
                     [sg.Text('Filters:', font=('Arial', 24), pad=(0, 10))],
                     [colors_filter_row, factories_filter_row, power_supplies_filter_row,
                      production_years_filter_row],
                     [sg.Column([[sg.Button('Search', key=SEARCH_BUTTON, size=25, pad=(10, 25)),
                                  sg.Button('Reset', key=RESET_BUTTON, size=25, pad=(10, 25))]], justification='center',
                                element_justification='center')],
                     table_layout
                     ]

    request_layout = [[sg.Text('request servicing for your purchased item here')]]

    logout_layout = [sg.Column([[sg.Text('', pad=(0, 0), key='-EXPAND-'), sg.Button('Log Out')]], justification='right')]
    
    tab_layout = [[sg.TabGroup([[sg.Tab('        Home        ', [[sg.Column(main_layout, pad=25)]])],
                                [sg.Tab('        Search        ', [[sg.Column(search_layout, pad=25)]])],
                                [sg.Tab('        Request       ', [[sg.Column(request_layout, pad=25)]])],
                                logout_layout,
                                ], size=window_size
                               )]
                  ]

    window = setup_window(f"{CUSTOMER_NAME}'s session", tab_layout)
    window['-EXPAND-'].expand(True, True, True)

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
            category = values[CATEGORY_OPTION] if values[CATEGORY_RADIO] else None
            model = values[MODEL_OPTION] if values[MODEL_RADIO] else None
            color = values[COLOR_CHECKBOX_VAL] if values[COLOR_CHECKBOX] else None
            factory = values[FACTORY_CHECKBOX_VAL] if values[FACTORY_CHECKBOX] else None
            power_supply = values[POWER_SUPPLY_CHECKBOX_VAL] if values[POWER_SUPPLY_CHECKBOX] else None
            production_year = values[PRODUCTION_YEARS_CHECKBOX_VAL] if values[PRODUCTION_YEAR_CHECKBOX] else None
            res = get_filtered_results(category=category, model=model, color=color, factory=factory,
                                       power_supply=power_supply, production_year=production_year)
            window['-TABLE-'].update(values=res)

        elif event == RESET_BUTTON:
            window['-TABLE-'].update(values=get_filtered_results())

    window.close()
