# B.M. ASHIK MAHMUD
# Brand Wise Stock

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
Select 
RTRIM(BRAND.VDESC) as Brand,
SUM(QTYONHAND) AS Stock
from ICHistoricalStock
Left JOIN BRAND ON BRAND.[VALUE]=ICHistoricalStock.BRAND
Where 
AUDTDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
Group By BRAND.VDESC
Order By SUM(QTYONHAND) ASC

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


bar_index = np.arange(len(data['Brand']))
print(bar_index)

color = ['#00b7c2', '#59405c', '#dd2c00', '#e7305b', '#f09ae9', '#af5800']
# create plot
fig, ax = plt.subplots()

bar_width = .7
opacity = 0.9

#  bar1 = plt.bar(bar_index, data['Sales'], bar_width,alpha=.8, color=color)
#--------------------------------------------------------------------

bar1 = plt.barh(bar_index, data['Stock'], align='center', alpha=0.9, color=color)




# def autolabel(bar1):
#     for bar in bar1:
#         height = int(bar.get_height())
#         ax.text(bar.get_x() + bar.get_width() / 2., .995 * height,
#                 for_bar(height),
#                 ha='center', va='bottom', fontsize=9, fontweight='bold')
#
# autolabel(bar1)
intergers = data['Stock'].astype(int) # Convert float to interger

for i, v in enumerate(intergers):
    ax.text(v, i + .05, str(v), color='blue', fontweight='bold')

# plt.bar(bar_index, data['LIVE_SALES'], align='center', alpha=.6, color=color) # total_bar = totall bar, sales Bar hight,
# plt.xticks(bar_index, data['Branch'],rotation=90, ha='right')
plt.yticks(bar_index, data['Brand'])
plt.ylabel('Brands')
plt.title('Brand Wise Stock MTD')
plt.tight_layout()
plt.show()