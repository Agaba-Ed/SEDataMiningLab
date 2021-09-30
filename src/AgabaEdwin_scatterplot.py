'''
 write a script that generates a scatterplot (using matplotlib) of weeks vs file variables 
 where the points are shaded according to author variable.
  Each author should have a distinct color.
'''

import matplotlib.pyplot as plt
import pandas as pd

from AgabaEdwin_authorsFileTouches import authorsFileTouches

filepath=r"F:\work\Software Metrics\sre\csv\file_AuthorsFileTouches.csv"

def main():
    author_file_touches=pd.read_csv(filepath)

    #get maximum and minimum date for each column in dataframe
    max_date=author_file_touches['Date'].max()
    min_date=author_file_touches['Date'].min()
    
    #create new column with number of weeks between dates
    author_file_touches['Weeks']=author_file_touches.apply(lambda row: weeks_between(row['Date'],max_date),axis=1)
    author_file_touches.to_csv(r"F:\work\Software Metrics\sre\csv\file_AuthorsFileTouches_withWeeks.csv")

    x=author_file_touches['Touches']
    y=author_file_touches['Weeks']


    #group by author
    author_file_touches_grouped=author_file_touches.groupby('Author')

    for name,group in author_file_touches_grouped:
        plt.scatter(group['Touches'],group['Weeks'],label=name)

    plt.xlabel('Touches')
    plt.ylabel('Weeks')
    plt.title('Scatterplot of Weeeks vs Touches')
    plt.legend()
    plt.show()




#function to calculate number of weeks between dates
def weeks_between(d1, d2):
    d1 = pd.to_datetime(d1)
    d2 = pd.to_datetime(d2)
    return abs((d2 - d1).days) // 7

if __name__=='__main__':
    main()





