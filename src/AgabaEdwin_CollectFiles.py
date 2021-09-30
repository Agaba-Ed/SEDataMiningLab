
import json
import requests
import csv


class CollectFiles:
    def __init__(self):
        self.dictfiles = {}
        self.lsttokens = ["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"]
        self.repo = 'Agaba-Ed/SharingApp'
        self.filepath=r"F:\work\Software Metrics\sre\csv\file_SharingApp.csv"
        self.fileobjs = []
        self.commits=[]
        self.sha_objects=[]
        self.file_objects=[]
        self.sourcefiles=[]

    
    # GitHub Authentication function
    def github_auth(self,url, lsttokens, ct):
        jsonData = None
        try:
            ct = ct % len(lsttokens)
            headers = {'Authorization': 'Bearer {}'.format(lsttokens[ct])}
            request = requests.get(url, headers=headers)
            jsonData = json.loads(request.content)
            ct += 1
        except Exception as e:
                pass
                print(e)
                exit(0)
        return jsonData, ct

    # @dictFiles, empty dictionary of files
    # @lstTokens, GitHub authentication tokens
    # @repo, GitHub repo
    def getsha_objects(self, lsttokens, repo):
        ipage = 1  # url page counter
        ct = 0  # token counter
        sourcefiles=[]
        
        try:
            # loop though all the commit pages until the last returned empty page
            while True:
                spage = str(ipage)
                commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
                jsonCommits, ct = self.github_auth(commitsUrl, lsttokens, ct)
                
                # break out of the while loop if there are no more commits in the pages
                if len(jsonCommits) == 0:
                     break
                # iterate through the list of commits in  spage
                for shaObject in jsonCommits:
                    sha = shaObject['sha']
                    # For each commit, use the GitHub commit API to extract the files touched by the commit
                    shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                    shaDetails, ct = self.github_auth(shaUrl, lsttokens, ct)
                    self.sha_objects.append(shaDetails) 
                    '''

                    '''
                ipage += 1
        except Exception as e:
            print(e)
            exit(0)
        
        return self.sha_objects

    def getcommits(self):
        sha_objects=self.getsha_objects(self.lsttokens,self.repo)
        for shaobj in sha_objects:
            self.commits.append[shaobj['commit']]
        return self.commits
    
    def getfileobjects(self):
        sha_objects=self.getsha_objects(self.lsttokens,self.repo)
        for shaobj in sha_objects:
            filenameObj=shaobj['files']
            self.file_objects.append(filenameObj)  
        return self.file_objects

    def getsourcefiles(self):
        
        fileobjs=self.getfileobjects()
        for files in fileobjs:
            for filenameObj in files:
                 # if the file is not a java,C, C++ or CMake file, skip it
                 if filenameObj['filename'].endswith('.java') or filenameObj['filename'].endswith('.c') or filenameObj['filename'].endswith('.cpp') or filenameObj['filename'].endswith('.cmake'):
                     self.sourcefiles.append(filenameObj)
        return self.sourcefiles



    def countfiles(self,dictfiles):
        sourceFiles=self.getsourcefiles()
        for file in sourceFiles:
            filename=file['filename']
            dictfiles[filename]=dictfiles.get(filename,0)+1
            print(filename)

    def write_to_csv(self, filepath,dictfiles,repo):
        with open(filepath, 'w') as f:
            print('Total number of files: ' + str(len(dictfiles)))
            file = repo.split('/')[1]
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
            print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')

           
    def main(self):
        #self.getfileobjects()
        #self.getsourcefiles()   
        self.countfiles(self.dictfiles)
        self.write_to_csv(self.filepath,self.dictfiles,self.repo)

if __name__ == '__main__':
    CollectFiles().main()