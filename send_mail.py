def send_mail(recipient, subject, message):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    username = "cll58@cam.ac.uk"
    password = "OMGWorkWork10!"

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    try:
        print('sending mail to ' + recipient + ' on ' + subject)

        mailServer = smtplib.SMTP('smtp-mail.outlook.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(username, password)
        mailServer.sendmail(username, recipient, msg.as_string())
        mailServer.close()

    except error as e:
        print(str(e))

trial = 'Test\n Test\n How are you\n'

send_mail('chuenleik_3837@hotmail.com', 'JCSU Feed Report', 'May the force be with you.\n '+trial)