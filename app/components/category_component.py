import PySimpleGUI as sg

CATEGORY_OPTION = 'category_option'
CATEGORY_RADIO = 'category_radio'


def category_component(cat):
    return [sg.Radio('Category', CATEGORY_RADIO, default=True, enable_events=True, key=CATEGORY_RADIO, size=10),
            sg.OptionMenu(cat, default_value=cat[0], disabled=False, key=CATEGORY_OPTION,
                          size=10)]
