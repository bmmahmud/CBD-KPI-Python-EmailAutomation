# B.M. ASHIK MAHMUD
# Top 10 Item Sales

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
top 5
ICItem_ShortName.ShortName as Item,
SUM(EXTINVMISC) as Sales
from OESalesDetails
Left Join ICItem_ShortName on ICItem_ShortName.FMTITEMNO = OESalesDetails.ITEM
Where 
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
and TRANSTYPE = 1
Group By ICItem_ShortName.ShortName
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

bar_index = np.arange(len(data['Item']))
print(bar_index)

color = ['#d54062', '#0f4c75', '#ff5722', 'blue', 'orange', '#af5800']
# create plot
fig, ax = plt.subplots()

bar_width = .7
opacity = 0.9


bar1 = plt.barh(bar_index, data['Sales'], align='center', alpha=0.8, color=color)

for i, v in enumerate(data['Sales']):
    ax.text(v + 3, i + .25, str(thousand_K_number_decorator(int(v))), color='blue', fontweight='bold')

plt.yticks(bar_index, data['Item'])
plt.ylabel('Items')
plt.title('Top 5 Item Wise Sales MTD')
plt.tight_layout()
plt.savefig('F:/PythonProject/CBD-KPI/img/item-wise-sales.png')
plt.show()