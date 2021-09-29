import slack
import creds


def send_results(message):
    client = slack.WebClient(token=creds.get_secret(creds.NAME))
    client.chat_postMessage(channel="Notifications", text=message)