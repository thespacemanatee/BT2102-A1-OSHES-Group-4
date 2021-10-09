import PySimpleGUI as sg

from app.auth import get_current_user
from app.components.category_component import category_component, CATEGORY_RADIO, CATEGORY_OPTION
from app.components.color_component import colors_filter_component, COLOR_CHECKBOX_VAL, COLOR_CHECKBOX
from app.components.factory_component import factories_filter_component, FACTORY_CHECKBOX_VAL, FACTORY_CHECKBOX
from app.components.item_search_component import item_search_component, ITEM_SEARCH_VAL, ITEM_SEARCH_RADIO
from app.components.item_summary_popup import item_summary_popup
from app.components.model_component import model_component, MODEL_RADIO
from app.components.power_supplies_component import power_supplies_filter_component, POWER_SUPPLY_CHECKBOX_VAL, \
    POWER_SUPPLY_CHECKBOX
from app.components.production_years_filter_component import production_years_filter_component, \
    PRODUCTION_YEARS_CHECKBOX_VAL, PRODUCTION_YEAR_CHECKBOX
from app.components.search_table_component import search_table_component, SEARCH_TABLE
from app.database.utils import get_categories, get_models, get_colors, get_factories, get_power_supplies, \
    get_production_years, get_filtered_results, find_item_by_id
from app.screens.customer.cust_dashboard import SEARCH_BUTTON
from app.utils import setup_window

RESET_BUTTON = 'reset_button'
MODEL_OPTION = 'model_option'

TABLE_HEADERS = [
    'PID',
    'Category',
    'Model',
    'Cost ($)',
    'Price ($)',
    'Warranty (months)',
    'Stock',
    'Sold'
]


def search_tab_screen(table_data):
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

    table_layout = search_table_component(table_data, TABLE_HEADERS, [5, 15, 15, 10, 10, 15, 10, 10])

    return [[sg.Text('Search by:', font=('Arial', 24), pad=(0, 0))],
            category_row,
            model_row,
            item_search_component(),
            [sg.Text('Filters:', font=('Arial', 24), pad=(0, 10))],
            [colors_filter_row, factories_filter_row],
            [power_supplies_filter_row, production_years_filter_row],
            [sg.Button('Search', key=SEARCH_BUTTON, size=10, pad=(5, 25)),
             sg.Button('Reset', key=RESET_BUTTON, size=10, pad=(5, 25))],
            table_layout
            ]


def administrator_screen():
    user = get_current_user()
    table_data, item_data = get_filtered_results(admin=True)
    is_after_reset = True

    def _get_filtered_results():
        nonlocal is_after_reset
        if is_after_reset:
            return get_filtered_results(admin=True)

        else:
            category = values[CATEGORY_OPTION] if values[CATEGORY_RADIO] else None
            model = values[MODEL_OPTION] if values[MODEL_RADIO] else None
            color = values[COLOR_CHECKBOX_VAL] if values[COLOR_CHECKBOX] else None
            factory = values[FACTORY_CHECKBOX_VAL] if values[FACTORY_CHECKBOX] else None
            power_supply = values[POWER_SUPPLY_CHECKBOX_VAL] if values[POWER_SUPPLY_CHECKBOX] else None
            production_year = values[PRODUCTION_YEARS_CHECKBOX_VAL] if values[PRODUCTION_YEAR_CHECKBOX] else None
            return get_filtered_results(admin=True, category=category, model=model, color=color, factory=factory,
                                        power_supply=power_supply, production_year=production_year)

    search_layout = search_tab_screen(table_data)

    request_layout = [[sg.Text('request servicing for your purchased item here')]]

    logout_layout = [[
        sg.Text(f'Welcome, {user.name}.', font=('Arial', 24)),
        sg.Button('Log Out'),
    ]]

    tab_layout = [[
        logout_layout,
        sg.TabGroup([
            [sg.Tab('        Search        ', [[sg.Column(search_layout, pad=25)]])],
            [sg.Tab('        Request       ', [[sg.Column(request_layout, pad=25)]])],
        ])]
    ]

    window = setup_window(f"{user.name}'s Session", tab_layout)

    while True:
        event, values = window.read()
        if event in ('Log Out', sg.WIN_CLOSED):
            break

        elif event == CATEGORY_RADIO:
            window[MODEL_RADIO].update(value=False)
            window[ITEM_SEARCH_RADIO].update(value=False)
            window[MODEL_OPTION].update(disabled=True)
            window[ITEM_SEARCH_VAL].update(disabled=True)
            window[CATEGORY_OPTION].update(disabled=False)

        elif event == MODEL_RADIO:
            window[CATEGORY_RADIO].update(value=False)
            window[ITEM_SEARCH_RADIO].update(value=False)
            window[MODEL_OPTION].update(disabled=False)
            window[ITEM_SEARCH_VAL].update(disabled=True)
            window[CATEGORY_OPTION].update(disabled=True)

        elif event == ITEM_SEARCH_RADIO:
            window[MODEL_RADIO].update(value=False)
            window[CATEGORY_RADIO].update(value=False)
            window[MODEL_OPTION].update(disabled=True)
            window[ITEM_SEARCH_VAL].update(disabled=False)
            window[CATEGORY_OPTION].update(disabled=True)

        elif event == SEARCH_BUTTON:
            is_after_reset = False
            if values[ITEM_SEARCH_RADIO]:
                user_input = values[ITEM_SEARCH_VAL]
                res = find_item_by_id(user_input)
                item_summary_popup(user_input, res)

            else:
                table_data, item_data = _get_filtered_results()
                window[SEARCH_TABLE].update(values=table_data)

        elif event == RESET_BUTTON:
            is_after_reset = True
            table_data, item_data = get_filtered_results(admin=True)
            window[SEARCH_TABLE].update(values=table_data)

    window.close()
