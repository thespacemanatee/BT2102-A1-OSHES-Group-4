import PySimpleGUI as sg

from app.components.base_table_component import base_table_component
from app.utils import get_requests_table_data

REQUESTS_TABLE_PADDING = [5, 15, 15, 15, 15, 5, 5, 15]
ONGOING_REQUESTS_TABLE = 'ongoing_requests_table'
PENDING_APPROVALS_TABLE = 'pending_approvals_table'
REQUESTS_TABLE_HEADERS = ['RID', 'Service Amount ($)', 'Payment Date', 'Request Status', 'Request Date', 'CID', 'IID',
                          'Serviced By']


def servicing_tab_screen(ongoing_requests_data, pending_requests_data):
    ongoing_requests_data = get_requests_table_data(ongoing_requests_data, admin=True)
    pending_requests_data = get_requests_table_data(pending_requests_data, admin=True)

    return [
        [sg.Text('Ongoing Service Requests', font=('Arial', 24))],
        [sg.Text('Click on a request to complete servicing.')],
        [base_table_component(values=ongoing_requests_data, headings=REQUESTS_TABLE_HEADERS,
                              key=ONGOING_REQUESTS_TABLE,
                              col_widths=REQUESTS_TABLE_PADDING,
                              tooltip='Service Requests',
                              pad=(10, 10)
                              )],
        [sg.Text('Pending Approval', font=('Arial', 24))],
        [sg.Text('Click on a request to approve.')],
        [base_table_component(values=pending_requests_data, headings=REQUESTS_TABLE_HEADERS,
                              key=PENDING_APPROVALS_TABLE,
                              col_widths=REQUESTS_TABLE_PADDING,
                              tooltip='Pending Requests',
                              pad=(10, 10)
                              )],
    ]
