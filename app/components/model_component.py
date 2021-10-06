import PySimpleGUI as sg

MODEL_OPTION = 'model_option'
MODEL_RADIO = 'model_radio'


def model_component(mod):
    return [sg.Radio('Model', MODEL_RADIO, default=False, enable_events=True, key=MODEL_RADIO, size=10),
            sg.OptionMenu(mod, default_value=mod[0], disabled=True, key=MODEL_OPTION, size=10)]
