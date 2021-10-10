import copy

import PySimpleGUI as sg

from app.components.base_table_component import base_table_component
from app.components.centered_component import centered_component
from app.components.item_purchase_popup import item_purchase_popup
from app.database.utils import find_product_by_category_and_model, get_stock_levels
from app.utils import setup_window

PURCHASE_TABLE = 'purchase_table'
PURCHASE_TABLE_HEADERS = ['Category', 'Model', 'Color', 'Factory', 'Power Supply', 'Production Year', 'Stock']


def setup_purchase_table(item_list):
    item_list_copy = copy.deepcopy(item_list)
    for item in item_list_copy:
        item.pop('Stock', None)
    counts = get_stock_levels(item_list_copy)
    for j in range(len(item_list_copy)):
        item_list_copy[j]['Stock'] = counts[j]
    return item_list_copy, [list(item.values()) for item in item_list_copy]


def item_purchase_window(item_list, callbacks=None):
    if callbacks is None:
        callbacks = []
    item_list, table_data = setup_purchase_table(item_list)
    product = find_product_by_category_and_model(item_list[0]['Category'], item_list[0]['Model'])

    def update_stock_levels():
        nonlocal item_list, table_data
        item_list, table_data = setup_purchase_table(item_list)
        window[PURCHASE_TABLE].update(values=table_data)

    layout = centered_component(
        top_children=[
            [sg.Text('Click on an item to purchase.')],
            [base_table_component(values=table_data, headings=PURCHASE_TABLE_HEADERS,
                                  key=PURCHASE_TABLE,
                                  auto_size_columns=True,
                                  num_rows=10,
                                  tooltip='Item List',
                                  pad=(10, 10)
                                  )]
        ], centered_children=[sg.Button('Done', size=10)])

    window = setup_window('Purchase an Item', layout, keep_on_top=True)

    while True:
        event, values = window.read()
        if event in ('Done', sg.WIN_CLOSED):
            break

        if event == PURCHASE_TABLE:
            try:
                item = item_list[values[PURCHASE_TABLE][0]]
                callbacks.append(update_stock_levels)
                item_purchase_popup(product, item, callbacks=callbacks)
            except IndexError:
                continue

    window.close()
