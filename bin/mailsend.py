import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from conf import emailconfig
from hostinfo import hostaddr, hostn
emc = emailconfig()


class EmailNotify(object):
    def __init__(self):
        self.msg = MIMEMultipart('alternative')
        self.hostname = hostn()
        self.ipaddr = hostaddr()

    def assemble_msg(self, report):
        self.msg['Subject'] = (emc.betreff + self.hostname)
        self.msg['From'] = emc.absender
        self.msg['To'] = emc.empfaenger
        mailtext = "Caution! \nRAID Error detected by Server \nHostname = %s \nIP-Address = %s \nSystem message: \n '%s' " %(self.hostname, self.ipaddr, report)
        htmltext = """<html><head></head><body>
        <p>Caution!<br />
        RAID Error detected by Server<br />Hostname = <span style="color:red"> %s </span><br />IP-Address = <span style="color:red"> %s </span><br />
        System message:<br />
        '%s'</p></body></html>""" %(self.hostname, self.ipaddr, report)
        part1 = MIMEText(mailtext, 'plain')
        part2 = MIMEText(htmltext, 'html')
        self.msg.attach(part1)
        self.msg.attach(part2)

    def sendmail(self):
        # Send the message via local SMTP server.
        if emc.ssl and not emc.starttls:
            s = smtplib.SMTP_SSL(emc.smtpserver, emc.smtpport)
        else:
            s = smtplib.SMTP(emc.smtpserver, emc.smtpport)
        if emc.starttls:
            s.starttls()
        if len(emc.smtpbenutzer) and len(emc.smtppasswort):
            s.login(emc.smtpbenutzer, emc.smtppasswort)
        result = s.sendmail(emc.absender, emc.empfaenger, self.msg.as_string())
        s.quit()
        return result

    def send(self, report):
        self.assemble_msg(report=report)
        return self.sendmail()
