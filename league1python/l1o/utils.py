from bs4 import BeautifulSoup
import requests
import json


def get_2022_teams(mens_standings_url, womens_standings_url):
    mens_r = requests.get(mens_standings_url)
    mens_soup = BeautifulSoup(mens_r.text, "html.parser")
    mens_teams = (
        mens_soup.find("table", class_="statTable").find("tbody").find_all("tr")
    )

    team_list = []
    pk = 1
    for team in mens_teams:
        team_list.append(write_team_json(team, 1, pk))
        pk += 1

    womens_r = requests.get(womens_standings_url)
    womens_soup = BeautifulSoup(womens_r.text, "html.parser")
    womens_teams = (
        womens_soup.find("table", class_="statTable").find("tbody").find_all("tr")
    )

    for team in womens_teams:
        team_list.append(write_team_json(team, 2, pk))
        pk += 1

    json_object = json.dumps(team_list, indent=4)

    with open("l1o/fixtures/2_teams.json", "w") as outfile:
        outfile.write(json_object)

    print("List of teams now in l1o/fixtures/2_teams.json")


def write_team_json(team, division_id, team_id):
    team_to_write = {
        "model": "l1o.team",
        "pk": team_id,
        "fields": {
            "name": team.find("a", class_="teamName").get_text(),
            "points_in_2022": int(team.find("td", class_="highlight").get_text()),
            "division": division_id,
        },
    }
    return team_to_write


MENS_TEAMS = "https://www.league1ontario.com/standings/show/7089232?subseason=809614"

WOMENS_TEAMS = "https://www.league1ontario.com/standings/show/7089244?subseason=809616"

get_2022_teams(MENS_TEAMS, WOMENS_TEAMS)
