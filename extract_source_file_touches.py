# Import necessary libraries
from gitconnect import GitWrapper  # for accessing the GitConnect API
import csv  # for working with CSV files
from dotenv import load_dotenv  # for loading environment variables
import os  # for working with operating system functionalities

# Load environment variables from .env file
load_dotenv()

# Get the access token from environment variable
access_token = os.getenv("GITHUB_TOKEN")

# Create an instance of GitWrapper to interact with GitConnect API using the access token
wrapper = GitWrapper(access_token)

# Define the owner and repository name
owner = "Agaba-Ed"
repo = "gitconnect"

# Define file extensions to keep track of
file_extensions = [".py"]

# Get all the commits in the repository using GitConnect API
commits = wrapper.get_commits(owner, repo)

# Initialize an empty list to store all the relevant files modified in the repo
source_files = []

# Initialize a dictionary to keep track of the number of changes on each file
dictfiles = {}

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
    name = file['filename']
    dictfiles[name] = dictfiles.get(name, 0)+1  # Increment the touch counter for the file (or initialize it to 1 if it hasn't been seen before)
    print(name)

# Write the data to a CSV file
with open('data/source_files.csv', 'w') as f:
    print('Total number of files: ' + str(len(dictfiles)))  # Print the total number of files to the console
    rows = ["Filename", "Touches"]
    writer = csv.writer(f)
    writer.writerow(rows)
    bigcount = None
    bigfilename = None
    for filename, count in dictfiles.items():
        rows = [filename, count]
        writer.writerow(rows)
        if bigcount is None or count > bigcount:  # Find the file that has been touched the most times
            bigcount = count
            bigfilename = filename
    f.close()
    # Print the result to the console
    print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
