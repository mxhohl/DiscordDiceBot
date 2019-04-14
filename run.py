import signal

from dice_bot import DiceBotClient


def sigint_handler(sig, frame):
    print("Exiting...")
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)

    dbc = DiceBotClient()
    dbc.start_client()
