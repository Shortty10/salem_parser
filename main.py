import requests
from bs4 import BeautifulSoup


def parse_report(url):
    """
    Parse the report's HTML into a report object.

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
    :class:`Report`
        The report object.
    """
    r = requests.get(url).text
    if r == "Could not find any reports with that ID.":
        raise ValueError("Report not found.")
    soup = BeautifulSoup(r, "lxml")

    judgement = soup.find("div", id="splash").text
    if judgement == "This report has been closed without judgement.":
        judgement = "Closed"
    elif judgement == "This report has been deemed guilty.":
        judgement = "Guilty"
    elif judgement == "This report has been deemed innocent.":
        judgement = "Innocent"

    data = {}

    data['judgement'] = judgement

    data['id'] = soup.find("span", class_="reportId").text

    data['user'] = soup.find("span", class_="reportedPlayer").text

    data['reason'] = soup.find("span", class_="reportReason").text

    data['ranked'] = bool("Ranked Game." in soup.find(
        "span", class_="notice").text)

    data['details'] = str(soup.find("span", class_='reportDescription')).split(
        '<span class="reportDescription">')[1].split('</span>')[0].split("<br/>")

    data['details'] = [] if data['details'] == [''] else data['details']

    return Report(data)


class Report:
    def __init__(self, data):
        self.id = data["id"]
        self.user = data["user"]
        self.reason = data["reason"]
        self.details = data["details"]
        self.ranked = data['ranked']
        self.judgement = data['judgement']
