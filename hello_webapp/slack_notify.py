import json

from slackclient import SlackClient

from hello_settings import SECRETS_DICT


def slack_notify_message(message):
    """
    sends a slack message (for logging, and error notification)
    :param message:
    :return: None
    """
    bot_token = SECRETS_DICT['CITIGROUP_SLACKBOT_TOKEN']
    sc = SlackClient(bot_token)

    log_channel_id = SECRETS_DICT['SLACK_LOG_CHANNEL_ID']
    sc.api_call('chat.postMessage', channel=log_channel_id,
                text='{message}'.format(message=message), link_names=1,
                as_user=True)


def list_channels():
    """
    helper method for listing all channels
    :return: None
    """
    bot_token = SECRETS_DICT['CITIGROUP_SLACKBOT_TOKEN']
    sc = SlackClient(bot_token)
    channels = sc.api_call('channels.list')
    return channels


if __name__ == '__main__':
    channels = json.loads(list_channels())
    slack_notify_message('test message')