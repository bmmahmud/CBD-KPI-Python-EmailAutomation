import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import pyodbc as db

# Formate
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
    number = int((number*-1) / 1000)
    number = format(number, ',')
    number = number + 'K'
    return number
# Database Start
connection = db.connect(
    'DRIVER={SQL SERVER};'
    # 'SERVER=137.116.139.217;'
    'SERVER=10.168.2.163;'
    'DATABASE=ARCCBD;'
    # 'UID=sa;PWD=erp@123'
    'UID=sa;PWD=erp'
    )
YTDReturnAmount = """
--YTD Return
select 
case when sum(EXTINVMISC) <> 0 Then sum(EXTINVMISC) ELSE 0 
END as YTDReturnAmount 
from OESalesDetails where
transtype<>1 and PRICELIST <> 0 and
(TRANSDATE between convert(varchar(6),DATEADD(yy, DATEDIFF(yy, 0, GETDATE()), 0),112)
and (convert(varchar(8),DATEADD(D,-1,GETDATE()),112)))
"""
LDReturnAmount = """
--Last Day Return
select 
case when sum(EXTINVMISC) <> 0 Then sum(EXTINVMISC) ELSE 0 
END as LDReturnAmount
from OESalesDetails where
transtype<>1 and PRICELIST <> 0 and
TRANSDATE = convert(varchar(8),getdate()-1,112)
"""
ReturnAmountsql = """
--Last  MTDReturn
select sum(EXTINVMISC) as ReturnAmount from OESalesDetails where
transtype<>1 and PRICELIST <> 0 and
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
"""
YTDReturnAmount = pd.read_sql_query(YTDReturnAmount, connection)
LDReturnAmount = pd.read_sql_query(LDReturnAmount, connection)
ReturnAmount = pd.read_sql_query(ReturnAmountsql, connection)
print(YTDReturnAmount["YTDReturnAmount"])
print(LDReturnAmount["LDReturnAmount"])
print(ReturnAmount["ReturnAmount"])
# Database END



####BOX 1 RND
# # Box 1
# left, width = 0.0, 0.32
# bottom, height = 0,1
# right = left + width
# top = 1
# fig = plt.figure(figsize=(12,2))
# ax = fig.add_axes([0,0,1,1])
#
# #----------------------- remove border from the figure
# for item in [fig,ax]:
#     item.patch.set_visible(False)
#     fig.patch.set_visible(False)
#     ax.axis('off')
#
#
# #---------------------------------
# p = patches.Rectangle( (left,bottom),width,height,color = '#f0a500')
# ax.add_patch(p)
# # plt.show()
# value =thousand_K_number_decorator(YTDReturnAmount["YTDReturnAmount"])
# kpi_lable = 'LD'
# return_p = value
# ax.text(0.5 * (left + right), 0.55 * (bottom + top), kpi_lable,
#         ha = 'center',va = 'center',
#         fontsize=24, color='black',
#         transform = ax.transAxes)
#
# ax.text(0.5 * (left + right), 0.3 * (bottom + top), return_p,
#         ha = 'center',va = 'center',
#         fontsize=24, color='red',
#         transform = ax.transAxes)
# #

# Box 1
left, width = 0.0, 0.32
bottom, height = 0,1
right = left + width
top = 1
fig = plt.figure(figsize=(12,2))
ax = fig.add_axes([0,0,1,1])

#----------------------- remove border from the figure
for item in [fig,ax]:
    item.patch.set_visible(False)
    fig.patch.set_visible(False)
    ax.axis('off')


#---------------------------------
p = patches.Rectangle( (left,bottom),width,height,color = '#f0a500')
ax.add_patch(p)
# plt.show()
value = thousand_K_number_decorator(LDReturnAmount["LDReturnAmount"])
# LDReturnAmount = thousand_K_number_decorator(LDReturnAmount["LDReturnAmount"])
# print(LDReturnAmount)
kpi_lable = 'LD'
return_p = value
ax.text(0.5 * (left + right), 0.55 * (bottom + top), kpi_lable,
        ha = 'center',va = 'center',
        fontsize=24, color='black',
        transform = ax.transAxes)

ax.text(0.5 * (left + right), 0.3 * (bottom + top), return_p,
        ha = 'center',va = 'center',
        fontsize=24, color='red',
        transform = ax.transAxes)

# # Box 2
left, width = 0.33, 0.32
bottom, height = 0,1
right = left + width
top = 1

p = patches.Rectangle((left,bottom),width,height,color = '#21bf73')
ax.add_patch(p)
# plt.show()
ReturnAmount = thousand_K_number_decorator(ReturnAmount["ReturnAmount"])
print(ReturnAmount)
kpi_lable = 'MTD'
return_p = ReturnAmount
ax.text(0.5 * (left + right), 0.55 * (bottom + top), kpi_lable,
        ha = 'center',va = 'center',
        fontsize=24, color='black',
        transform = ax.transAxes)

ax.text(0.5 * (left + right), 0.3 * (bottom + top), return_p,
        ha = 'center',va = 'center',
        fontsize=24, color='red',
        transform = ax.transAxes)

# # Box 3
left, width = 0.66, 0.34
bottom, height = 0,1
right = left + width
top = 1

p = patches.Rectangle((left,bottom),width,height,color = '#fbc687')
ax.add_patch(p)
# plt.show()
YTDReturnAmount = thousand_K_number_decorator(YTDReturnAmount["YTDReturnAmount"])
print(YTDReturnAmount)
kpi_lable = 'YTD'
return_p = YTDReturnAmount
ax.text(0.5 * (left + right), 0.55 * (bottom + top), kpi_lable,
        ha = 'center',va = 'center',
        fontsize=24, color='black',
        transform = ax.transAxes)

ax.text(0.5 * (left + right), 0.3 * (bottom + top), return_p,
        ha = 'center',va = 'center',
        fontsize=24, color='red',
        transform = ax.transAxes)
# Save Images
# # # Box 4
# left, width = 0.60, .19
# bottom, height = 0,1
# right = left + width
# top = 1
#
# p = patches.Rectangle((left,bottom),width,height,color = '#ff9c71')
# ax.add_patch(p)
# # plt.show()
#
# kpi_lable = 'MOT'
# return_p = '180K'
# ax.text(0.5 * (left + right), 0.55 * (bottom + top), kpi_lable,
#         ha = 'center',va = 'center',
#         fontsize=24, color='black',
#         transform = ax.transAxes)
#
# ax.text(0.5 * (left + right), 0.3 * (bottom + top), return_p,
#         ha = 'center',va = 'center',
#         fontsize=24, color='red',
#         transform = ax.transAxes)
# # # Box 5
# left, width = 0.80, .19
# bottom, height = 0,1
# right = left + width
# top = 1
#
# p = patches.Rectangle((left,bottom),width,height,color = '#32e0c4')
# ax.add_patch(p)
# # plt.show()
#
# kpi_lable = 'MIR'
# return_p = '45K'
# ax.text(0.5 * (left + right), 0.55 * (bottom + top), kpi_lable,
#         ha = 'center',va = 'center',
#         fontsize=24, color='black',
#         transform = ax.transAxes)
#
# ax.text(0.5 * (left + right), 0.3 * (bottom + top), return_p,
#         ha = 'center',va = 'center',
#         fontsize=24, color='red',
#         transform = ax.transAxes)
#

plt.savefig('F:/PythonProject/CBD-KPI/img/box.png')

plt.show()


