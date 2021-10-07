import PySimpleGUI as sg

from app.auth import get_current_user
from app.components.centered_component import centered_component, COLUMN, EXPAND_1, EXPAND_2
from app.components.color_component import colors_filter_component, COLOR_CHECKBOX_VAL, COLOR_CHECKBOX
from app.components.factory_component import factories_filter_component, FACTORY_CHECKBOX_VAL, FACTORY_CHECKBOX
from app.components.model_component import model_component, MODEL_RADIO, MODEL_OPTION
from app.components.power_supplies_component import power_supplies_filter_component, POWER_SUPPLY_CHECKBOX_VAL, \
    POWER_SUPPLY_CHECKBOX
from app.components.production_years_filter_component import production_years_filter_component, \
    PRODUCTION_YEARS_CHECKBOX_VAL, PRODUCTION_YEAR_CHECKBOX
from app.components.search_table_component import search_table_component, SEARCH_TABLE
from app.database.utils import get_categories, get_models, get_colors, get_factories, get_power_supplies, \
    get_production_years, get_filtered_results, find_product_by_category_and_model, purchase_item
from app.utils import setup_window
from app.components.category_component import category_component, CATEGORY_RADIO, CATEGORY_OPTION

RESET_BUTTON = 'reset_button'
SEARCH_BUTTON = 'search_button'
PURCHASE_TABLE = 'purchase_table'

SEARCH_TABLE_HEADERS = [
    'IID',
    'Category',
    'Model',
    'Price ($)',
    'Warranty (months)',
    'Stock'
]
PURCHASE_TABLE_HEADERS = ['IID', 'Category', 'Model', 'Color', 'Factory', 'Power Supply', 'Production Year']


def item_purchase_popup(purchase_window, product, item, update_search_table):
    user = get_current_user()
    layout = centered_component(top_children=[
        sg.Column([
            [sg.Text('Item ID:')],
            [sg.Text('Category:')],
            [sg.Text('Model:')],
            [sg.Text('Color:')],
            [sg.Text('Factory:')],
            [sg.Text('Power Supply:')],
            [sg.Text('Production Year:')],
            [sg.Text('Price ($):')],
            [sg.Text('Warranty (months)')],
        ],
            pad=20
        ), sg.Column([
            [sg.Text(item["ItemID"])],
            [sg.Text(product["Category"])],
            [sg.Text(product["Model"])],
            [sg.Text(item["Color"])],
            [sg.Text(item["Factory"])],
            [sg.Text(item["PowerSupply"])],
            [sg.Text(item["ProductionYear"])],
            [sg.Text(product["Price ($)"])],
            [sg.Text(product["Warranty (months)"])],
        ],
            element_justification='right',
            pad=20
        )
    ], centered_children=[sg.Button('Purchase', s=10), sg.Button('Cancel', s=10)])

    popup = setup_window(f'Item ID: {item["ItemID"]}', layout, keep_on_top=True)
    popup[COLUMN].expand(True, True, True)
    popup[EXPAND_1].expand(True, True, True)
    popup[EXPAND_2].expand(True, False, True)

    while True:
        event, values = popup.read()
        if event in ('Cancel', sg.WIN_CLOSED):
            break

        elif event == 'Purchase':
            purchase_item(user.id, item["ItemID"])
            update_search_table()
            popup.close()
            purchase_window.close()
            break

    popup.close()


def item_purchase_window(item_list, update_search_table):
    product = find_product_by_category_and_model(item_list[0]['Category'], item_list[0]['Model'])
    table_data = [list(item.values()) for item in item_list]
    layout = [[
        sg.Table(values=table_data, headings=PURCHASE_TABLE_HEADERS,
                 auto_size_columns=True,
                 justification='right',
                 num_rows=10,
                 alternating_row_color='lightyellow',
                 key=PURCHASE_TABLE,
                 row_height=35,
                 tooltip='Item List',
                 enable_events=True
                 )
    ]]

    window = setup_window(f"Purchase Product: {product['Category']}, Model: {product['Model']}", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == PURCHASE_TABLE:
            item = item_list[values[PURCHASE_TABLE][0]]
            item_purchase_popup(window, product, item, update_search_table)


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

    table_layout = search_table_component(table_data, SEARCH_TABLE_HEADERS)

    return [[sg.Text('Search by:', font=('Arial', 24), pad=(0, 10))],
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


def customer_screen():
    user = get_current_user()
    table_data, item_data = get_filtered_results()

    def update_search_table():
        nonlocal table_data, item_data
        table_data, item_data = get_filtered_results()
        window[SEARCH_TABLE].update(values=table_data)

    main_layout = [[sg.Text(f'Welcome, {user.name}.', font=('Arial', 32))]]

    search_layout = search_tab_screen(table_data)

    request_layout = [[sg.Text('request servicing for your purchased item here')]]

    logout_layout = [
        sg.Column([[sg.Text('', pad=(0, 0), key='-EXPAND-'), sg.Button('Log Out')]], justification='right')]

    tab_layout = [[sg.TabGroup([[sg.Tab('        Home        ', [[sg.Column(main_layout, pad=25)]])],
                                [sg.Tab('        Search        ', [[sg.Column(search_layout, pad=25)]])],
                                [sg.Tab('        Request       ', [[sg.Column(request_layout, pad=25)]])],
                                logout_layout,
                                ])]
                  ]

    window = setup_window(f"{user.name}'s Session", tab_layout)
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
            table_data, item_data = get_filtered_results(category=category, model=model, color=color, factory=factory,
                                                         power_supply=power_supply, production_year=production_year)
            window[SEARCH_TABLE].update(values=table_data)

        elif event == RESET_BUTTON:
            table_data, item_data = get_filtered_results()
            window[SEARCH_TABLE].update(values=table_data)

        elif event == SEARCH_TABLE:
            item_list = item_data[values[SEARCH_TABLE][0]]
            item_purchase_window(item_list, update_search_table)

    window.close()
