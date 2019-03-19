import os
import time
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_TOKEN = os.environ.get('OAUTH_TOKEN')
slack_client = SlackClient(SLACK_TOKEN)

#Set using the "set" command in windows

def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None

def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

def send_message(channel_id,message):
    slack_client.api_call(
        "chat.postMessage",
        channel = channel_id,
        text=message,
        username = 'Comms Bot',
        icon_emoji=':robot_face:'
    )

def get_messages(slack_args, messages, filter_func):
    history = slack_client.api_call("channels.history", **slack_args)
    print("HISTROY",history)
    last_ts = history['messages'][-1]['ts'] if (history['has_more'] and history) else False
    filtered = list(filter(filter_func, history['messages']))
    all_messages = messages + filtered
    print('Fetched {} messages. {} Total now.'.format(len(filtered), len(all_messages)))

    return {
        'messages': all_messages,
        'last_ts': last_ts,
    }

def scrape_slack(slack_args, filter_func = lambda x: x):
    results = get_messages(slack_args, [], filter_func)

    while results['last_ts']:
        slack_args['latest'] = results['last_ts']
        results = get_messages(sc, slack_args, results['messages'], filter_func)

    print('Done fetching messages. Found {} in total.'.format(len(results['messages'])))
    return results['messages']

if __name__ == '__main__':
    channels = list_channels()

    slack_args = {
        'channel': "CFRV15GBU",
        'oldest': "",
    }
    if channels:
        print("Channels: ")
        for c in channels:
            #print(c['name'] + " (" + c['id'] + ")")
            detailed_info = channel_info(c['id'])
            #if detailed_info:
                #print(detailed_info.keys())
            #if c['name'] == 'communications_office':
                #send_message(c['id'], "Testing comms feed bot,ignore")
            
        print("GETTING MESSAGES...")
        msgs = scrape_slack(slack_args)
        print(msgs)
        print('-----')
    else:
        print("Unable to authenticate.")