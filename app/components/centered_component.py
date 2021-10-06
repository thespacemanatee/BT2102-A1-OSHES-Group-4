import PySimpleGUI as sg

COLUMN = "-C-"
EXPAND_1 = "-EXPAND1-"
EXPAND_2 = "-EXPAND2-"


def centered_component(centered_children, top_children=None):
    if top_children:
        return [[sg.Text(key=EXPAND_1, font='ANY 1', pad=(0, 0))],
                [sg.Text('', pad=(0, 0), key=EXPAND_2),
                 [top_children],
                 sg.Column([centered_children], vertical_alignment='center', justification='center', k=COLUMN)]]

    return [[sg.Text(key=EXPAND_1, font='ANY 1', pad=(0, 0))],
            [sg.Text('', pad=(0, 0), key=EXPAND_2),
             sg.Column([centered_children], vertical_alignment='center', justification='center', k=COLUMN)]]
