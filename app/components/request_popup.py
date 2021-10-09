import PySimpleGUI as sg

from app.auth import get_current_user
from app.components.centered_component import centered_component, COLUMN, EXPAND_1, EXPAND_2
from app.database.utils import update_request_status_by_id, update_request_admin_by_id
from app.models.request import RequestStatus
from app.utils import setup_window

SERVICING_COMPLETED_BUTTON = 'servicing_completed_button'


def request_popup(request, callbacks=None):
    user_id = get_current_user().id
    if callbacks is None:
        callbacks = []
    layout = centered_component(top_children=[
        sg.Column([
            [sg.Text('Item ID:')],
            [sg.Text('Customer ID:')],
            [sg.Text('Serviced By:')],
            [sg.Text('Service Amount:')],
            [sg.Text('Service Payment Date:')],
            [sg.Text('Request Status:')],
            [sg.Text('Request Date:')],
        ],
            pad=20
        ), sg.Column([
            [sg.Text(request.item_id)],
            [sg.Text(request.customer_id)],
            [sg.Text(request.admin_id)],
            [sg.Text(request.service_amount)],
            [sg.Text(request.service_payment_date)],
            [sg.Text(request.request_status)],
            [sg.Text(request.request_date)],
        ],
            element_justification='right',
            pad=20
        )
    ], centered_children=[sg.Button('Servicing Completed', key=SERVICING_COMPLETED_BUTTON,
                                    visible=True if request.request_status == RequestStatus.Approved.value else False),
                          sg.Cancel(s=10)])

    popup = setup_window(f'Request ID: {request.request_id}', layout, keep_on_top=True)

    while True:
        event, values = popup.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            break

        elif event == SERVICING_COMPLETED_BUTTON:
            update_request_status_by_id(request.request_id, RequestStatus.Completed.value)
            update_request_admin_by_id(request.request_id, user_id)
            for callback in callbacks:
                callback()
            break

    popup.close()