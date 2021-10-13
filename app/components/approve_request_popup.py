import PySimpleGUI as sg

from app.auth import get_current_user
from app.components.centered_component import centered_component
from app.database.utils import update_request_status_by_id, update_service_status_by_id, update_request_admin_by_id
from app.models.item import ServiceStatus
from app.models.request import RequestStatus
from app.utils import setup_window


def approve_request_popup(request, callbacks=None):
    if callbacks is None:
        callbacks = []
    user_id = get_current_user().id
    layout = centered_component([sg.Button('Confirm'), sg.Button('Cancel', button_color='grey')], top_children=[
        [sg.Text(f'Approve Servicing for Request ID: {request.request_id}')],
    ]) if request.request_status != RequestStatus.WaitingForPayment.value else centered_component(
        [sg.Button('Okay')], top_children=[
            [sg.Text(f'Request ID: {request.request_id} is awaiting payment from customer.')],
        ])
    window = setup_window('Approve Request', layout, keep_on_top=True)
    while True:
        event, values = window.read()
        if event in ['Cancel', 'Okay', sg.WIN_CLOSED]:
            break

        elif event == 'Confirm':
            update_request_status_by_id(request.request_id, RequestStatus.Approved.value)
            update_service_status_by_id(request.item_id, ServiceStatus.InProgress.value)
            update_request_admin_by_id(request.request_id, user_id)
            for callback in callbacks:
                callback()
            break

    window.close()
