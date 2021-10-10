import PySimpleGUI as sg

from app.auth import get_current_user
from app.components.category_component import CATEGORY_RADIO, CATEGORY_OPTION
from app.components.color_component import COLOR_CHECKBOX_VAL, COLOR_CHECKBOX
from app.components.factory_component import FACTORY_CHECKBOX_VAL, FACTORY_CHECKBOX
from app.components.item_purchase_window import item_purchase_window
from app.components.make_payment_popup import make_payment_popup
from app.components.model_component import MODEL_RADIO, MODEL_OPTION
from app.components.power_supplies_component import POWER_SUPPLY_CHECKBOX_VAL, \
    POWER_SUPPLY_CHECKBOX
from app.components.price_filter_component import PRICE_MIN_VAL, PRICE_MAX_VAL, PRICE_CHECKBOX
from app.components.production_years_filter_component import PRODUCTION_YEARS_CHECKBOX_VAL, PRODUCTION_YEAR_CHECKBOX
from app.components.request_servicing_popup import request_servicing_popup
from app.components.search_table_component import SEARCH_TABLE
from app.database.utils import get_filtered_results, get_purchase_history_by_id, get_item_information_by_id, \
    find_service_requests_by_id_and_status
from app.models.request import RequestStatus
from app.screens.commons.search_tab_screen import search_tab_screen, SEARCH_BUTTON, RESET_BUTTON, WRONG_ENTRY
from app.screens.customer.home_tab_screen import home_tab_screen, PENDING_REQUESTS_TABLE, SERVICE_REQUESTS_TABLE
from app.screens.customer.purchase_history_tab_screen import purchase_history_tab_screen, HISTORY_TABLE, \
    REQUEST_SERVICING_BUTTON, HISTORY_TABLE_VALUE, ITEM_ID_TEXT, ITEM_CATEGORY_TEXT, ITEM_MODEL_TEXT, \
    ITEM_PRICE_TEXT, ITEM_COLOR_TEXT, ITEM_POWER_SUPPLY_TEXT, ITEM_FACTORY_TEXT, ITEM_PRODUCTION_YEAR_TEXT, \
    ITEM_WARRANTY_TEXT, ITEM_SERVICE_STATUS_TEXT, ITEM_PURCHASE_DATE_TEXT
from app.utils import setup_window, get_requests_table_data

SEARCH_TABLE_COL_WIDTHS = [5, 15, 15, 10, 15, 10]
SEARCH_TABLE_HEADERS = [
    'PID',
    'Category',
    'Model',
    'Price ($)',
    'Warranty (months)',
    'Stock'
]


def get_service_requests_data():
    user_id = get_current_user().id
    payment_pending_requests = find_service_requests_by_id_and_status(user_id, (RequestStatus.WaitingForPayment.value,))
    service_requests = find_service_requests_by_id_and_status(user_id, (
        RequestStatus.Submitted.value, RequestStatus.InProgress.value, RequestStatus.Approved.value,
        RequestStatus.Canceled.value, RequestStatus.Completed.value))

    return payment_pending_requests, service_requests


