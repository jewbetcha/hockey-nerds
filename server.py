from flask import Flask
from flask import request
from flask_cors import CORS
import statistics
import csv

app = Flask(__name__)
CORS(app)

@app.route('/goals-for-against', methods=['POST'])
def goals_for_against_avg():
	teams = request.json
	team_1 = teams['team_1']
	team_2 = teams['team_2']

	reader = csv.DictReader(open('./sample-data/teams.csv'))
	data = []
	for row in reader:
		data.append(row)

	out_data = {}

	for team in data:
		if team['Team'] == team_1:
			out_data[team_1] = team
		if team['Team'] == team_2:
			out_data[team_2] = team
	
	t1_gf_ga = float(out_data[team_1]['xGF/60']) + float(out_data[team_1]['xGA/60'])
	t2_gf_ga = float(out_data[team_2]['xGF/60']) + float(out_data[team_2]['xGA/60'])

	return {
		'average': str(statistics.mean([t1_gf_ga, t2_gf_ga])),
		'team_1': t1_gf_ga,
		'team_2': t2_gf_ga
	}


if __name__ == '__main__':
    app.run()