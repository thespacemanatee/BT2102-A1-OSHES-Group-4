import PySimpleGUI as sg

from app.components.category_component import category_component
from app.components.color_component import colors_filter_component
from app.components.factory_component import factories_filter_component
from app.components.item_search_component import item_search_component
from app.components.model_component import model_component
from app.components.power_supplies_component import power_supplies_filter_component
from app.components.price_filter_component import price_filter_component
from app.components.production_years_filter_component import production_years_filter_component
from app.components.search_table_component import search_table_component
from app.database.utils import get_categories, get_models, get_colors, get_factories, get_power_supplies, \
    get_production_years

WRONG_ENTRY = 'wrong_entry'
RESET_BUTTON = 'reset_button'
SEARCH_BUTTON = 'search_button'


def search_tab_screen(table_data, table_headers, col_widths, admin=False):
    categories = get_categories()
    cat = categories if len(categories) > 0 else ['Null']
    category_row = category_component(cat)

    models = get_models()
    mod = models if len(models) > 0 else ['Null']
    model_row = model_component(mod)

    price_filter_row = price_filter_component()

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

    table_layout = search_table_component(table_data, table_headers, col_widths)

    return [[sg.Text('Search by:', font=('Arial', 20), pad=(0, 0))],
            category_row,
            model_row,
            item_search_component() if admin else [],
            [sg.Text('Filters:', font=('Arial', 20), pad=(0, 10))],
            [price_filter_row, colors_filter_row, factories_filter_row],
            [power_supplies_filter_row, production_years_filter_row],
            [sg.Button('Search', key=SEARCH_BUTTON, size=10, pad=((5, 5), (25, 0))),
             sg.Button('Reset', key=RESET_BUTTON, size=10, pad=((5, 5), (25, 0)))],
            [sg.Text('', key=WRONG_ENTRY, pad=((5, 5), (0, 25)))],
            [sg.Text('Click on a product to view available items.')] if not admin else [],
            table_layout
            ]