def customer_screen():
    user = get_current_user()
    table_data, item_data = get_filtered_results()
    pending_table_data, requests_table_data = get_service_requests_data()
    history = get_purchase_history_by_id(user.id)
    is_after_reset = True

    def _get_filtered_results():
        nonlocal is_after_reset
        if is_after_reset:
            return get_filtered_results()

        else:
            try:
                category = values[CATEGORY_OPTION] if values[CATEGORY_RADIO] else None
                model = values[MODEL_OPTION] if values[MODEL_RADIO] else None
                price_min = int(values[PRICE_MIN_VAL]) if values[PRICE_CHECKBOX] else None
                price_max = int(values[PRICE_MAX_VAL]) if values[PRICE_CHECKBOX] else None
                color = values[COLOR_CHECKBOX_VAL] if values[COLOR_CHECKBOX] else None
                factory = values[FACTORY_CHECKBOX_VAL] if values[FACTORY_CHECKBOX] else None
                power_supply = values[POWER_SUPPLY_CHECKBOX_VAL] if values[POWER_SUPPLY_CHECKBOX] else None
                production_year = values[PRODUCTION_YEARS_CHECKBOX_VAL] if values[PRODUCTION_YEAR_CHECKBOX] else None
                return get_filtered_results(category=category, model=model, price_min=price_min,
                                            price_max=price_max, color=color, factory=factory,
                                            power_supply=power_supply, production_year=production_year)
            except ValueError:
                window[WRONG_ENTRY].update('Please specify a number for min and max price values.', text_color='red')

    def _update_search_table():
        nonlocal table_data, item_data
        table_data, item_data = _get_filtered_results()
        window[SEARCH_TABLE].update(values=table_data)

    def _update_purchase_history():
        nonlocal history
        history = get_purchase_history_by_id(user.id)
        window[REQUEST_SERVICING_BUTTON].update(visible=False)
        window[HISTORY_TABLE].update(values=[list(item1.values()) for item1 in history], visible=True)

    def _update_service_requests():
        nonlocal pending_table_data, requests_table_data
        pending_table_data, requests_table_data = get_service_requests_data()
        window[PENDING_REQUESTS_TABLE].update(values=get_requests_table_data(pending_table_data))
        window[SERVICE_REQUESTS_TABLE].update(values=get_requests_table_data(requests_table_data))

    home_layout = home_tab_screen(pending_table_data, requests_table_data)

    search_layout = search_tab_screen(table_data, SEARCH_TABLE_HEADERS, SEARCH_TABLE_COL_WIDTHS)

    request_layout = purchase_history_tab_screen(history)

    logout_layout = [[
        sg.Text(f'Welcome, {user.name}.', font=('Arial', 28)),
        sg.Button('Log Out'),
    ]]

    tab_layout = [[
        logout_layout,
        sg.TabGroup([
            [sg.Tab('         Home         ', [[sg.Column(home_layout, pad=25)]])],
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
            window[WRONG_ENTRY].update('')
            try:
                table_data, item_data = _get_filtered_results()
                window[SEARCH_TABLE].update(values=table_data)
            except TypeError:
                continue

        elif event == RESET_BUTTON:
            is_after_reset = True
            table_data, item_data = get_filtered_results()
            window[SEARCH_TABLE].update(values=table_data)

        elif event == SEARCH_TABLE:
            try:
                index = values[SEARCH_TABLE][0]
                item_list = item_data[index]
                if len(item_list) > 0:
                    item_purchase_window(item_list, [_update_search_table, _update_purchase_history])
                else:
                    sg.popup(f'Product ID: {table_data[index][0]} is out of stock', custom_text="That's unfortunate...")
            except IndexError:
                continue

        elif event == HISTORY_TABLE:
            try:
                index = values[HISTORY_TABLE][0]
                item = history[index]
                item = get_item_information_by_id(item['id'])
                if item['service_status'] in ['', 'Canceled', 'Completed']:
                    window[REQUEST_SERVICING_BUTTON].update(visible=True)
                else:
                    window[REQUEST_SERVICING_BUTTON].update(visible=False)
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
                window[ITEM_PURCHASE_DATE_TEXT].update(f'{item["purchase_date"]}')
            except IndexError:
                continue

        elif event == REQUEST_SERVICING_BUTTON:
            try:
                index = values[HISTORY_TABLE][0]
                item = history[index]
                item = get_item_information_by_id(item['id'])
                request_servicing_popup(item, [_update_purchase_history, _update_service_requests])
            except IndexError:
                continue

        elif event == PENDING_REQUESTS_TABLE:
            try:
                index = values[PENDING_REQUESTS_TABLE][0]
                request = pending_table_data[index]
                make_payment_popup(request.request_id, [_update_service_requests])
            except IndexError:
                continue

    window.close()
