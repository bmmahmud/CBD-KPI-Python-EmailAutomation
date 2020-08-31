# B.M. ASHIK MAHMUD
# Top 10 Customer Wise Sales

import pandas as pd
import pyodbc as db
from matplotlib import pyplot as plt
import numpy as np

## Create Database connection ---------

connection = db.connect(
    'DRIVER={SQL SERVER};'
    # 'SERVER=137.116.139.217;'
    'SERVER=10.168.2.163;'
    'DATABASE=ARCCBD;'
    # 'UID=sa;PWD=erp@123'
    'UID=sa;PWD=erp'
    )
query = """
select
top 10 
CUSTNAME as  CUSTNAME,
SUM(EXTINVMISC) as Sales
From OESalesDetails
Where 
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
Group By CUSTNAME
Order By SUM(EXTINVMISC) Desc 
"""
data = pd.read_sql_query(query, connection)
print(data)

# -------------------Bar Charts---------------------------------
def number_decorator(number):
    number = round(number, 1)
    number = format(number, ',')
    number = number + ' K'
    return number

def for_bar(number):
    number = round(number, 1)
    number = format(number, ',')
    number = number + 'K'
    return number
def thousand_K_number_decorator(number):
    number = int(number / 1000)
    number = format(number, ',')
    number = number + 'K'
    return number


bar_index = np.arange(len(data['CUSTNAME']))
print(bar_index)

color = ['#00b7c2', '#59405c', '#dd2c00', '#e7305b', '#f09ae9', '#af5800']
# create plot
fig, ax = plt.subplots()

bar_width = .7
opacity = 0.9

#  bar1 = plt.bar(bar_index, data['Sales'], bar_width,alpha=.8, color=color)
#--------------------------------------------------------------------

bar1 = plt.barh(bar_index, data['Sales'], align='center', alpha=0.9, color=color)




# def autolabel(bar1):
#     for bar in bar1:
#         height = int(bar.get_height())
#         ax.text(bar.get_x() + bar.get_width() / 2., .995 * height,
#                 for_bar(height),
#                 ha='center', va='bottom', fontsize=9, fontweight='bold')
#
# autolabel(bar1)
for i, v in enumerate(data['Sales']):
    ax.text(v + 3, i + .25, str(thousand_K_number_decorator(int(v))), color='blue', fontweight='bold')

# plt.bar(bar_index, data['LIVE_SALES'], align='center', alpha=.6, color=color) # total_bar = totall bar, sales Bar hight,
# plt.xticks(bar_index, data['Branch'],rotation=90, ha='right')
plt.yticks(bar_index, data['CUSTNAME'])
plt.ylabel('Customers')
plt.title('Top 10 Customer Wise Sales MTD')
plt.tight_layout()
plt.savefig('F:/PythonProject/CBD-KPI/img/customer-wise-sales.png')
plt.show()