import xlrd
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from email import encoders
from email.mime.base import MIMEBase


def table_data():
    xl = xlrd.open_workbook('F:/PythonProject/CBD-KPI/file/top20.xlsx')
    sh = xl.sheet_by_name('Sheet1')

    th = ""
    td = ""
    # Select all columns header name and placed All name in serial
    for i in range(0, 1):
        # th = th + "<th class=\"unit\"> ID</th>"

        for j in range(0, sh.ncols):
            th = th + "<th class=\"unit\">" + str(sh.cell_value(i, j)) + "</th>\n"
        th = th + "</tr>\n"

    # Now placed all data
    for i in range(1, sh.nrows):
        td = td + "<tr>\n"
        td = td + "<td class=\"idcol\">" + str(i) + "</td>"

        for j in range(1, 2):
            td = td + "<td class=\"idcol\">" + str(sh.cell_value(i, j)) + "</td>\n"
        for j in range(2, 3):
            td = td + "<td class=\"unit\">" + str(sh.cell_value(i, j)) + "</td>\n"
        for j in range(3, 4):
            td = td + "<td class=\"unit\">" + str(sh.cell_value(i, j)) + "</td>\n"
        for j in range(4, sh.ncols):
            td = td + "<td class=\"unit\">" + str(sh.cell_value(i, j)) + "</td>\n"
        # for j in range(5,sh.ncols):
        #     td = td + "<td class=\"unit\">" + str(sh.cell_value(i, j)) + "</td>\n"
        # for j in range(2, sh.ncols):
        #     td = td + "<td class=\"idcol\">" + str(int(sh.cell_value(i, j))) + "</td>\n"
        td = td + "</tr>\n"
    html = th + td
    return html


# ------------ Group email ----------------------------------------
msgRoot = MIMEMultipart('related')
me = 'erp-bi.service@transcombd.com'
to = ['ashik.mahmud@transcombd.com', '']
cc = ['', '']
bcc = ['', '']

recipient = to + cc + bcc

subject = "Python Final Project by B.M. ASHIK MAHMUD "

email_server_host = 'mail.transcombd.com'
port = 25

msgRoot['From'] = me

msgRoot['To'] = ', '.join(to)
msgRoot['Cc'] = ', '.join(cc)
msgRoot['Bcc'] = ', '.join(bcc)
msgRoot['Subject'] = subject

msg = MIMEMultipart()
msgRoot.attach(msg)

msgText = MIMEText(""" 

<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<style>
	table {
		border-collapse: collapse;
		border: 1px solid gray;
		padding: 5px;
	}

	td {
		padding-top: 5px;
		border-bottom: 1px solid #ddd;
		text-align: left;
		white-space: nowrap;
		border: 1px solid gray;
		#text-align: justify;
	}

	th.unit {
		padding: 2px;
		border: 1px solid gray;
		background-color: #dcf045;
		width: 22px;
		font-size: 16px;
		white-space: nowrap;
	}

	td.idcol {
		text-align: right;
		white-space: nowrap;
		text-justify: inter-word;
	}
	</style>
</head>

<body>
	<table> """ + table_data() + """ </table>
</body>

</html>

""", 'html')

msg.attach(msgText)

# # # Attached files
file_location = 'F:/PythonProject/CBD-KPI/file/top20.xlsx'
filename = os.path.basename(file_location)
attachment = open(file_location, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msgRoot.attach(part)

# # ----------- Finally send mail and close server connection ---
server = smtplib.SMTP(email_server_host, port)
server.ehlo()
server.sendmail(me, recipient, msgRoot.as_string())
server.close()
print('Mail Send')