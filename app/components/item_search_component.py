import PySimpleGUI as sg

ITEM_SEARCH_VAL = "item_search_val"
ITEM_SEARCH_RADIO = 'item_radio'


def item_search_component():
    return [sg.Radio('Item Id', ITEM_SEARCH_RADIO, default=False, enable_events=True, key=ITEM_SEARCH_RADIO, size=10),
            sg.Input(key=ITEM_SEARCH_VAL)]
