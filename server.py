from flask import Flask
from flask import request
from flask_cors import CORS
import statistics
import csv
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Ridge

app = Flask(__name__)
CORS(app)

@app.route('/goals-for-against', methods=['POST'])
def goals_for_against_avg():
	teams = request.json
	team_1 = teams['team_1']
	team_2 = teams['team_2']

	reader = csv.DictReader(open('./sample-data/teams1.csv'))
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

@app.route('/adjusted-plus-minus', methods=['POST'])
def adjusted_plus_minus():
	df = pd.read_csv('./sample-data/test.csv', skiprows=1, names=['date', 'visitor', 'visitor_goals', 'home', 'home_goals'])

	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
	df['goal_difference'] = df['home_goals'] - df['visitor_goals']
	df['home_win'] = np.where(df['goal_difference'] > 0, 1, 0)
	df['home_loss'] = np.where(df['goal_difference'] < 0, 1, 0)
	df_visitor = pd.get_dummies(df['visitor'], dtype=np.int64)
	df_home = pd.get_dummies(df['home'], dtype=np.int64)
	df_model = df_home.sub(df_visitor) 
	df_model['goal_difference'] = df['goal_difference']
	lr = Ridge(alpha=0.001) 
	X = df_train.drop(['goal_difference'], axis=1)
	y = df_train['goal_difference']

	lr.fit(X, y)
	df_ratings = pd.DataFrame(data={'team': X.columns, 'rating': lr.coef_})


if __name__ == '__main__':
    app.run()