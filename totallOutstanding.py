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
select
OESales.SalesCash+ARReceive.ReceiveCash as Cash,
OESales.SalesCredit+ARReceive.ReceiveCredit as Credit
from
(select 
SUM(CASE WHEN TERMS='CASH' THEN invneth END) AS SalesCash,
SUM(CASE WHEN TERMS not like '%CASH%' THEN invneth END) AS SalesCredit
from OESalesSummery
where TRANSDATE between 19650101 and convert(varchar(8),DATEADD(D,0,GETDATE()-1),112) ) 
as OESales,

(select
SUM(CASE WHEN TERMS='CASH' THEN docnet END) AS ReceiveCash,
SUM(CASE WHEN TERMS not like '%CASH%' THEN docnet END) AS ReceiveCredit
from ARReceiptAdjustment 
where docdate between 19650101 and convert(varchar(8),DATEADD(D,0,GETDATE()-1),112)) 
as ARReceive
""", conn)

cash = int(outstanding_df['Cash'])
credit = int(outstanding_df['Credit'])
data = [cash, credit]
print(cash, credit)

# Center Circle Text
results = cash + credit
print(results)
total = 'Total\n' + str(results)

# Define Color and lengend color
colors = ['#fa7d09', '#aacfcf']
legend_element = [Patch(facecolor='#fa7d09', label='Cash'),
                  Patch(facecolor='#aacfcf', label='Credit')]
# -------------------------

data_label = [cash, credit]
print(data_label)
#

fig1, ax = plt.subplots()
pack_all, label, percent_value = ax.pie(data, labels=data_label, colors=colors, autopct='%.1f%%', textprops={
    'color': "Black"}, startangle=90, pctdistance=.8)
ax.text(0, -.1, total, ha='center', fontsize=18, color='#d92027', fontweight='bold')
plt.setp(percent_value, fontsize=12, color='#120136', fontweight='bold')
plt.setp(label, fontsize=10, color='#035aa6', fontweight='bold')

# Center Circle and
centre_circle = plt.Circle((0, 0), 0.50, fc='white')
fig1.gca().add_artist(centre_circle)

plt.title('Total Outstanding', fontsize=14, fontweight='bold', color='#303960')
ax.axis('equal')
plt.legend(handles=legend_element, loc='upper left', fontsize=11)
plt.tight_layout()
plt.savefig('F:/PythonProject/CBD-KPI/img/total-Outstanding.png')
plt.show()
