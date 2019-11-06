import requests
from bs4 import BeautifulSoup
import json


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
        Invalid ID

    Returns
    -------------
    :class:`Report`
        The report object.
    """
    r = requests.get(url).text
    if r == "Could not find any reports with that ID.":
        raise ValueError("Report not found.")
    soup = BeautifulSoup(r, "lxml")

    judgement = soup.find("div", id="splash")
    if not judgement:
        judgement = "Open"
    elif judgement.text == "This report has been closed without judgement.":
        judgement = "Closed"
    elif judgement.text == "This report has been deemed guilty.":
        judgement = "Guilty"
    elif judgement.text == "This report has been deemed innocent.":
        judgement.text = "Innocent"

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

    return Report(data, soup)


class Report:
    def __init__(self, data, soup):
        self.soup = soup
        self.id = data["id"]
        self.reported = self.get_player(data['user'])
        self.reason = data["reason"]
        self.details = data["details"]
        self.ranked = data['ranked']
        self.judgement = data['judgement']

    def get_player(self, name):
        data = {}
        data['name'] = name
        return Player(data, self.soup)


class Player:
    def __init__(self, data, soup):

        self.name = data['name']

        all_players = str(soup.find_all("script")).split(
            'data =')[1].split("}]};")[0] + "}]}"

        all_players = json.loads(all_players)["players"]

        for player in all_players:
            if player["username"] == self.name:
                info = player
                break

        role_info = find_faction(info["role"])

        self.name = info["username"]
        self.role = info["role"]
        self.slot = info["slot"]
        self.nick = info["ign"]
        self.faction = role_info["faction"]
        self.alignment = role_info["alignment"]


def find_faction(role):

    if role == "Bodyguard":
        role_info = {"faction": "Town", "alignment": "Town Protective"}
    elif role == "Doctor":
        role_info = {"faction": "Town", "alignment": "Town Protective"}
    elif role == "Escort":
        role_info = {"faction": "Town", "alignment": "Town Support"}
    elif role == "Investigator":
        role_info = {"faction": "Town", "alignment": "Town Investigative"}
    elif role == "Jailor":
        role_info = {"faction": "Town", "alignment": "Town Killing"}
    elif role == "Lookout":
        role_info = {"faction": "Town", "alignment": "Town Investigative"}
    elif role == "Mayor":
        role_info = {"faction": "Town", "alignment": "Town Support"}
    elif role == "Medium":
        role_info = {"faction": "Town", "alignment": "Town Support"}
    elif role == "Retributionist":
        role_info = {"faction": "Town", "alignment": "Town Support"}
    elif role == "Sheriff":
        role_info = {"faction": "Town", "alignment": "Town Investigative"}
    elif role == "Spy":
        role_info = {"faction": "Town", "alignment": "Town Investigative"}
    elif role == "Transporter":
        role_info = {"faction": "Town", "alignment": "Town Support"}
    elif role == "Vampire Hunter":
        role_info = {"faction": "Town", "alignment": "Town Killing"}
    elif role == "Veteran":
        role_info = {"faction": "Town", "alignment": "Town Killing"}
    elif role == "Vigilante":
        role_info = {"faction": "Town", "alignment": "Town Killing"}
    elif role == "Crusader":
        role_info = {"faction": "Town", "alignment": "Town Protective"}
    elif role == "Tracker":
        role_info = {"faction": "Town", "alignment": "Town Investigative"}
    elif role == "Trapper":
        role_info = {"faction": "Town", "alignment": "Town Protective"}
    elif role == "Psychic":
        role_info = {"faction": "Town", "alignment": "Town Investigative"}

    elif role == "Blackmailer":
        role_info = {"faction": "Mafia", "alignment": "Mafia Support"}
    elif role == "Consigliere":
        role_info = {"faction": "Mafia", "alignment": "Mafia Support"}
    elif role == "Consort":
        role_info = {"faction": "Mafia", "alignment": "Mafia Support"}
    elif role == "Disguiser":
        role_info = {"faction": "Mafia", "alignment": "Mafia Deception"}
    elif role == "Forger":
        role_info = {"faction": "Mafia", "alignment": "Mafia Deception"}
    elif role == "Framer":
        role_info = {"faction": "Mafia", "alignment": "Mafia Deception"}
    elif role == "Godfather":
        role_info = {"faction": "Mafia", "alignment": "Mafia Killing"}
    elif role == "Janitor":
        role_info = {"faction": "Mafia", "alignment": "Mafia Deception"}
    elif role == "Mafioso":
        role_info = {"faction": "Mafia", "alignment": "Mafia Killing"}
    elif role == "Hypnotist":
        role_info = {"faction": "Mafia", "alignment": "Mafia Deception"}
    elif role == "Ambusher":
        role_info = {"faction": "Mafia", "alignment": "Mafia Support"}

    elif role == "Amnesiac":
        role_info = {"faction": "Neutral", "alignment": "Neutral Benign"}
    elif role == "Arsonist":
        role_info = {"faction": "Neutral", "alignment": "Neutral Killing"}
    elif role == "Executioner":
        role_info = {"faction": "Neutral", "alignment": "Neutral Evil"}
    elif role == "GuardianAngel":
        role_info = {"faction": "Neutral", "alignment": "Neutral Benign"}
    elif role == "Jester":
        role_info = {"faction": "Neutral", "alignment": "Neutral Evil"}
    elif role == "Juggernaut":
        role_info = {"faction": "Neutral", "alignment": "Neutral Killing"}
    elif role == "Pirate":
        role_info = {"faction": "Neutral", "alignment": "Neutral Chaos"}
    elif role == "Plaguebearer":
        role_info = {"faction": "Neutral", "alignment": "Neutral Chaos"}
    elif role == "Serial Killer":
        role_info = {"faction": "Neutral", "alignment": "Neutral Killing"}
    elif role == "Survivor":
        role_info = {"faction": "Neutral", "alignment": "Neutral Benign"}
    elif role == "Vampire":
        role_info = {"faction": "Neutral", "alignment": "Neutral Chaos"}
    elif role == "Werewolf":
        role_info = {"faction": "Neutral", "alignment": "Neutral Killing"}
    elif role == "Witch":
        role_info = {"faction": "Neutral", "alignment": "Neutral Evil1"}

    return role_info
