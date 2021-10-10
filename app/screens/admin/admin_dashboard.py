import PySimpleGUI as sg

from app.auth import get_current_user
from app.components.category_component import category_component, CATEGORY_RADIO, CATEGORY_OPTION
from app.components.centered_component import centered_component
from app.components.color_component import colors_filter_component, COLOR_CHECKBOX_VAL, COLOR_CHECKBOX
from app.components.factory_component import factories_filter_component, FACTORY_CHECKBOX_VAL, FACTORY_CHECKBOX
from app.components.item_search_component import item_search_component, ITEM_SEARCH_VAL, ITEM_SEARCH_RADIO
from app.components.item_summary_popup import item_summary_popup
from app.components.model_component import model_component, MODEL_RADIO
from app.components.power_supplies_component import power_supplies_filter_component, POWER_SUPPLY_CHECKBOX_VAL, \
    POWER_SUPPLY_CHECKBOX
from app.components.production_years_filter_component import production_years_filter_component, \
    PRODUCTION_YEARS_CHECKBOX_VAL, PRODUCTION_YEAR_CHECKBOX
from app.components.request_popup import request_popup
from app.components.search_table_component import search_table_component, SEARCH_TABLE
from app.database.utils import get_categories, get_models, get_colors, get_factories, get_power_supplies, \
    get_production_years, get_filtered_results, find_item_by_id, get_sold_and_unsold, \
    find_service_requests_by_status, update_request_status_by_id, update_request_admin_by_id, \
    update_service_status_by_id
from app.models.item import ServiceStatus
from app.models.request import RequestStatus
from app.screens.customer.cust_dashboard import SEARCH_BUTTON
from app.utils import setup_window, get_requests_table_data

REQUESTS_TABLE_PADDING = [5, 15, 15, 15, 15, 5, 5, 15]
COMPLETED_REQUESTS_TABLE = 'completed_requests_table'
PENDING_APPROVALS_TABLE = 'pending_approvals_table'
ONGOING_REQUESTS_TABLE = 'ongoing_requests_table'
STOCK_LEVELS_TABLE = 'stock_levels_table'
STOCK_LEVELS_TABLE_HEADERS = ['IID', 'Number of "SOLD" items', 'Number of "UNSOLD" items']
REQUESTS_TABLE_HEADERS = ['RID', 'Service Amount ($)', 'Payment Date', 'Request Status', 'Request Date', 'CID', 'IID',
                          'Serviced By']

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


def approve_request_popup(request, update_pending_requests, update_service_requests):
    user_id = get_current_user().id
    layout = centered_component([sg.Button('Confirm'), sg.Button('Cancel', button_color='grey')], top_children=[
        [sg.Text(f'Approving Request ID: {request.request_id}')],
    ])
    window = setup_window('Make Payment', layout, keep_on_top=True)
    while True:
        event, values = window.read()
        if event in ['Cancel', sg.WIN_CLOSED]:
            break

        elif event == 'Confirm':
            update_request_status_by_id(request.request_id, RequestStatus.Approved.value)
            update_service_status_by_id(request.item_id, ServiceStatus.InProgress.value)
            update_request_admin_by_id(request.request_id, user_id)
            update_pending_requests()
            update_service_requests()
            break

    window.close()


