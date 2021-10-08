import PySimpleGUI as sg
import copy

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
    get_production_years, get_filtered_results, find_product_by_category_and_model, purchase_item, get_stock_levels, \
    get_purchase_history, get_item_information
from app.utils import setup_window
from app.components.category_component import category_component, CATEGORY_RADIO, CATEGORY_OPTION

HISTORY_TABLE_GROUP = 'history_table_group'

NO_PAST_PURCHASE_TEXT = 'NO_PAST_PURCHASE_TEXT'
ITEM_ID_TEXT = 'item_id_text'
ITEM_CATEGORY_TEXT = 'item_category_text'
ITEM_MODEL_TEXT = 'item_model_text'
ITEM_PRICE_TEXT = 'item_price_text'
ITEM_COLOR_TEXT = 'item_color_text'
ITEM_POWER_SUPPLY_TEXT = 'item_power_supply_text'
ITEM_FACTORY_TEXT = 'item_factory_text'
ITEM_PRODUCTION_YEAR_TEXT = 'item_production_year_text'
ITEM_WARRANTY_TEXT = 'item_warranty_text'
ITEM_SERVICE_STATUS_TEXT = 'item_service_status_text'
ITEM_SERVICED_BY_TEXT = 'item_serviced_by_text'
ITEM_PURCHASE_DATE_TEXT = 'item_purchase_date_text'

HISTORY_TABLE_VALUE = 'history_table_value'
HISTORY_TABLE_KEY = 'history_table_key'
HISTORY_ITEM_TITLE_TEXT = 'history_item_title_text'
HISTORY_ITEM_DETAILS_COLUMN = 'history_item_details_column'
WRONG_ENTRY = 'wrong_entry'
QUANTITY_VAL = 'quantity_val'
RESET_BUTTON = 'reset_button'
SEARCH_BUTTON = 'search_button'
PURCHASE_TABLE = 'purchase_table'
HISTORY_TABLE = 'history_table'

SEARCH_TABLE_HEADERS = [
    'Product ID',
    'Category',
    'Model',
    'Price ($)',
    'Warranty (months)',
    'Stock'
]
PURCHASE_TABLE_HEADERS = ['Category', 'Model', 'Color', 'Factory', 'Power Supply', 'Production Year', 'Stock']
HISTORY_TABLE_HEADERS = ['Item ID', 'Model', 'Purchase Date', 'Service Status']


def purchase_history_tab_screen(history):
    table_data = [list(item.values()) for item in history]
    table_data = table_data if len(table_data) > 0 else [['' for item in HISTORY_TABLE_HEADERS]]

    return [
        [sg.Text('You have no past purchases.', key=NO_PAST_PURCHASE_TEXT, visible=(not len(history) > 0))],
        [
            sg.Column([
                [sg.Text('No item selected.' + ' ' * 30, key=HISTORY_ITEM_TITLE_TEXT,
                         pad=((5, 0), (5, 20)))],
                [sg.Column([
                    [sg.Text('Item ID:')],
                    [sg.Text('Category:')],
                    [sg.Text('Model:')],
                    [sg.Text('Price ($):')],
                    [sg.Text('Color:')],
                    [sg.Text('Power Supply:')],
                    [sg.Text('Factory:')],
                    [sg.Text('Production Year:')],
                    [sg.Text('Warranty (months)')],
                    [sg.Text('Service Status:')],
                    [sg.Text('Serviced By:')],
                    [sg.Text('Purchase Date:')],
                ], key=HISTORY_TABLE_KEY, pad=((0, 10), (0, 0))),
                    sg.Column([
                        [sg.Text('', key=ITEM_ID_TEXT)],
                        [sg.Text('', key=ITEM_CATEGORY_TEXT)],
                        [sg.Text('', key=ITEM_MODEL_TEXT)],
                        [sg.Text('', key=ITEM_PRICE_TEXT)],
                        [sg.Text('', key=ITEM_COLOR_TEXT)],
                        [sg.Text('', key=ITEM_POWER_SUPPLY_TEXT)],
                        [sg.Text('', key=ITEM_FACTORY_TEXT)],
                        [sg.Text('', key=ITEM_PRODUCTION_YEAR_TEXT)],
                        [sg.Text('', key=ITEM_WARRANTY_TEXT)],
                        [sg.Text('', key=ITEM_SERVICE_STATUS_TEXT)],
                        [sg.Text('', key=ITEM_SERVICED_BY_TEXT)],
                        [sg.Text('', key=ITEM_PURCHASE_DATE_TEXT)],
                    ], element_justification='right', visible=False, key=HISTORY_TABLE_VALUE, expand_x=True),
                ],
            ], expand_y=True, expand_x=True, key=HISTORY_ITEM_DETAILS_COLUMN, pad=((10, 0), (0, 0))),
            sg.Column([
                [sg.Text('Click on an item to view details.')],
                [sg.Table(values=table_data, headings=HISTORY_TABLE_HEADERS,
                          justification='right',
                          num_rows=18,
                          alternating_row_color='lightyellow',
                          key=HISTORY_TABLE,
                          row_height=35,
                          tooltip='Purchase History',
                          enable_events=True),
                 ]
            ], key=HISTORY_TABLE_GROUP)
        ],
    ]


