import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


class Mailer():
    def __init__(self, fromaddr, toaddr, frompass, clustering_info):
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.frompass = frompass
        self.clustering_info = clustering_info
        self.subject = ""
        self.body = ""
        self.attachments = []

    def prepare_custom_report(self, subject, text):
        self.subject = subject
        self.body = text

    def prepare_end_report(self, jobname, bestmodel, simcount,
                           modelcount, clustering_info):
        self.subject = "PyRy3D - all jobs complete - final results."
        lines = ["Simulations starded: "+simcount,
                 "Models obtained: "+modelcount,
                 "",
                 ]
        self.body = "\n".join(lines)

    def send_report(self):
        msg = MIMEMultipart()

        msg['From'] = self.fromaddr
        msg['To'] = self.toaddr
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.body, 'plain'))

        for at in self.attachments:
            filename = at
            attachment = open(at, "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % filename)
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.fromaddr, self.frompass)
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
