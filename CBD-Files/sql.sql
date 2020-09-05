---Brand Wise Sales
select 
BRAND.VDESC as Brand 
,SUM(EXTINVMISC) as Sales
from OESalesDetails
Left Join Brand on BRAND.[Value] = OESalesDetails.Brand
Where 
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
and TRANSTYPE = 1
Group By BRAND.VDESC

-----------Branch Wise Sales MTD-------------
select   
BRANCHLIST.BRANCH as Branch 
,SUM(EXTINVMISC) as Sales
from OESalesDetails
Left Join BRANCHLIST on BRANCHLIST.CBD = OESalesDetails.AUDTORG
Where 
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
and TRANSTYPE = 1
Group By BRANCHLIST.BRANCH

------------------- Top 10 Item Sales MTD -------------
select 
top 10
ICItem_ShortName.ShortName,
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

------------------ Top 10 Customer  Sales MTD-----------------------------
select
top 10 
CUSTNAME ,
SUM(EXTINVMISC) as Sales
From OESalesDetails
Where 
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
Group By CUSTNAME
Order By SUM(EXTINVMISC) Desc 

------------------- Terms Wise Sale --------------------
Select 
SUM(case WHEN  TERMS = 'CASH' Then EXTINVMISC END ) as 'CASH',
SUM(case WHEN  TERMS not like '%CASH%'  Then EXTINVMISC END ) as 'CREDIT'
from OESalesDetails

Where 
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
---------------BRAND WISE STOCK------------------
Select 
BRAND.VDESC as Brand,
SUM(QTYONHAND) AS STOCK
from ICHistoricalStock
Left JOIN BRAND ON BRAND.[VALUE]=ICHistoricalStock.BRAND
Where 
AUDTDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
Group By BRAND.VDESC
----------------------- Totall Outstanding ----------------
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
----------------------------------------------------------------

-- Branch Wise Sales Compare 
---- MTD Sales
Select 
AUDTORG As Branch,
SUM(EXTINVMISC) As Sales
from OESalesDetails
Where 
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
Group By AUDTORG
----Last Month Sales
Select 
AUDTORG As Branch,
SUM(EXTINVMISC) As Sales
from OESalesDetails
Where 
TRANSDATE between
(convert(varchar(8),DATEADD(M, DATEDIFF(M, 0, GETDATE())-1, 0),112))
AND
convert(varchar(8),DATEADD(d,-1,DATEADD(mm, DATEDIFF(m,0,GETDATE()),0)),112)
Group By AUDTORG
--------------------- Top 20 Brand Wise Customer Sales ------------------
select
top 20
BRAND.VDESC as Brand,
OESalesDetails.CUSTOMER,
OESalesDetails.CUSTNAME
,SUM(OESalesDetails.EXTINVMISC) as Sales
from OESalesDetails
Left Join Brand on BRAND.[Value] = OESalesDetails.Brand
Where 
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)
and TRANSTYPE = 1
Group By BRAND.VDESC,OESalesDetails.CUSTNAME,OESalesDetails.CUSTOMER
----------------------------------------------------------------
--- RETURN
-----------------
--YTD Return
select sum(EXTINVMISC) as YTDReturnAmount from OESalesDetails where
transtype<>1 and PRICELIST <> 0 and
(TRANSDATE between convert(varchar(6),DATEADD(yy, DATEDIFF(yy, 0, GETDATE()), 0),112)
and (convert(varchar(8),DATEADD(D,-1,GETDATE()),112)))

--Last Day Return
select sum(EXTINVMISC) as LDReturnAmount from OESalesDetails where
transtype<>1 and PRICELIST <> 0 and
TRANSDATE = convert(varchar(8),getdate()-1,112)

--Last  MTDReturn
select sum(EXTINVMISC) as ReturnAmount from OESalesDetails where
transtype<>1 and PRICELIST <> 0 and
TRANSDATE between
(convert(varchar(8),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),112))
AND
convert(varchar(8),DATEADD(D,-1,GETDATE()),112)


