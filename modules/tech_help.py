import webbrowser

def open_url(url):
    """
    Open the specified URL in the default web browser.
    
    Parameters:
        url (str): The URL to open.
        
    Returns:
        None
    """
    webbrowser.open(url)

# Example usage:
url = "https://github.com/Brotherkayman"
open_url(url)
