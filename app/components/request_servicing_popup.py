import PySimpleGUI as sg

from app.auth import get_current_user
from app.components.centered_component import centered_component
from app.database.utils import insert_request_by_id, get_request_status
from app.utils import setup_window


def request_servicing_popup(item, callbacks=None):
    if callbacks is None:
        callbacks = []
    user_id = get_current_user().id
    layout = centered_component([sg.Button('Confirm'), sg.Button('Cancel', button_color='grey')], top_children=[
        [sg.Text(f'Request servicing for Item ID: {item["id"]}?')],
    ])
    window = setup_window('Request for Servicing', layout, keep_on_top=True)
    while True:
        event, values = window.read()
        if event in ['Cancel', sg.WIN_CLOSED]:
            break

        elif event == 'Confirm':
            request_status, service_amount = get_request_status(item)
            insert_request_by_id(item, user_id, request_status, 'Waiting for approval', service_amount)
            for callback in callbacks:
                callback()
            break

    window.close()
