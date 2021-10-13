from datetime import date

import PySimpleGUI as sg

from app.components.centered_component import centered_component
from app.database.utils import update_request_status_by_id, update_service_payment_date_by_id, \
    update_service_status_by_id
from app.models.item import ServiceStatus
from app.models.request import RequestStatus
from app.utils import setup_window


def make_payment_popup(request, callbacks=None):
    if callbacks is None:
        callbacks = []
    layout = centered_component(
        [sg.Button('Confirm Payment'), sg.Button('Cancel Request', button_color='red'),
         sg.Button('Cancel', button_color='grey')],
        top_children=[
            [sg.Text(f'Making payment for Request ID: {request.request_id}', expand_x=True, justification='center')],
        ])
    window = setup_window('Make Payment', layout, keep_on_top=True)
    while True:
        event, values = window.read()
        if event in ['Cancel', sg.WIN_CLOSED]:
            break

        elif event == 'Cancel Request':
            update_request_status_by_id(request.request_id, RequestStatus.Canceled.value)
            update_service_status_by_id(request.item_id, ServiceStatus.Empty.value)
            for callback in callbacks:
                callback()
            break

        elif event == 'Confirm Payment':
            update_request_status_by_id(request.request_id, RequestStatus.InProgress.value)
            update_service_payment_date_by_id(request.request_id, date.today())
            for callback in callbacks:
                callback()
            break

    window.close()
