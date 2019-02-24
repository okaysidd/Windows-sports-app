import requests
from bs4 import BeautifulSoup
import lxml


LEAGUES = {
        1 : 'http://www.espn.in/football/teams/_/league/esp.1',
        2 : 'http://www.espn.in/football/teams',
        3 : 'http://www.espn.in/football/teams/_/league/ger.1',
        4 : 'http://www.espn.in/football/teams/_/league/ita.1',
        5 : 'http://www.espn.in/football/teams/_/league/fra.1',
        'la liga' : 'http://www.espn.in/football/teams/_/league/esp.1',
        'english premier league' : 'http://www.espn.in/football/teams',
        'bundesliga' : 'http://www.espn.in/football/teams/_/league/ger.1',
        'serie A' : 'http://www.espn.in/football/teams/_/league/ita.1',
        'ligue 1' : 'http://www.espn.in/football/teams/_/league/fra.1',
        }


def get_all_leagues(choice=None):
    if choice and choice.isdigit():
        return LEAGUES[int(choice)]
    else:
        print('Which league does your favourite team play in?\nYou can pick a number or league name')
        print('1. La Liga')
        print('2. English Premier League')
        print('3. Bundesliga')
        print('4. Serie A')
        print('5. Ligue 1')
        league = input().lower()
        if league.isdigit():
            return LEAGUES[int(league)]
        elif league in LEAGUES.keys():
            return LEAGUES[league]


def get_all_teams(league):
    source = requests.get(league).text
    soup = BeautifulSoup(source, 'lxml')
    all_teams = soup.find_all('section', class_='TeamLinks flex items-center')
    team_list = {}
    for team in range(len(all_teams)):
         team_name = all_teams[team].find_all('div', class_='pl3')[0].find('h2').text
         team_id = all_teams[team].find_all('a')[0]['href'].split('id/')[1].split('/')[0]
         team_list[team_name] = team_id
    return team_list


def set_team(team_id):
    espn_link = 'https://www.espn.in/football/team/_/id/' + team_id + '/'
    source = requests.get(espn_link).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def get_games(soup, team_name):
    output = team_name + '\n' + '\n'
    games_section = soup.find('section', class_='col-a chk-height')
    list_of_games = games_section.find_all('li')
    for game in range(0, 5):
        competetion_name = list_of_games[game].find_all('div', class_='league-name-short')[0].text
        if list_of_games[game].find_all('div', class_='game-status'):
            game_status = list_of_games[game].find_all('div', class_='game-status')
            if len(game_status) > 3:
                game_status = game_status[3].text
                competetion_name += '-' + game_status
        team_a = list_of_games[game].find_all('div', class_='team-a')
        team_a_name = team_a[0].find_all('span', 'abbrev')[0].text
        team_b = list_of_games[game].find_all('div', class_='team-b')
        team_b_name = team_b[0].find_all('span', 'abbrev')[0].text
        if game == 0:
            if list_of_games[0].find_all('div', class_='game-date'):
                time = list_of_games[0].find_all('div', class_='game-date')[0].text
                result = 'To be played on ' + time
            elif list_of_games[0].find_all('span', class_='game-time') and list_of_games[0].find_all('span', class_='score'):
                time = 'Live'
                score = list_of_games[0].find_all('span', class_='score')
                result = 'Going on. Current score: ' + score[0].text + '-' + score[1].text
            else:
                if list_of_games[0].find_all('span', class_='game-time'):
                    time = list_of_games[0].find_all('span', class_='game-time')[0].text
                    result = time
                elif list_of_games[0].find_all('div', class_='game-date'):
                    time = list_of_games[0].find_all('div', class_='game-date')[0].text
                    result = time
            output += '--Next match--' + '\n'
            output += '{} vs {} in the {}. {}\n'.format(team_a_name, team_b_name, competetion_name, result) + '\n'
            output += '--Previous match results--' + '\n'
        else:
            score = list_of_games[game].find_all('span', class_='score')
            result = 'Final score: ' + score[0].text + '-' + score[1].text
            output += '{} vs {} in the {}. {}'.format(team_a_name, team_b_name, competetion_name, result) + '\n'
    return output


if __name__ == "__main__":
    league = get_all_leagues()
    team_list = get_all_teams(league)
    print('Select a team:')
    for team in team_list:
        print(team)
    team_name = input()
    soup = set_team(team_list[team_name])
    output = get_games(soup, team_name)
    print(output)
