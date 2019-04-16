Discord Dice Bot
================

[![Release 1.0.0](https://img.shields.io/badge/release-v1.0.0-informational.svg)](https://git.ephesos.eu/maxime/DiscordDiceBot/releases)
[![Python 3.6](https://img.shields.io/badge/python-3.6-informational.svg)](https://www.python.org/)

**Discord Dice Bot** is a discord bot that can calculate mathematical equations containing additions, 
subtractions, multiplications and divisions as operators, numbers and dices as operands.
It has been written by *Maxime Hohl* in [Python](https://www.python.org/) 3.6 using 
the [discord.py](https://github.com/Rapptz/discord.py) library.

This code is under the CC BY-SA 4.0 licence (see [LICENCE.md](LICENCE.md)).


How to
------

### Install the bot

Install dependencies :
```bash
apt-get update -y
apt-get install git python3 python3-venv python3-pip
```

Then clone the *git* repository :
```bash
git clone https://git.ephesos.eu/maxime/DiscordDiceBot.git -b master
```

Create the virtual environment :
```bash
cd DiscordDiceBot
python3 -m venv venv
```

Switch to the environment we just created :
```bash
source ./venv/bin/activate
```

Download the python's dependencies :
```bash
pip3 install discord.py
```

Now you can run the bot with :
```bash
chmod u+x run.sh
./run.sh
```

### Update the bot

Stop the bot, then go to the bot folder and type the following command :
```bash
git pull
```

The bot is now up-to-date.

### Use the bot

#### Configuration
Configuring the bot is quite straight forward. Open the `settings` 
directory and copy `example_settings.py` to `settings.py`.

You need to fill the token field before you use the bot.
To generate this token go to Discord 
[applications page](https://discordapp.com/developers/applications/me).

All the other settings are detailed in the `settings.py` file.

#### Invite the bot to a server

Go to this url where you replaced `<CLIENT ID>` with the discord application
client id :
```url
https://discordapp.com/oauth2/authorize?&client_id=<CLIENT ID>&scope=bot&permissions=0
```

#### Commands
All the commands need to be prefixed with the `COMMAND_PREFIX` setting.

##### Commands
- `help` - Print a list of commands
- `roll <equation>` - calculate the result for the equation `equation`
- `r` - Alias for `roll` 

##### Equations
All the equations follow the grammar detailed in the file `interpreter/grammar`.

Operators : `+`, `-`, `*` or `/`  
Operands : any real number or dice  
Dice : `<c>d<n>` with `c` the number of dice and `n` the maximum value of the dices

Examples :
- `5d6+2` will roll 5 dices with 6 faces and add 2 to the sum of the dices results
- `(3d12 + 4) * 2` will roll 3 dices with 12 faces, add 4 to the sum of the dices results 
and then multiply the result by 2


TODO
----

- Add options :
    - enable/disable user tag on available roll result