def servicing_tab_screen(ongoing_requests_data, completed_requests_data):
    ongoing_requests_data = get_requests_table_data(ongoing_requests_data, admin=True)
    completed_requests_data = get_requests_table_data(completed_requests_data, admin=True)

    return [
        [sg.Text('Ongoing Service Requests', font=('Arial', 24))],
        [sg.Text('Click on a request to complete servicing.')],
        [sg.Table(values=ongoing_requests_data, headings=REQUESTS_TABLE_HEADERS,
                  auto_size_columns=False,
                  col_widths=REQUESTS_TABLE_PADDING,
                  justification='right',
                  num_rows=7,
                  alternating_row_color='lightyellow',
                  key=ONGOING_REQUESTS_TABLE,
                  row_height=35,
                  tooltip='Service Requests',
                  enable_events=True,
                  pad=(10, 10)
                  )],
        [sg.Text('Completed Service Requests', font=('Arial', 24))],
        [sg.Text('Click on a request to view more details.')],
        [sg.Table(values=completed_requests_data, headings=REQUESTS_TABLE_HEADERS,
                  auto_size_columns=False,
                  col_widths=REQUESTS_TABLE_PADDING,
                  justification='right',
                  num_rows=7,
                  alternating_row_color='lightyellow',
                  key=COMPLETED_REQUESTS_TABLE,
                  row_height=35,
                  tooltip='Service Requests',
                  enable_events=True,
                  pad=(10, 10)
                  )],
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


def home_tab_screen(stock_levels_data, pending_requests_data):
    stock_levels_data = [list(item.values()) for item in stock_levels_data]
    pending_requests_data = get_requests_table_data(pending_requests_data, admin=True)
    return [
        [sg.Text('Overview', font=('Arial', 24))],
        [sg.Table(values=stock_levels_data, headings=STOCK_LEVELS_TABLE_HEADERS,
                  justification='right',
                  num_rows=7,
                  alternating_row_color='lightyellow',
                  key=STOCK_LEVELS_TABLE,
                  row_height=35,
                  tooltip='Stock Levels',
                  pad=(10, 10)
                  )],
        [sg.Text('Pending Approval', font=('Arial', 24))],
        [sg.Text('Click on a request to approve.')],
        [sg.Table(values=pending_requests_data, headings=REQUESTS_TABLE_HEADERS,
                  auto_size_columns=False,
                  col_widths=REQUESTS_TABLE_PADDING,
                  justification='right',
                  num_rows=7,
                  alternating_row_color='lightyellow',
                  key=PENDING_APPROVALS_TABLE,
                  row_height=35,
                  tooltip='Pending Requests',
                  enable_events=True,
                  pad=(10, 10)
                  )],
    ]


def administrator_screen():
    user = get_current_user()
    table_data, item_data = get_filtered_results(admin=True)
    stock_levels_data = get_sold_and_unsold()
    pending_requests_data = find_service_requests_by_status(
        (RequestStatus.Submitted.value, RequestStatus.InProgress.value,))
    ongoing_requests_data = find_service_requests_by_status(
        (RequestStatus.Approved.value, RequestStatus.WaitingForPayment.value))
    completed_requests_data = find_service_requests_by_status((RequestStatus.Completed.value,))
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

    def update_pending_requests():
        nonlocal pending_requests_data
        pending_requests_data = find_service_requests_by_status(
            (RequestStatus.Submitted.value, RequestStatus.InProgress.value,))
        window[PENDING_APPROVALS_TABLE].update(values=get_requests_table_data(pending_requests_data, admin=True))

    def update_service_requests():
        nonlocal ongoing_requests_data, completed_requests_data
        ongoing_requests_data = find_service_requests_by_status(
            (RequestStatus.Approved.value, RequestStatus.WaitingForPayment.value))
        completed_requests_data = find_service_requests_by_status((RequestStatus.Completed.value,))
        window[ONGOING_REQUESTS_TABLE].update(values=get_requests_table_data(ongoing_requests_data, admin=True))
        window[COMPLETED_REQUESTS_TABLE].update(values=get_requests_table_data(completed_requests_data, admin=True))

    home_layout = home_tab_screen(stock_levels_data, pending_requests_data)

    search_layout = search_tab_screen(table_data)

    servicing_layout = servicing_tab_screen(ongoing_requests_data, completed_requests_data)

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
                approve_request_popup(request, update_pending_requests, update_service_requests)
            except IndexError:
                continue

        elif event == ONGOING_REQUESTS_TABLE:
            try:
                index = values[ONGOING_REQUESTS_TABLE][0]
                request = ongoing_requests_data[index]
                request_popup(request, [update_service_requests])
            except IndexError:
                continue

    window.close()
