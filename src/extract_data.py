
from gitconnect import GitWrapper
import csv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

access_token = os.getenv("GITHUB_TOKEN")
wrapper = GitWrapper(access_token)

owner = "Agaba-Ed"
repo = "gitconnect"
file_extensions = [".py"]

commits = wrapper.get_commits(owner, repo)
source_files = []
dictfiles = {}

for commit in commits:
    commit_sha = commit['sha']
    commit_files = wrapper.get_commit_files(owner, repo, commit_sha)
    source_files += [file for file in commit_files if any(
        file['filename'].endswith(ext) for ext in file_extensions)]
for file in source_files:
    name = file['filename']
    dictfiles[name] = dictfiles.get(name, 0)+1
    print(name)

with open('data/source_files.csv', 'w') as f:
    print('Total number of files: ' + str(len(dictfiles)))
    rows = ["Filename", "Touches"]
    writer = csv.writer(f)
    writer.writerow(rows)
    bigcount = None
    bigfilename = None
    for filename, count in dictfiles.items():
        rows = [filename, count]
        writer.writerow(rows)
        if bigcount is None or count > bigcount:
            bigcount = count
            bigfilename = filename
    f.close()
    print('The file ' + bigfilename +
          ' has been touched ' + str(bigcount) + ' times.')