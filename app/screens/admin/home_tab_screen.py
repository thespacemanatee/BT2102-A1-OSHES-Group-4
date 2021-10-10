import PySimpleGUI as sg

from app.components.base_table_component import base_table_component
from app.utils import get_requests_table_data

REQUESTS_TABLE_PADDING = [5, 15, 15, 15, 15, 5, 5, 15]
COMPLETED_REQUESTS_TABLE = 'completed_requests_table'
STOCK_LEVELS_TABLE = 'stock_levels_table'
STOCK_LEVELS_TABLE_HEADERS = ['IID', 'Number of "SOLD" items', 'Number of "UNSOLD" items']
REQUESTS_TABLE_HEADERS = ['RID', 'Service Amount ($)', 'Payment Date', 'Request Status', 'Request Date', 'CID', 'IID',
                          'Serviced By']


def home_tab_screen(stock_levels_data, completed_requests_data):
    stock_levels_data = [list(item.values()) for item in stock_levels_data]
    completed_requests_data = get_requests_table_data(completed_requests_data, admin=True)
    return [
        [sg.Text('Overview', font=('Arial', 24))],
        [base_table_component(values=stock_levels_data, headings=STOCK_LEVELS_TABLE_HEADERS,
                              auto_size_columns=True,
                              key=STOCK_LEVELS_TABLE,
                              tooltip='Stock Levels',
                              pad=(10, 10)
                              )],
        [sg.Text('Completed Service Requests', font=('Arial', 24))],
        [sg.Text('Click on a request to view more details.')],
        [base_table_component(values=completed_requests_data, headings=REQUESTS_TABLE_HEADERS,
                              key=COMPLETED_REQUESTS_TABLE,
                              col_widths=REQUESTS_TABLE_PADDING,
                              tooltip='Service Requests',
                              pad=(10, 10)
                              )],
    ]
