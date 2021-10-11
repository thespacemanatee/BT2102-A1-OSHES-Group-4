import PySimpleGUI as sg

from app.components.base_table_component import base_table_component
from app.utils import get_requests_table_data

REQUESTS_TABLE_PADDING = [5, 15, 15, 15, 15, 5, 5, 15]
UNDER_SERVICE_TABLE = 'under_service_table'
WAITING_PAYMENT_TABLE = 'waiting_payment_table'
REQUESTS_TABLE_HEADERS = ['RID', 'Service Amount ($)', 'Payment Date', 'Request Status', 'Request Date', 'CID', 'IID',
                          'Serviced By']


def servicing_tab_screen(under_service_data, waiting_payment_data):
    under_service_data = get_requests_table_data(under_service_data, admin=True)
    waiting_payment_data = get_requests_table_data(waiting_payment_data, admin=True)

    return [
        [sg.Text('Items under service', font=('Arial', 24))],
        [sg.Text('Click on a request to view options.')],
        [base_table_component(values=under_service_data, headings=REQUESTS_TABLE_HEADERS,
                              key=UNDER_SERVICE_TABLE,
                              col_widths=REQUESTS_TABLE_PADDING,
                              tooltip='Items under service',
                              pad=(10, 10)
                              )],
        [sg.Text('Waiting for payment', font=('Arial', 24))],
        [base_table_component(values=waiting_payment_data, headings=REQUESTS_TABLE_HEADERS,
                              key=WAITING_PAYMENT_TABLE,
                              col_widths=REQUESTS_TABLE_PADDING,
                              tooltip='Waiting for payment',
                              pad=(10, 10)
                              )],
    ]
