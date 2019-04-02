from flask_script import Manager
import json
import bot
import time
import os
from slackclient import SlackClient
from app import app
from app import send_message,send_mail,scrape_slack

manager = Manager(app)
SLACK_TOKEN = os.environ.get('OAUTH_TOKEN')
EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

@manager.command
def getmessages():
    print("Trying?")
    slack_client=SlackClient(SLACK_TOKEN)
    
    ###
    channel_id=''
    old_json=[]
    ###

    slack_args = {
        'channel': "CFRV15GBU",
        'oldest': "",
    }

    temp = scrape_slack(slack_client,slack_args,lambda x:('client_msg_id' in x) and ('[JCSU]' in x['text']))
    print(temp)
    subject = time.strftime('JCSU Slack Channel Feed on %A %d %B %Y \n\n\n')
    email = subject+'------------------\n\n\n'
    for msg in temp:
        message="Event:" + msg['text']
        email = email + '\n\n'+msg['text'][7:]
        print(message)
        send_message(slack_client,slack_args['channel'],message)
    send_mail("chuenleik_3837@hotmail.com",subject,email)
    return ''

#trial = 'Test\n Test\n How are you\n'
#send_mail('chuenleik_3837@hotmail.com', 'JCSU Feed Report', 'May the force be with you.\n '+trial)

if __name__ == "__main__":
    manager.run()