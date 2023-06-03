# Import necessary libraries
from gitconnect import GitWrapper  # for accessing the GitConnect API
import pandas as pd  # for working with data in DataFrames
from dotenv import load_dotenv  # for loading environment variables
import os  # for working with operating system functionalities

# Load environment variables from .env file
load_dotenv()

# Get the access token from environment variable
access_token = os.getenv("GITHUB_TOKEN")

# Create an instance of GitWrapper to interact with GitConnect API using access token
wrapper = GitWrapper(access_token)

# Define the owner and repository name
owner = "Agaba-Ed"
repo = "gitconnect"

# Define file extensions to keep track of
file_extensions = [".py"]

# Initialize empty list to store all the relevant files modified in the repo
source_files = []

# Get all the commits in the repository using GitConnect API
commits = wrapper.get_commits(owner, repo)

# Initialize dictionary to store Filename, Author, Date and Touches for each commit, in separate lists
dict = {'Filename':[],'Author':[],'Date':[],'Touches':[]}

# Loop through each commit in the repository
for commit in commits:
    # Get the sha key of the commit (using which one can get detailed commit information)
    commit_sha = commit['sha']
    
    # Get all the information about the changed files in the commit
    commit_files = wrapper.get_commit_files(owner, repo, commit_sha)
    
    # Add the file to source_files if its extension is of interest
    source_files += [file for file in commit_files if any(
        file['filename'].endswith(ext) for ext in file_extensions)]
        
# Loop through each file among the relevant files
for file in source_files:
    # Add filename of that file to dict
    dict['Filename'].append(file['filename'])
    # Add author of the commit who changed the file to dict
    dict['Author'].append(commit['commit']['author']['name'])
    # Add date of the commit when the file was changed to dict
    dict['Date'].append(commit['commit']['author']['date'])
    # Add number of lines(changed) in the file to dict
    dict['Touches'].append(file['changes'])

# Create a DataFrame using dictionary 'dict' and save as a CSV file
df=pd.DataFrame(data=dict)
df.to_csv('data/author_file_touches.csv',index=False)

# Print the first 5 rows of the data to check
print(df.head())



