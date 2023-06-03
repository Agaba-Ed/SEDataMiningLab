
import matplotlib.pyplot as plt
import pandas as pd


#function to calculate number of weeks between dates
def weeks_between(d1, d2):
    d1 = pd.to_datetime(d1)
    d2 = pd.to_datetime(d2)
    return abs((d2 - d1).days) // 7


author_file_touches_df = pd.read_csv("data/author_file_touches.csv")

min_date=author_file_touches_df['Date'].min()

#create new column with number of weeks between dates
author_file_touches_df['Weeks']=author_file_touches_df.apply(lambda row: weeks_between(min_date,row["Date"]),axis=1)

x=author_file_touches_df['Touches']
y=author_file_touches_df['Weeks']

#group by author
author_file_touches_grouped=author_file_touches_df.groupby('Author')

for name,group in author_file_touches_grouped:
        plt.scatter(group['Touches'],group['Weeks'],label=name)

plt.xlabel('Touches')
plt.ylabel('Weeks')
plt.title('Scatterplot of Weeeks vs Touches')
plt.legend()
plt.show()






