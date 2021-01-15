import requests

API_BASEURL = 'https://statsapi.web.nhl.com/api/v1'

SEASONS = ['20142015', '20152016', '20162017', '20172018', '20182019']
goals_per_game = []

def get_data():
	for season in SEASONS:
		team_data = requests.get(API_BASEURL + '/teams/14?expand=team.stats&season=' + season)
		json = team_data.json()
		goals_per_game.append(json['teams'][0]['teamStats'][0]['splits'][0]['stat']['goalsPerGame'])
	print(goals_per_game)



if __name__ == '__main__':
	get_data()