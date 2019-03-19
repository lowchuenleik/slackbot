from flask_script import Manager
import json
import bot
import os
from slackclient import SlackClient
from app import app

manager = Manager(app)

@manager.command
def getmessages():
    print("Trying?")
    SLACK_TOKEN = os.environ.get('OAUTH_TOKEN')
    slack_client=SlackClient(SLACK_TOKEN)
    ###
    channel_id=''
    old_json=[]
    ###
    #^ remove

    slack_args = {
        'channel': "CFRV15GBU",
        'oldest': "",
    }

    temp = scrape_slack(slack_client,slack_args,lambda x:'client_msg_id' in x)
    print(temp)
    for msg in temp:
        message="Event:" + msg['text']
        print(message)
        send_message(slack_client,slack_args['channel'],message)
    return ''

def get_messages(sc,slack_args, messages, filter_func):
    
    history = sc.api_call("channels.history", **slack_args)
    print("HISTROY",history)
    last_ts = history['messages'][-1]['ts'] if (history['has_more'] and history) else False
    filtered = list(filter(filter_func, history['messages']))
    all_messages = messages + filtered
    print('Fetched {} messages. {} Total now.'.format(len(filtered), len(all_messages)))

    return {
        'messages': all_messages,
        'last_ts': last_ts,
    }

def scrape_slack(sc,slack_args, filter_func = lambda x: x):
    results = get_messages(sc,slack_args, [], filter_func)

    while results['last_ts']:
        slack_args['latest'] = results['last_ts']
        results = get_messages(sc, slack_args, results['messages'], filter_func)

    print('Done fetching messages. Found {} in total.'.format(len(results['messages'])))
    return results['messages']

def list_channels():
    channels_call = pyBot.client.api_call("channels.list")
    print('\n\n CHANNEL CALLS:',channels_call)
    if channels_call.get('ok'):
        return channels_call['channels']
    return None

def send_message(slack_client,channel_id,message):
    slack_client.api_call(
        "chat.postMessage",
        channel = channel_id,
        text=message,
        username = 'Comms Bot',
        icon_emoji=':robot_face:'
    )


if __name__ == "__main__":
    manager.run()