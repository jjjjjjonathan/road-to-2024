from bs4 import BeautifulSoup
import requests
import json
import csv


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


def write_schedule_to_json(csv_file, starting_match_id, division_id, outfile):
    with open(csv_file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader, None)
        pk = starting_match_id
        matches = []
        for e2e_id, home_id, away_id, date, time in reader:
            match = {
                "e2e_id": int(e2e_id),
                "home_team": int(home_id),
                "away_team": int(away_id),
                "scheduled_time": f"{date} {time}",
            }
            matches.append(write_match_to_json(match, pk, division_id))
            pk += 1

        json_object = json.dumps(matches, indent=4)
        with open(outfile, "w") as outfile:
            outfile.write(json_object)


def write_match_to_json(match, pk, division_id):
    match_to_write = {
        "model": "l1o.match",
        "pk": pk,
        "fields": {
            "home_team": match["home_team"],
            "away_team": match["away_team"],
            "division": division_id,
            "e2e_id": match["e2e_id"],
            "scheduled_time": match["scheduled_time"],
        },
    }
    return match_to_write


MENS_TEAMS = "https://www.league1ontario.com/standings/show/7089232?subseason=809614"

WOMENS_TEAMS = "https://www.league1ontario.com/standings/show/7089244?subseason=809616"

# get_2022_teams(MENS_TEAMS, WOMENS_TEAMS)

write_schedule_to_json(
    "schedules/2023_mens_schedule.csv", 1, 1, "l1o/fixtures/3_mens_matches.json"
)

write_schedule_to_json(
    "schedules/2023_womens_schedule.csv", 211, 2, "l1o/fixtures/4_womens_matches.json"
)
