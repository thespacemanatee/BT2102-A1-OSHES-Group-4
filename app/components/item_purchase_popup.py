import PySimpleGUI as sg

from app.auth import get_current_user
from app.components.centered_component import centered_component
from app.database.utils import purchase_item
from app.utils import setup_window

WRONG_ENTRY = 'wrong_entry'

QUANTITY_VAL = 'quantity_val'


def item_purchase_popup(product, item, callbacks=None):
    if callbacks is None:
        callbacks = []
    user_id = get_current_user().id
    layout = centered_component(top_children=[
        sg.Column([
            [sg.Text('Category:')],
            [sg.Text('Model:')],
            [sg.Text('Color:')],
            [sg.Text('Factory:')],
            [sg.Text('Power Supply:')],
            [sg.Text('Production Year:')],
            [sg.Text('Price ($):')],
            [sg.Text('Warranty (months)')],
        ],
            pad=20
        ), sg.Column([
            [sg.Text(product["Category"])],
            [sg.Text(product["Model"])],
            [sg.Text(item["Color"])],
            [sg.Text(item["Factory"])],
            [sg.Text(item["PowerSupply"])],
            [sg.Text(item["ProductionYear"])],
            [sg.Text(product["Price ($)"])],
            [sg.Text(product["Warranty (months)"])],
        ],
            element_justification='right',
            pad=20
        )
    ], centered_children=[sg.Column([[sg.Text(f'Quantity: ({item["Stock"]} left)'), sg.Input(k=QUANTITY_VAL, s=9)],
                                     [sg.Text(k=WRONG_ENTRY)],
                                     [sg.Column([[
                                         sg.Button('Purchase', s=10), sg.Button('Cancel', s=10, button_color='grey')]
                                     ])]
                                     ]),
                          ])

    popup = setup_window('Confirm Purchase', layout, keep_on_top=True)

    while True:
        event, values = popup.read()
        if event in ('Cancel', sg.WIN_CLOSED):
            break

        elif event == 'Purchase':
            try:
                quantity = int(values[QUANTITY_VAL])
                if quantity > item['Stock']:
                    popup[WRONG_ENTRY].update('Quantity exceeded.', text_color='red')
                elif quantity <= 0:
                    popup[WRONG_ENTRY].update('Enter a number more than 0.', text_color='red')
                else:
                    purchase_item(user_id, {
                        'Category': item['Category'],
                        'Model': item['Model'],
                        'Color': item['Color'],
                        'Factory': item['Factory'],
                        'PowerSupply': item['PowerSupply'],
                        'ProductionYear': item['ProductionYear'],
                    }, int(values[QUANTITY_VAL]))
                    for callback in callbacks:
                        callback()
                    break
            except ValueError:
                popup[WRONG_ENTRY].update('Please enter a number.', text_color='red')

    popup.close()
