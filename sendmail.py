import smtplib, dkim, time, os
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
port = 25
smtp_server = "mail.ietf.org"
sender_email = "vladimir@lightside-instruments.com"
sender_domain="lightside-instruments.com"
receiver_email = "bmwg@ietf.org"
dkim_selector = "key1"
password = "strongPassword"
msg = MIMEMultipart('alternative')       
msg['From']= sender_email
msg['To']= receiver_email
msg['Subject']= "Fwd: [bmwg] I-D Action: draft-ietf-bmwg-network-tester-cfg-03.txt"
with open('message.txt') as fh:
    message = fh.read()
#message = "A digitally signed email"
msg.attach(MIMEText(message, "plain"))
headers=[b'from', b'to', b'subject']
with open('key1.private') as fh:
    dkim_private_key = fh.read()

#print(dkim_private_key)
signature = dkim.sign(message=msg.as_bytes(), selector=dkim_selector.encode(), domain=sender_domain.encode(), privkey=dkim_private_key.encode(), include_headers=headers) #, signature_algorithm="ed25519-sha256".encode()
msg['DKIM-Signature'] = signature[len("DKIM-Signature: "):].decode()
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server) as server:
#    server.starttls() # context=context
#    server.login(sender_email, password )
    server.set_debuglevel(1)
    server.sendmail(sender_email, receiver_email, msg.as_bytes())
    server.quit()
print('Sent')
