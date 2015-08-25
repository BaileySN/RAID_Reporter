#!/usr/bin/python
# -*- coding: utf-8 -*-


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from conf import emailconfig
from hostinfo import hostaddr,hostn
emc = emailconfig()
hostname = hostn()
ipaddr = hostaddr()

class emailsend(object):
    def __init__(self, report):
        self.txt = "text"

    def __new__(self, report):
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = (emc.betreff+hostname)
        msg['From'] = emc.absender
        msg['To'] = emc.empfaenger

        # Create the body of the message (a plain-text and an HTML version).
        text = "Caution! \nRAID Error detected by Server \nHostname = '%s' \nIP-Address = '%s' \nSystem message: \n'%s'" % (hostname, ipaddr, report)
        html = """\
		<html>
		<head></head>
		<body>
			<p>Caution!<br />
			RAID Error detected by Server<br />Hostname = <span style="color:red">'%s'</span><br />IP-Address = <span style="color:red">'%s'</span><br />
			System message:<br />
			'%s'
			</p>
		</body>
		</html>
		""" %(hostname, ipaddr, report)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via local SMTP server.
        s = smtplib.SMTP(emc.smtpserver)
        s.sendmail(emc.absender, emc.empfaenger, msg.as_string())
        s.quit()
