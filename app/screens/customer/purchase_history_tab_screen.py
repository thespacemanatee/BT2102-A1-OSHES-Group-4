import PySimpleGUI as sg

from app.components.base_table_component import base_table_component

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
ITEM_PURCHASE_DATE_TEXT = 'item_purchase_date_text'

HISTORY_TABLE_VALUE = 'history_table_value'
HISTORY_ITEM_DETAILS_COLUMN = 'history_item_details_column'
HISTORY_TABLE = 'history_table'
HISTORY_TABLE_GROUP = 'history_table_group'
HISTORY_TABLE_HEADERS = ['IID', 'Category ', 'Model', 'Purchase Date']

REQUEST_SERVICING_BUTTON = 'request_servicing_button'


def purchase_history_tab_screen(history):
    table_data = [list(item.values()) for item in history]

    return [
        [sg.Column([
            [sg.Text('Click on an item to view details.')],
            [base_table_component(values=table_data, headings=HISTORY_TABLE_HEADERS,
                                  key=HISTORY_TABLE,
                                  col_widths=[5, 10, 10, 15],
                                  num_rows=17,
                                  tooltip='Purchase History',
                                  ),
             ]
        ], key=HISTORY_TABLE_GROUP),
            sg.Column([
                [sg.Text('')],
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
                    [sg.Text('Purchase Date:')],
                    [sg.Text(' ' * 42)],
                ], expand_y=True, pad=((0, 10), (0, 0))),
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
                        [sg.Text('', key=ITEM_PURCHASE_DATE_TEXT)],
                        [sg.Text(' ' * 42)],
                    ], element_justification='right', visible=False, key=HISTORY_TABLE_VALUE, expand_x=True,
                        expand_y=True),
                ],
                [sg.Button('Request for Servicing', expand_x=True, size=40, pad=(0, 20), visible=False,
                           key=REQUEST_SERVICING_BUTTON)],
            ], expand_y=True, expand_x=True, key=HISTORY_ITEM_DETAILS_COLUMN, pad=((10, 0), (0, 0))),

        ],
    ]
