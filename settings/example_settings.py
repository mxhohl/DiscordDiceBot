# The bot token (should remain secret)
TOKEN = ""

# The log file path
LOG_FILE_PATH = "logs/dicebot.log"

# The prefix for the roll (or r) command
COMMAND_PREFIX = '!'

# Define the time after which the user command will be removed (in seconds)
# Set to -1 to disable cleaning
# To enable this parameter the bot need the *manage_messages* permission
TIME_BEFORE_CLEANING_COMMAND = 5

# Define the time before which the discord dice bot will remove his help message (in seconds)
# Set to -1 to disable cleaning
TIME_BEFORE_CLEANING_HELP = -1

# Define the log level used by the bot
# Possible values are ALL, INFO, WARNING, ERROR
LOGGING_LEVEL = "ALL"
