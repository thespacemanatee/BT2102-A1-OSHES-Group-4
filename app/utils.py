import PySimpleGUI as sg

window_size = (800, 700)


def setup_window(title: str, layout, size=None):
    """
    Use this function to generate new windows
    @param title: Title to be set for new screen
    @param layout: A PySimpleGUI layout object
    @param size: Optional custom window size
    """
    if size:
        return sg.Window(title, layout, size=size, finalize=True)

    return sg.Window(title, layout, finalize=True)
