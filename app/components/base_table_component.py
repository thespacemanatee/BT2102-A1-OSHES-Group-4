import PySimpleGUI as sg


def base_table_component(values, headings, key, auto_size_columns=False, col_widths=None, justification='right',
                         num_rows=7, alternating_row_color='lightyellow', row_height=35, tooltip='', enable_events=True,
                         pad=None):
    return sg.Table(values=values, headings=headings,
                    auto_size_columns=auto_size_columns,
                    col_widths=col_widths,
                    justification=justification,
                    num_rows=num_rows,
                    alternating_row_color=alternating_row_color,
                    key=key,
                    row_height=row_height,
                    tooltip=tooltip,
                    enable_events=enable_events,
                    pad=pad
                    )
