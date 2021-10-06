import PySimpleGUI as sg

from app.components.centered_component import centered_component, COLUMN, EXPAND_1, EXPAND_2


def item_summary_popup(user_input, item):
    if item:
        layout = centered_component(top_children=[
            sg.Column([[sg.Text('Category:')],
                       [sg.Text(f'Model:')],
                       [sg.Text(f'Color:')],
                       [sg.Text(f'Factory:')],
                       [sg.Text(f'Power Supply:')],
                       [sg.Text(f'Purchase Status:')],
                       [sg.Text(f'Production Year:')],
                       [sg.Text(f'Service Status:')]],
                      pad=20
                      ), sg.Column([[sg.Text(item["Category"])],
                                    [sg.Text(item["Model"])],
                                    [sg.Text(item["Color"])],
                                    [sg.Text(item["Factory"])],
                                    [sg.Text(item["PowerSupply"])],
                                    [sg.Text(item["PurchaseStatus"])],
                                    [sg.Text(item["ProductionYear"])],
                                    [sg.Text(item["ServiceStatus"])]],
                                   element_justification='right',
                                   pad=20
                                   )
        ], centered_children=[sg.Ok(s=10)])
    else:
        layout = centered_component(top_children=sg.Text(f"Item ID: {user_input} not found. Did you enter a valid ID?"),
                                    centered_children=[sg.Ok(s=10)])

    popup = sg.Window(f'Item ID: {user_input}', layout, keep_on_top=True, finalize=True)
    popup[COLUMN].expand(True, True, True)
    popup[EXPAND_1].expand(True, True, True)
    popup[EXPAND_2].expand(True, False, True)
    choice, _ = popup.read(close=True)
