import discord
import logging
import sys
import os
import asyncio

from settings import settings
from interpreter.lexer import Lexer
from interpreter.interpreter import Interpreter


def create_log_folder():
    folder_path = os.path.dirname(os.path.abspath(settings.LOG_FILE_PATH))
    os.makedirs(folder_path, exist_ok=True)


def get_config_log_level():
    if settings.LOGGING_LEVEL == "INFO":
        return logging.INFO
    elif settings.LOGGING_LEVEL == "WARNING":
        return logging.WARNING
    elif settings.LOGGING_LEVEL == "ERROR":
        return logging.ERROR
    return logging.DEBUG


class DiceBotClient(discord.Client):
    def __init__(self, *, loop=None, **options):
        super().__init__(loop=loop, **options)

        create_log_folder()
        self.logger = logging.getLogger("DiceBot")
        self.init_logging()

        self.lexer = Lexer()
        self.interpreter = Interpreter(self.lexer)

    def start_client(self):
        self.run(settings.TOKEN)

    async def on_ready(self):
        self.logger.info('Logged in as %s (id:%s, disc:%s)',
                         self.user.name,
                         self.user.id,
                         self.user.discriminator)

    async def on_message(self, message):
        if not message.content.startswith("{}roll".format(settings.COMMAND_PREFIX)):
            if not message.content.startswith("{}r".format(settings.COMMAND_PREFIX)):
                return

            else:
                command = message.content[(2 + len(settings.COMMAND_PREFIX)):]

        else:
            command = message.content[(5 + len(settings.COMMAND_PREFIX)):]

        if command.startswith("help"):
            await self.on_command_help(message)

        else:
            await self.on_command_roll(command, message)

        if settings.TIME_BEFORE_CLEANING_COMMAND > 0:
            await asyncio.sleep(settings.TIME_BEFORE_CLEANING_COMMAND)
            await message.delete()

    async def on_command_help(self, message):
        self.logger.info('Received help command from %s', message.author)
        await message.channel.send(
            "```"
            "Discord Dice Bot is a small Discord bot developed by Maxime Hohl.\n"
            "Git repo : https://git.ephesos.eu/maxime/DiscordDiceBot\n"
            "Licence : CC BY-SA 4.0\n"
            "\n"
            "Commands :\n"
            "  - help : this message\n"
            "  - roll (or r) : roll dice expression\n"
            "\n"
            "Dice expression :\n"
            "A dice expression is like any normal mathematical expression with "
            "the operators +, -, *, /, parenthesis and number."
            "To this mathematical you can add dice rolling operator which look like nDm where "
            "n is the number of dice you want to roll and m the maximum value of the dice.\n"
            "For example 2d6 + 3 will roll two six faced dice and then add 3 to the result of that roll."
            "```",
            delete_after=settings.TIME_BEFORE_CLEANING_HELP if settings.TIME_BEFORE_CLEANING_HELP != -1 else None
        )

    async def on_command_roll(self, equation, message):
        sent_message = await message.channel.send('Calculating result...')
        try:
            self.lexer.new(equation)
            self.interpreter.new()
            result = self.interpreter.parse(), self.interpreter.result_desc

            await sent_message.edit(content='Here is your roll {} !\n`{}` = **{}**'
                                    .format(message.author.mention, result[1], result[0]))

            self.logger.info("Rolled '%s' for %s with the following result : '%s'",
                             equation, message.author, result[0])

        except Exception as exception:
            await sent_message.edit('{} {}'.format(message.author.mention, exception))

            self.logger.warning("Failed to roll '%s' for %s",
                                equation, message.author)

    def init_logging(self):
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s][%(name)-12s][%(levelname)8s] - %(message)s',
                                      '%Y-%m-%d %H:%M:%S')

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        stdout_handler.setLevel(get_config_log_level())

        file_handler = logging.FileHandler(settings.LOG_FILE_PATH, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(get_config_log_level())

        self.logger.addHandler(stdout_handler)
        self.logger.addHandler(file_handler)


if __name__ == "__main__":
    client = DiceBotClient()
    client.run("NTE0MDI3MzEyMDQwMTE2MjI1.DtQlfA.gPBjqvfpk1Z1omeWg4vrJuDmfi4")
