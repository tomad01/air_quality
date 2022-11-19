import smtplib
import logging
import os

#context = ssl.create_default_context()


message = """From: tomadragos96@gmail.com
To: tomadragos96@gmail.com
Subject: Send mail from raspberry!!

"""
email_address = os.getenv("EMAIL_ADDRESS", default=None)
password = os.getenv("EMAIL_PASSWORD", default=None)

def send_email(text):
    try:
        sender = email_address
        receiver = email_address

        #server = smtplib.SMTP('smtp.mailtrap.io',2525)
        #server.ehlo()
        #server.starttls(context=context)
        #server.login("a0438499a3f07d", "77610ab18b0a70")
        #server.sendmail(receiver, sender,"this message is from python")
        #server.quit()
  
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email_address,password)
        server.sendmail(receiver, sender,message+text)
        server.quit()
        logging.info('email sent')
    except Exception as er:
        logging.error(str(er))