def item_purchase_popup(product, item, update_search_table, update_stock_levels, update_purchase_history):
    user = get_current_user()
    layout = centered_component(top_children=[
        sg.Column([
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
    ], centered_children=[sg.Column([[sg.Text(f'Quantity: ({item["Stock"]} left)'), sg.Input(k=QUANTITY_VAL, s=9)],
                                     [sg.Text(k=WRONG_ENTRY)],
                                     [sg.Column([[
                                         sg.Button('Purchase', s=10), sg.Button('Cancel', s=10)]
                                     ])]
                                     ]),
                          ])

    popup = setup_window('Confirm Purchase', layout, keep_on_top=True)
    popup[COLUMN].expand(True, True, True)
    popup[EXPAND_1].expand(True, True, True)
    popup[EXPAND_2].expand(True, False, True)

    while True:
        event, values = popup.read()
        if event in ('Cancel', sg.WIN_CLOSED):
            break

        elif event == 'Purchase':
            try:
                quantity = int(values[QUANTITY_VAL])
                if quantity > item['Stock']:
                    popup[WRONG_ENTRY].update('Quantity exceeded.', text_color='red')

                else:
                    purchase_item(user.id, {
                        'Category': item['Category'],
                        'Model': item['Model'],
                        'Color': item['Color'],
                        'Factory': item['Factory'],
                        'PowerSupply': item['PowerSupply'],
                        'ProductionYear': item['ProductionYear'],
                    }, int(values[QUANTITY_VAL]))
                    update_search_table()
                    update_stock_levels()
                    update_purchase_history()
                    popup.close()
                    break
            except ValueError:
                popup[WRONG_ENTRY].update('Please enter a number.', text_color='red')

    popup.close()


def setup_purchase_table(item_list):
    item_list_copy = copy.deepcopy(item_list)
    counts = get_stock_levels(item_list_copy)
    for j in range(len(item_list_copy)):
        item_list_copy[j]['Stock'] = counts[j]
    return item_list_copy, [list(item.values()) for item in item_list_copy]


def item_purchase_window(item_list, update_search_table, update_purchase_history):
    item_list_copy, table_data = setup_purchase_table(item_list)
    product = find_product_by_category_and_model(item_list[0]['Category'], item_list[0]['Model'])

    def update_stock_levels():
        nonlocal item_list_copy, table_data
        item_list_copy, table_data = setup_purchase_table(item_list)
        window[PURCHASE_TABLE].update(values=table_data)

    layout = centered_component(
        top_children=[[sg.Text(f"Product: {product['Category']}; Model: {product['Model']}")],
                      [sg.Text('Click on an item to purchase.')],
                      [sg.Table(values=table_data, headings=PURCHASE_TABLE_HEADERS,
                                justification='right',
                                num_rows=10,
                                alternating_row_color='lightyellow',
                                key=PURCHASE_TABLE,
                                row_height=35,
                                tooltip='Item List',
                                enable_events=True,
                                pad=(10, 10)
                                )]
                      ], centered_children=[sg.Button('Done', size=10)])

    window = setup_window('Purchase an Item', layout)

    while True:
        event, values = window.read()
        if event in ('Done', sg.WIN_CLOSED):
            break

        if event == PURCHASE_TABLE:
            try:
                item = item_list_copy[values[PURCHASE_TABLE][0]]
                item_purchase_popup(product, item, update_search_table, update_stock_levels, update_purchase_history)
            except IndexError:
                continue

    window.close()


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
            [sg.Button('Search', key=SEARCH_BUTTON, size=10, pad=(5, 25)),
             sg.Button('Reset', key=RESET_BUTTON, size=10, pad=(5, 25))],
            [sg.Text('Click on a product to view available items.')],
            table_layout
            ]


def customer_screen():
    user = get_current_user()
    table_data, item_data = get_filtered_results()
    history = get_purchase_history(user.id)
    is_after_reset = True

    def _get_filtered_results():
        nonlocal is_after_reset
        if is_after_reset:
            return get_filtered_results()

        else:
            category = values[CATEGORY_OPTION] if values[CATEGORY_RADIO] else None
            model = values[MODEL_OPTION] if values[MODEL_RADIO] else None
            color = values[COLOR_CHECKBOX_VAL] if values[COLOR_CHECKBOX] else None
            factory = values[FACTORY_CHECKBOX_VAL] if values[FACTORY_CHECKBOX] else None
            power_supply = values[POWER_SUPPLY_CHECKBOX_VAL] if values[POWER_SUPPLY_CHECKBOX] else None
            production_year = values[PRODUCTION_YEARS_CHECKBOX_VAL] if values[PRODUCTION_YEAR_CHECKBOX] else None
            return get_filtered_results(category=category, model=model, color=color, factory=factory,
                                        power_supply=power_supply, production_year=production_year)

    def update_search_table():
        nonlocal table_data, item_data
        table_data, item_data = _get_filtered_results()
        window[SEARCH_TABLE].update(values=table_data)

    def update_purchase_history():
        nonlocal history
        history = get_purchase_history(user.id)
        window[NO_PAST_PURCHASE_TEXT].update(visible=False)
        window[HISTORY_TABLE].update(values=[list(item1.values()) for item1 in history], visible=True)

    search_layout = search_tab_screen(table_data)

    request_layout = purchase_history_tab_screen(history)

    logout_layout = [[
        sg.Column([
            [sg.Text(' ' * 460, font=('Arial', 1))],
            [sg.Text(f'Welcome, {user.name}.', font=('Arial', 24))],
        ], element_justification='left'),
        sg.Column([
            [sg.Text(' ' * 460, font=('Arial', 1))],
            [sg.Button('Log Out')]
        ], element_justification='right'),
    ]]

    tab_layout = [[
        logout_layout,
        sg.TabGroup([
            [sg.Tab('        Search        ', [[sg.Column(search_layout, pad=25)]])],
            [sg.Tab('   Purchase History   ', [[sg.Column(request_layout, pad=25)]])],
        ])]
    ]

    window = setup_window(f"{user.name}'s Session", tab_layout)

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
            is_after_reset = False
            table_data, item_data = _get_filtered_results()
            window[SEARCH_TABLE].update(values=table_data)

        elif event == RESET_BUTTON:
            is_after_reset = True
            table_data, item_data = get_filtered_results()
            window[SEARCH_TABLE].update(values=table_data)

        elif event == SEARCH_TABLE:
            index = values[SEARCH_TABLE][0]
            item_list = item_data[index]
            if len(item_list) > 0:
                item_purchase_window(item_list, update_search_table, update_purchase_history)
            else:
                sg.popup(f'Product ID: {table_data[index][0]} is out of stock', custom_text="That's unfortunate...")

        elif event == HISTORY_TABLE:
            index = values[HISTORY_TABLE][0]
            item = history[index]
            item = get_item_information(item['id'])
            window[HISTORY_ITEM_TITLE_TEXT].update(visible=False)
            window[HISTORY_TABLE_KEY].update(visible=True)
            window[HISTORY_TABLE_VALUE].update(visible=True)
            window[ITEM_ID_TEXT].update(f'{item["id"]}')
            window[ITEM_CATEGORY_TEXT].update(f'{item["category"]}')
            window[ITEM_MODEL_TEXT].update(f'{item["model"]}')
            window[ITEM_PRICE_TEXT].update(f'{item["price"]}')
            window[ITEM_COLOR_TEXT].update(f'{item["colour"]}')
            window[ITEM_POWER_SUPPLY_TEXT].update(f'{item["power_supply"]}')
            window[ITEM_FACTORY_TEXT].update(f'{item["factory"]}')
            window[ITEM_PRODUCTION_YEAR_TEXT].update(f'{item["production_year"]}')
            window[ITEM_WARRANTY_TEXT].update(f'{item["warranty"]}')
            window[ITEM_SERVICE_STATUS_TEXT].update(f'{item["service_status"]}')
            window[ITEM_SERVICED_BY_TEXT].update(f'{item["name"]}')
            window[ITEM_PURCHASE_DATE_TEXT].update(f'{item["purchase_date"]}')

    window.close()
