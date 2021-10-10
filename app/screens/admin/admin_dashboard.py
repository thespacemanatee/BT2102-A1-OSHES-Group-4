import PySimpleGUI as sg

from app.auth import get_current_user
from app.components.approve_request_popup import approve_request_popup
from app.components.category_component import CATEGORY_RADIO, CATEGORY_OPTION
from app.components.color_component import COLOR_CHECKBOX_VAL, COLOR_CHECKBOX
from app.components.factory_component import FACTORY_CHECKBOX_VAL, FACTORY_CHECKBOX
from app.components.item_search_component import ITEM_SEARCH_VAL, ITEM_SEARCH_RADIO
from app.components.item_summary_popup import item_summary_popup
from app.components.model_component import MODEL_RADIO, MODEL_OPTION
from app.components.power_supplies_component import POWER_SUPPLY_CHECKBOX_VAL, \
    POWER_SUPPLY_CHECKBOX
from app.components.production_years_filter_component import PRODUCTION_YEARS_CHECKBOX_VAL, PRODUCTION_YEAR_CHECKBOX
from app.components.search_table_component import SEARCH_TABLE
from app.components.service_request_popup import service_request_popup
from app.database.utils import get_filtered_results, find_item_by_id, get_sold_and_unsold, \
    find_service_requests_by_status
from app.models.request import RequestStatus
from app.screens.admin.home_tab_screen import home_tab_screen, COMPLETED_REQUESTS_TABLE
from app.screens.admin.servicing_tab_screen import servicing_tab_screen, PENDING_APPROVALS_TABLE, ONGOING_REQUESTS_TABLE
from app.screens.commons.search_tab_screen import search_tab_screen, RESET_BUTTON, SEARCH_BUTTON
from app.utils import setup_window, get_requests_table_data

SEARCH_TABLE_HEADERS = [
    'PID',
    'Category',
    'Model',
    'Cost ($)',
    'Price ($)',
    'Warranty (months)',
    'Stock',
    'Sold'
]

SEARCH_TABLE_COL_WIDTHS = [5, 15, 15, 10, 10, 15, 10, 10]


def get_service_requests_data():
    pending_requests_data = find_service_requests_by_status(
        (RequestStatus.Submitted.value, RequestStatus.InProgress.value, RequestStatus.WaitingForPayment.value))
    ongoing_requests_data = find_service_requests_by_status((RequestStatus.Approved.value,))
    completed_requests_data = find_service_requests_by_status((RequestStatus.Completed.value,))
    return pending_requests_data, ongoing_requests_data, completed_requests_data


def administrator_screen():
    user = get_current_user()
    table_data, item_data = get_filtered_results(admin=True)
    stock_levels_data = get_sold_and_unsold()
    pending_requests_data, ongoing_requests_data, completed_requests_data = get_service_requests_data()
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

    def _update_service_requests():
        nonlocal pending_requests_data, ongoing_requests_data, completed_requests_data
        pending_requests_data, ongoing_requests_data, completed_requests_data = get_service_requests_data()
        window[PENDING_APPROVALS_TABLE].update(values=get_requests_table_data(pending_requests_data, admin=True))
        window[ONGOING_REQUESTS_TABLE].update(values=get_requests_table_data(ongoing_requests_data, admin=True))
        window[COMPLETED_REQUESTS_TABLE].update(values=get_requests_table_data(completed_requests_data, admin=True))

    home_layout = home_tab_screen(stock_levels_data, completed_requests_data)

    search_layout = search_tab_screen(table_data, SEARCH_TABLE_HEADERS, SEARCH_TABLE_COL_WIDTHS, admin=True)

    servicing_layout = servicing_tab_screen(ongoing_requests_data, pending_requests_data)

    logout_layout = [[
        sg.Text(f'Welcome, {user.name}.', font=('Arial', 28)),
        sg.Button('Log Out'),
    ]]

    tab_layout = [[
        logout_layout,
        sg.TabGroup([
            [sg.Tab('         Home         ', [[sg.Column(home_layout, pad=25)]])],
            [sg.Tab('        Search        ', [[sg.Column(search_layout, pad=25)]])],
            [sg.Tab('       Servicing      ', [[sg.Column(servicing_layout, pad=25)]])],
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

        elif event == PENDING_APPROVALS_TABLE:
            try:
                index = values[PENDING_APPROVALS_TABLE][0]
                request = pending_requests_data[index]
                approve_request_popup(request, [_update_service_requests])
            except IndexError:
                continue

        elif event == ONGOING_REQUESTS_TABLE:
            try:
                index = values[ONGOING_REQUESTS_TABLE][0]
                request = ongoing_requests_data[index]
                service_request_popup(request, [_update_service_requests])
            except IndexError:
                continue

    window.close()
