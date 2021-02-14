import statistics
import csv
import pprint
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Ridge

def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep]

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

def adjusted_plus_minus_hockey(data_file):
	df = pd.read_csv(data_file, skiprows=1, names=['date', 'visitor', 'visitor_goals', 'home', 'home_goals'])
	df = clean_dataset(df)

	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
	df['goal_difference'] = df['home_goals'] - df['visitor_goals']

	df['home_win'] = np.where(df['goal_difference'] > 0, 1, 0)
	df['home_loss'] = np.where(df['goal_difference'] < 0, 1, 0)


	df_visitor = pd.get_dummies(df['visitor'], dtype=np.int64)
	df_home = pd.get_dummies(df['home'], dtype=np.int64)

	df_model = df_home.sub(df_visitor) 
	df_model['goal_difference'] = df['goal_difference']

	df_train = df_model

	lr = Ridge(alpha=0.001) 
	X = df_train.drop(['goal_difference'], axis=1)
	y = df_train['goal_difference']
	lr.fit(X, y)

	df_ratings = pd.DataFrame(data={'team': X.columns, 'rating': lr.coef_})
	print(df_ratings.sort_values(by=['rating']))

# TODO: add stats and asjusted_plus_minus for basketball too

def adjusted_plus_minus_basketball(data_file):
	cleaned_file = pd.read_csv(data_file)
	columns_to_keep = ['Visitor', 'visitor_pts', 'Home', 'home_pts']
	cleaned_file = cleaned_file[columns_to_keep]
	file = cleaned_file.to_csv('./sample-data/out.csv')
	df = pd.read_csv('./sample-data/out.csv', skiprows=1, names=['date','visitor', 'visitor_goals', 'home', 'home_goals'])

	df['goal_difference'] = df['home_goals'] - df['visitor_goals']

	df['home_win'] = np.where(df['goal_difference'] > 0, 1, 0)
	df['home_loss'] = np.where(df['goal_difference'] < 0, 1, 0)


	df_visitor = pd.get_dummies(df['visitor'], dtype=np.int64)
	df_home = pd.get_dummies(df['home'], dtype=np.int64)

	df_model = df_home.sub(df_visitor) 
	df_model['goal_difference'] = df['goal_difference']

	
	df_train = df_model

	lr = Ridge(alpha=0.001) 
	X = df_train.drop(['goal_difference'], axis=1)
	y = df_train['goal_difference']
	lr.fit(X, y)

	df_ratings = pd.DataFrame(data={'team': X.columns, 'rating': lr.coef_})
	print(df_ratings.sort_values(by=['rating']))

if __name__ == '__main__':
	adjusted_plus_minus_hockey('./sample-data/2021data.csv')
	# adjusted_plus_minus_basketball('./sample-data/2021_basketball_data.csv')