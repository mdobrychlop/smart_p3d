import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


fromaddr = "pyry3d.status@gmail.com"
toaddr = "mateusz.dobrychlop@gmail.com"
jobname = "TEST"
best_scored_model = "test.pdb"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "PyRy3D job "+jobname+" - best model"

body = "Representative model's name: " + best_scored_model

msg.attach(MIMEText(body, 'plain'))

filename = "clap.jpg"
attachment = open("clap.jpg", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "ZywiecPorter")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
