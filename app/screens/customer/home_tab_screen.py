import PySimpleGUI as sg

from app.components.base_table_component import base_table_component
from app.utils import get_requests_table_data

REQUESTS_TABLE_PADDING = [5, 15, 15, 15, 15, 5, 15]
PENDING_REQUESTS_TABLE = 'pending_requests_table'
SERVICE_REQUESTS_TABLE = 'service_requests_table'
REQUESTS_TABLE_HEADERS = ['RID', 'Service Amount ($)', 'Payment Date', 'Request Status', 'Request Date', 'IID',
                          'Serviced By']


def home_tab_screen(pending_table_data, requests_table_data):
    pending_table_data = get_requests_table_data(pending_table_data)
    requests_table_data = get_requests_table_data(requests_table_data)

    return [
        [sg.Text('Pending Payment', font=('Arial', 20))],
        [sg.Text('Click on an item to make payment')],
        [base_table_component(values=pending_table_data, headings=REQUESTS_TABLE_HEADERS,
                              key=PENDING_REQUESTS_TABLE,
                              col_widths=REQUESTS_TABLE_PADDING,
                              justification='right',
                              tooltip='Item List',
                              pad=(10, 10))],
        [sg.Text('Service Requests', font=('Arial', 20))],
        [base_table_component(values=requests_table_data, headings=REQUESTS_TABLE_HEADERS,
                              key=SERVICE_REQUESTS_TABLE,
                              col_widths=REQUESTS_TABLE_PADDING,
                              tooltip='Item List',
                              pad=(10, 10))]
    ]
