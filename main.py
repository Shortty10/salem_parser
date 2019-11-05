import requests
from bs4 import BeautifulSoup


def parse_report(url):
    """
    Parse the report into a BeautifulSoup object.

    Parameters
    -------------
    url: :class:`str`
        The report URL

    Raises
    -------------
    ValueError
        Invalid URL

    Returns
    -------------
    :class:`bs4.BeautifulSoup`
        The Soup Object.
    """
    r = requests.get(url).text
    if r == "Could not find any reports with that ID.":
        raise ValueError("Report not found.")
    soup = BeautifulSoup(r, "lxml")
    return soup
