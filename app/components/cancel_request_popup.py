import PySimpleGUI as sg

from app.components.centered_component import centered_component
from app.database.utils import update_request_status_by_id, update_service_status_by_id
from app.models.item import ServiceStatus
from app.models.request import RequestStatus
from app.utils import setup_window


def cancel_request_popup(request, callbacks=None):
    if callbacks is None:
        callbacks = []
    layout = centered_component(
        [sg.Button('Confirm'),
         sg.Button('Cancel', button_color='grey')],
        top_children=[
            [sg.Text(f'Cancelling Request ID: {request.request_id}', expand_x=True, justification='center')],
        ])

    window = setup_window('Cancel Request', layout, keep_on_top=True)

    while True:
        event, values = window.read()
        if event in ['Cancel', sg.WIN_CLOSED]:
            break

        elif event == 'Confirm':
            update_request_status_by_id(request.request_id, RequestStatus.Canceled.value)
            update_service_status_by_id(request.item_id, ServiceStatus.Empty.value)
            for callback in callbacks:
                callback()
            break

    window.close()
