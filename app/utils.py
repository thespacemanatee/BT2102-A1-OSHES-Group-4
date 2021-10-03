import PySimpleGUI as sg


window_size = (1200, 800)

def setup_window(title: str, layout):
    """
    Use this function to generate new windows
    @param title: Title to be set for new screen
    @param layout: A PySimpleGUI layout object
    """

    return sg.Window(title, layout, resizable=True, size=window_size, finalize=True)
