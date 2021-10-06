import PySimpleGUI as sg

window_size = (800, 700)


def setup_window(title: str, layout, size=None, keep_on_top=False):
    """
    Use this function to generate new windows
    @param title: Title to be set for new screen
    @param layout: A PySimpleGUI layout object
    @param size: Optional custom window size
    @param keep_on_top: Optional parameter to set keep_on_top attribute on window
    """
    if size:
        return sg.Window(title, layout, size=size, keep_on_top=keep_on_top, finalize=True)

    return sg.Window(title, layout, keep_on_top=keep_on_top, finalize=True)
