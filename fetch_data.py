import statistics
import csv
import pprint
import sys


def goals_for_against_avg():
	reader = csv.DictReader(open('./sample-data/teams.csv'))
	data = []
	for row in reader:
		data.append(row)

	team_1 = sys.argv[1]
	team_2 = sys.argv[2]
	out_data = {}

	for team in data:
		if team['Team'] == team_1:
			out_data[team_1] = team
		if team['Team'] == team_2:
			out_data[team_2] = team
	
	t1_gf_ga = float(out_data[team_1]['xGF/60']) + float(out_data[team_1]['xGA/60'])
	t2_gf_ga = float(out_data[team_2]['xGF/60']) + float(out_data[team_2]['xGA/60'])
	print(team_1 + ': ' + str(t1_gf_ga) + ', ' + team_2 + ': ' + str(t2_gf_ga) + ', AVG: ' + str(statistics.mean([t1_gf_ga, t2_gf_ga])))




if __name__ == '__main__':
	goals_for_against_avg()