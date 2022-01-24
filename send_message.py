import smtplib,ssl
context = ssl.create_default_context()

sender = "tomadragos96@gmail.com"
receiver = "tomadragos96@gmail.com"

server = smtplib.SMTP('smtp.mailtrap.io',2525)
#server.ehlo()
#server.starttls(context=context)
server.login("a0438499a3f07d", "77610ab18b0a70")
server.sendmail(receiver, sender,"this message is from python")
server.quit()