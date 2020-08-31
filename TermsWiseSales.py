# Terms Wise Sales - Donut Chart
# B.M. ASHIK MAHMUD

import pandas as pd
import pyodbc as db
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def numberInThousands(number):
    number = int(number / 1000)
    number = format(number, ',')
    number = number + 'K'
    return number


def numberInComma(number):
    number = int(number)
    number = format(number, ',')
    return number


conn = db.connect('DRIVER={SQL Server};'
                  'SERVER=10.168.2.163;'
                  'DATABASE=ARCCBD;'
                  'UID=sa;PWD=erp')

outstanding_df = pd.read_sql_query(""" 
                        Select 
                        SUM(case WHEN  TERMS = 'CASH' Then EXTINVMISC END ) as CASH,
                        SUM(case WHEN  TERMS not like '%CASH%'  Then EXTINVMISC END ) as CREDIT
                        from OESalesDetails

                        Where 
                        TRANSDATE between
                        (convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
                        AND
                        convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
                     """, conn)

cash = int(outstanding_df['CASH'])
credit = int(outstanding_df['CREDIT'])
data = [cash, credit]
print(cash, credit)

# Center Circle Text
results = cash + credit
print(results)
total = 'Total\n' + str(results)

# Define Color and lengend color
colors = ['#ff847c', '#f6cd61']
legend_element = [Patch(facecolor='#ff847c', label='Cash'),
                  Patch(facecolor='#f6cd61', label='Credit')]
# -------------------------

data_label = [cash, credit]
print(data_label)
#

fig1, ax = plt.subplots()
pack_all, label, percent_value = ax.pie(data, labels=data_label, colors=colors, autopct='%.1f%%', textprops={
    'color': "Black"}, startangle=90, pctdistance=.8)
ax.text(0, -.1, total, ha='center', fontsize=18, color='#d92027', fontweight='bold')
plt.setp(percent_value, fontsize=12, color='#120136', fontweight='bold')
plt.setp(label, fontsize=16, color='#035aa6', fontweight='bold')

# Center Circle and
centre_circle = plt.Circle((0, 0), 0.50, fc='white')
fig1.gca().add_artist(centre_circle)

plt.title('Terms Wise Sales', fontsize=16, fontweight='bold', color='#303960')
ax.axis('equal')
plt.legend(handles=legend_element, loc='upper left', fontsize=11)
plt.tight_layout()
plt.savefig('F:/PythonProject/CBD-KPI/img/terms-wise-sales.png')
plt.show()
