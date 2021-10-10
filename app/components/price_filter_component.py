import PySimpleGUI as sg

PRICE_CHECKBOX = 'price_checkbox'
PRICE_MIN_VAL = 'price_min_val'
PRICE_MAX_VAL = 'price_max_val'


def price_filter_component():
    return sg.Column([[sg.Checkbox('Price', key=PRICE_CHECKBOX),
                       sg.Input('Min', key=PRICE_MIN_VAL, size=10),
                       sg.Input('Max', key=PRICE_MAX_VAL, size=10),
                       ]
                      ])
