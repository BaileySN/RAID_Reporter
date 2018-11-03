import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from conf import emailconfig
from hostinfo import hostaddr,hostn
emc = emailconfig()
hostname = hostn()
ipaddr = hostaddr()


class EmailNotify(object):
    def __init__(self):
        self.msg = MIMEMultipart('alternative')

    def assemble_msg(self, report):
        self.msg['Subject'] = (emc.betreff + hostname)
        self.msg['From'] = emc.absender
        self.msg['To'] = emc.empfaenger
        mailtext = "Caution! \nRAID Error detected by Server \nHostname = %s \nIP-Address = %s \nSystem message: \n '%s' " %(hostname, ipaddr, report)
        htmltext = """<html><head></head><body>
        <p>Caution!<br />
        RAID Error detected by Server<br />Hostname = <span style="color:red"> %s </span><br />IP-Address = <span style="color:red"> %s </span><br />
        System message:<br />
        '%s'</p></body></html>""" %(hostname, ipaddr, report)
        part1 = MIMEText(mailtext, 'plain')
        part2 = MIMEText(htmltext, 'html')
        self.msg.attach(part1)
        self.msg.attach(part2)

    def sendmail(self):
        # Send the message via local SMTP server.
        s = smtplib.SMTP(emc.smtpserver, emc.smtpport)
        if emc.ssl:
            s.starttls()
        if len(emc.smtpbenutzer) and len(emc.smtppasswort):
            s.login(emc.smtpbenutzer, emc.smtppasswort)
        result = s.sendmail(emc.absender, emc.empfaenger, self.msg.as_string())
        s.quit()
        return result

    def send(self, report):
        self.assemble_msg(report=report)
        return self.sendmail()
