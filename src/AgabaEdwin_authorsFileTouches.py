'''First, write a script with the name <'your_firstname'_authorsFileTouches.py> that collects the authors 
 and the dates when they touched for each file in the list of files generated 
by the adapted file CollectFiles.py (only source files).
'''


from pandas.core.reshape.merge import merge
from AgabaEdwin_CollectFiles import CollectFiles as cf
import pandas as pd



author_file_touches_path=r"F:\work\Software Metrics\sre\csv\file_RootBeerFileTouches.csv"
sharing_app_path=r"F:\work\Software Metrics\sre\csv\file_rootbeer.csv"

def authorsFileTouches():
    """
    This function collects the authors and the dates when they touched for each file in the list of files generated 
    by the adapted file CollectFiles.py (only source files).
    """

    
    collector=cf()
    shaobjects=collector.getsha_objects(collector.lsttokens,collector.repo)
    d={'Filename':[],'Author':[],'Date':[]}
    for shaobj in shaobjects:
        fileObjs=shaobj['files']
        for filenameObj in fileObjs:
            # if the file is not a java,C, C++ or CMake file, skip it
            if filenameObj['filename'].endswith('.java') or filenameObj['filename'].endswith('.c') or filenameObj['filename'].endswith('.cpp') or filenameObj['filename'].endswith('.cmake'):
                d['Filename'].append(filenameObj['filename'])  
                d['Author'].append(shaobj['commit']['author']['name'])
                d['Date'].append(shaobj['commit']['author']['date'])     
       
    
    
    df=pd.DataFrame(data=d)
    root_beer=pd.read_csv(sharing_app_path)

    #merge the files based on Filename column
    authors_file_touches=merge(df,root_beer,on='Filename')
    authors_file_touches.to_csv(author_file_touches_path,index=False)

    print("Task completed....")
    




if __name__ == "__main__":
    authorsFileTouches()
