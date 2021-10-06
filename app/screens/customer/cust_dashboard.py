import PySimpleGUI as sg

from app.components.color_component import colors_filter_component, COLOR_CHECKBOX_VAL, COLOR_CHECKBOX
from app.components.factory_component import factories_filter_component, FACTORY_CHECKBOX_VAL, FACTORY_CHECKBOX
from app.components.model_component import model_component, MODEL_RADIO, MODEL_OPTION
from app.components.power_supplies_component import power_supplies_filter_component, POWER_SUPPLY_CHECKBOX_VAL, \
    POWER_SUPPLY_CHECKBOX
from app.components.production_years_filter_component import production_years_filter_component, \
    PRODUCTION_YEARS_CHECKBOX_VAL, PRODUCTION_YEAR_CHECKBOX
from app.components.search_table_component import search_table_component, SEARCH_TABLE
from app.constants import CUSTOMER_NAME
from app.database.utils import get_categories, get_models, get_colors, get_factories, get_power_supplies, \
    get_production_years, get_filtered_results
from app.utils import setup_window
from app.components.category_component import category_component, CATEGORY_RADIO, CATEGORY_OPTION

RESET_BUTTON = 'reset_button'
SEARCH_BUTTON = 'search_button'

TABLE_HEADERS = [
    'Category',
    'Model',
    'Price ($)',
    'Warranty (months)',
    'Stock'
]


def customer_screen():
    main_layout = [[sg.Text(f'Welcome, {CUSTOMER_NAME}.', font=('Arial', 32))]]

    categories = get_categories()
    cat = categories if len(categories) > 0 else ['Null']
    category_row = category_component(cat)

    models = get_models()
    mod = models if len(models) > 0 else ['Null']
    model_row = model_component(mod)

    colors = get_colors()
    col = colors if len(colors) > 0 else ['Null']
    colors_filter_row = colors_filter_component(col)

    factories = get_factories()
    fac = factories if len(factories) > 0 else ['Null']
    factories_filter_row = factories_filter_component(fac)

    power_supplies = get_power_supplies()
    pow_sup = power_supplies if len(power_supplies) > 0 else ['Null']
    power_supplies_filter_row = power_supplies_filter_component(pow_sup)

    production_years = get_production_years()
    prod = production_years if len(production_years) > 0 else ['Null']
    production_years_filter_row = production_years_filter_component(prod)

    table_data = get_filtered_results()
    table_layout = search_table_component(table_data, TABLE_HEADERS)

    search_layout = [[sg.Text('Search by:', font=('Arial', 24), pad=(0, 10))],
                     category_row,
                     model_row,
                     [sg.Text('Filters:', font=('Arial', 24), pad=(0, 10))],
                     [colors_filter_row, factories_filter_row],
                     [power_supplies_filter_row, production_years_filter_row],
                     [sg.Column([[sg.Button('Search', key=SEARCH_BUTTON, size=25, pad=(10, 25)),
                                  sg.Button('Reset', key=RESET_BUTTON, size=25, pad=(10, 25))]], justification='center',
                                element_justification='center')],
                     table_layout
                     ]

    request_layout = [[sg.Text('request servicing for your purchased item here')]]

    logout_layout = [
        sg.Column([[sg.Text('', pad=(0, 0), key='-EXPAND-'), sg.Button('Log Out')]], justification='right')]

    tab_layout = [[sg.TabGroup([[sg.Tab('        Home        ', [[sg.Column(main_layout, pad=25)]])],
                                [sg.Tab('        Search        ', [[sg.Column(search_layout, pad=25)]])],
                                [sg.Tab('        Request       ', [[sg.Column(request_layout, pad=25)]])],
                                logout_layout,
                                ])]
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
            window[SEARCH_TABLE].update(values=res)

        elif event == RESET_BUTTON:
            window[SEARCH_TABLE].update(values=get_filtered_results())

    window.close()
