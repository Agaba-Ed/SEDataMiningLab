
import requests
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
	
register_matplotlib_converters()

# Read the json data from the api
pull_request_url = 'https://api.github.com/repos/{}/pulls?state=all'
pull_request_data = []
repos = ['scottyab/rootbeer','Skyscanner/backpack','k9mail/k-9','mendhak/gpslogger']
count=0
for repo in repos:
    pull_request_url_repo = pull_request_url.format(repo)
    pull_request_data_repo = requests.get(pull_request_url_repo).json()
    pull_request_data.append(pull_request_data_repo)
    count+=1
    print("Received repos:"+ str(count)+"/"+str(len(repos)))

# Initialize the dataframe
pull_request_df = pd.DataFrame(columns=['repo', 'state', 'title', 'created_at', 'closed_at'])
for repo_data in pull_request_data:
	for pull_request in repo_data:
		pull_request_df = pull_request_df.append({
			'repo': pull_request['base']['repo']['full_name'], 
			'state': pull_request['state'], 
			'title': pull_request['title'], 
			'created_at': pull_request['created_at'], 
            'merged_at': pull_request['merged_at'],
			'closed_at': pull_request['closed_at']

			}, ignore_index=True)

# Convert the datetime strings to datetime objects
pull_request_df['created_at'] = pd.to_datetime(pull_request_df['created_at'], format='%Y-%m-%dT%H:%M:%SZ')
pull_request_df['closed_at'] = pd.to_datetime(pull_request_df['closed_at'], format='%Y-%m-%dT%H:%M:%SZ')
pull_request_df['merged_at'] = pd.to_datetime(pull_request_df['merged_at'], format='%Y-%m-%dT%H:%M:%SZ')

#Create a dataframe containing only merged pull requests
merged_pull_request_df = pull_request_df[pull_request_df['merged_at'].notnull()]

#Create a dataframe containing only closed pull requests and not merged
closed_pull_request_df = pull_request_df[pull_request_df['closed_at'].notnull() & pull_request_df['merged_at'].isnull()]

# Export all dataframes as csv files
path_to_csv_dir="F:\work\Software Metrics\sre\csv"
merged_pull_request_df.to_csv(r""+path_to_csv_dir+'\merged_pull_request_df.csv')
closed_pull_request_df.to_csv(r""+path_to_csv_dir+'\closed_pull_request_df.csv')

#Create graph 
fig, ax = plt.subplots()
ax.plot(merged_pull_request_df['created_at'], merged_pull_request_df['merged_at'], 'o', label='Merged')
ax.plot(closed_pull_request_df['created_at'], closed_pull_request_df['closed_at'], 'o', label='Closed')
ax.set_xlabel('Created at')
ax.set_ylabel('Closed at')  
ax.set_title('Merged and Closed(But Not Merged) Pull Requests')
ax.legend()
plt.show()


