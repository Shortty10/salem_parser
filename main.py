import json
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

    return Report(data, soup)


class Report:
    def __init__(self, data, soup):
        content = list(soup.find("div", id="reportContent").find_all("span"))

        count = 0
        new_list = []

        for message in content:
            new_list.append(str(message))

        content = new_list
        days = {}

        for message in content:
            if '<span class="note"' in message:
                content.remove(message)
                continue
            if '<span class="time day"' in message:

                day = message.split('<span class="time day">')[
                    1].split('</span>')[0]

                days[day] = content.index(message)

            count += 1

        self.soup = soup
        self.days = days
        self.id = data["id"]
        self.reported = self.get_player(data['user'])
        self.reason = data["reason"]
        self.details = data["details"]
        self.ranked = data['ranked']
        self.judgement = data['judgement']
        self.content = content

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

        if not self.name in [x["username"] for x in all_players]:
            raise ValueError("Report not found.")

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

    if role == "BodyGuard":
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
    elif role == "VampireHunter":
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
    elif role == "SerialKiller":
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
