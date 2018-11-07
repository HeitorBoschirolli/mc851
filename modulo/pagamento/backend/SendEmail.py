import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

fromaddr = "mc851nani@gmail.com"
toaddr = "EMAIL DE ENVIO"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "SUBJECT DO ENVIO"

body = "MENSAGEM"
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "mc851pagamento")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()