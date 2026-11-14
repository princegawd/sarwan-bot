import asyncio
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ChatType
from telegram.error import RetryAfter, TimedOut, NetworkError
import logging
import re
import random

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.WARNING
)

OWNER_ID = int(os.getenv("OWNER_ID", "8640855841"))
BOT_TOKENS = [
    os.getenv("BOT_TOKEN_1", "9155027493:AAG5wOsYTsIlTnOfI2OVFN-_8MOu6CxqXXU"),
    os.getenv("BOT_TOKEN_2", "9297733031:AAGAFna50XuOhKwse5tA6mn1UiwwEvHGucU"),
    os.getenv("BOT_TOKEN_3", "9035946089:AAEpYrXvty_qN9UGFya0IE9RhaglMNa7LSc"),
    os.getenv("BOT_TOKEN_4", "9018659997:AAGutr0Dk65XMYsbKo3HDgF5HlkE1sX5M6M"),
    os.getenv("BOT_TOKEN_5", "9139127626:AAGGtYdFa3gFsLaDRssodN4_xVqeo-V7A30"),
    os.getenv("BOT_TOKEN_6", "9269393280:AAGy4Zk8vP_pNBjAetITEoDHcDorQ9cEUCM"),
    os.getenv("BOT_TOKEN_7", "9029451417:AAFZ90UQSdq1ETV4MqKkBRkSzI8yHn-pAdA"),
    os.getenv("BOT_TOKEN_8", "8968418613:AAGHtddkDI4UVXx5uCJeXgzj6WcE3saCWb4"),
    os.getenv("BOT_TOKEN_9", "8972448429:AAERvnPWbQ8Hvi5otXKIP5JbS5yam82FdpI"),
    os.getenv("BOT_TOKEN_10","9118981182:AAEdm8PM0ftSC3opG3pdpRPDJ0bqp8YLuWE"),
]

BOT_TOKENS = [t for t in BOT_TOKENS if t]

if not BOT_TOKENS:
    print("ERROR: No bot tokens found! Set BOT_TOKEN_1, BOT_TOKEN_2, etc. environment variables")
    exit(1)

NC_V2_MESSAGES = [
	"{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆 (⚡) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖💖❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆 (⚡) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖💖❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆 (🤑) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖💖❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆 (😴) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖💖❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆 (🤤) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖💖❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆 (🥶) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖💖❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
    "{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐧e 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 (🥵) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖💖❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
	"{target}  𝐂𝐇𝐔𝐏 𝐊𝐑 𝐓𝐌𝐊𝐂 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐓𝐄𝐑𝐈 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈🤣 😍 𝐂𝐇𝐔𝐏 𝐊𝐑 𝐓𝐌𝐊𝐂 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐓𝐄𝐑𝐈 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈🤣 😍 (❤️‍🔥) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖💖❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
	"{target}  𝐓𝐄𝐑𝐈 𝐌𝐔𝐌𝐌𝐘 𝐊𝐈 𝐊𝐀𝐋𝐈 𝐂𝐇𝐔𝐓 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐈 M𝐔𝐇 𝐌𝐄 🍑()  (💥) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖💖❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
	"{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆 (💫) 💌❖❖❖❖❖💝❖❖❖❖❖❣️❖❖❖❖❖👑❖❖❖❖❖🤍❖❖❖❖❖💕❖❖❖❖❖💛❖❖❖❖❖❣️❖❖❖❖❖❤️❖❖❖❖❖💙❖❖❖❖❖💓❖❖❖❖❖💗❖❖❖❖❖💖❖❖❖❖❖💝❖❖❖❖❖🤎❖❖❖❖❖💚❖❖❖❖❖💔❖❖❖❖❖💛❖❖❖❖❖💞❖❖❖❖❖💜❖❖❖❖❖🖤❖❖❖❖❖🤍❖❖❖❖❤️‍🩹❖❖❖❖❖💌❖❖❖❖❖❣️❖❖❖❖❖💥❖❖❖❖❖💗❖❖❖❖❖💝❖❖❖❖❖💘❖❖❖❖❖❤️‍🔥❖❖❖❖❖💝❖❖❖❖❖💖",
]

NC_FLAG_MESSAGES = [
    "{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ𝐆𝐎𝐃 𝐧e 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 ⁣⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣✨🌟🌟✨✨🌟🌟✨⁣💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚💚👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁🍁💚💚👑👑💚👑👑💚💚👑👑💚👑👑👑👑👑⁣(🇿🇼)",
    "{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ𝐆𝐎𝐃𓆪𓆩⃟ 𝐧e 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 ⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣✨🌟🌟✨✨🌟🌟✨⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣(🏳️‍🌈)",
    "{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐧e 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 ⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣✨🌟🌟✨✨🌟🌟✨⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣(🏳️‍⚧️)",
    "{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ𝐆𝐎𝐃𓆪𓆩⃟ 𝐧e 𝐬𝐨 𝐬𝐚𝐝 🍷 ⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣✨🌟🌟✨✨🌟🌟✨⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣(🇦🇩)",
    "{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 PrInCe 𝐧e 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 ⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣✨🌟🌟✨✨🌟🌟✨⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣(🇦🇱)",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛 ⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣✨🌟🌟✨✨🌟🌟✨⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣(🇦🇴)",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛 ⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣✨🌟🌟✨✨🌟🌟✨⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣(🇦🇮)",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛 ⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣✨🌟🌟✨✨🌟🌟✨⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣(🇬🇬)",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛 ⁣✨🌟🌟✨🌟✨✨✨💚✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣✨🌟🌟✨✨🌟🌟✨⁣✨🌟🌟✨🌟✨✨✨✨✨🌟✨✨✨🌙🌟✨✨🌟🌟✨🌟✨✨✨✨✨⁣(👑💚🇳🇴)",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛 ⁣👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑👑",
]

NC_CURLY_MESSAGES = [
    "{{ {target} }}",
    "{{- {target} -}}",
    "{{★ {target} ★}}",
    "{{🔥 {target} 🔥}}",
    "{{🔱 {target} 🔱}}",
    "{{✨ {target} ✨}}",
    "{{🥀 {target} 🥀}}",
]

DOTZKENG_MESSAGES = [
    "⚡ {target} 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐎 𝐁𝐀𝐀𝐏 𝐁𝐎𝐋  𝐓𝐌𝐊𝐂 ⚡",
    "🔥 {target}  𝐂𝐇𝐔𝐏 𝐊𝐑 𝐓𝐌𝐊𝐂 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐓𝐄𝐑𝐈 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈🤣 👅 🔥",
    "👑 {target} 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐎 𝐁𝐀𝐀𝐏 𝐁𝐎𝐋  𝐓𝐌𝐊𝐂  👑",
    "👑 {target} 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐎 𝐁𝐀𝐀𝐏 𝐁𝐎𝐋  𝐓𝐌𝐊𝐂  👑",
    "💀 {target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ𝐆𝐎𝐃𓆪𓆩⃟ 𝐊𝐀 🍆🍆",
    "💥 {target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆",
    "🚀 {target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ𝐆𝐎𝐃𓆪𓆩⃟ 𝐊𝐀 🍆🍆",
    "🦾 {target} CHUD GYA NA RNDYKE AB BAAP BOL 🦾",
]

FLOWER_NC_MESSAGES = [
    "༄˖°.🥀.ೃ࿔*:･{target} KI MA KI CHUT ME GULAB ",
    "༄˖°.💮.ೃ࿔*:･{target} KI MA KI CHUT ME CLAY ",
    "༄˖°.💠.ೃ࿔*:･{target} TERI MA KI CHUT ME DULL ",
    "༄˖°.🌻.ೃ࿔*:･{target} TERI MA KI CHUT ME SUNFLOWER ",
    "༄˖°.🌺.ೃ࿔*:･{target} TERI MA KI CHUT ME RED ROSE ",
    "༄˖°.🌸.ೃ࿔*:･{target} TERI MA KI CHUT ME BRUST ",
    "༄˖°.🌷.ೃ࿔*:･{target} TERI MA KI CHUT ME ROSE ",
]

UNAUTHORIZED_MESSAGE = "- 𝐓𝐔 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ𝐆𝐎𝐃𓆪𓆩⃟ 𝐊𝐈 𝐁𝐎𝐓 𝐔𝐒𝐄 𝐊𝐀𝐑𝐄𝐆𝐀 𝐓𝐌𝐊𝐂 𝐌𝐀𝐑𝐔"

NAME_CHANGE_MESSAGES = [
    "{target}  𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐎 𝐁𝐀𝐀𝐏 𝐁𝐎𝐋 𝐂𝐇𝐀𝐋  𝐁𝐎𝐋 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈 🏑🏴‍☠️ 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿  ",
    "{target}   𝐓𝐄𝐑𝐈 𝐁𝐇𝐄𝐍 𝐊𝐈 𝐂𝐇𝐔𝐓 𝐌𝐀𝐑 𝐆𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ💀🤣 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
    "{target} 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐎 𝐁𝐀𝐀𝐏 𝐁𝐎𝐋  𝐓𝐌𝐊𝐂 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
    "{target}   𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 PrInCe 𝐧e 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
    "{target}  𝐂𝐇𝐔𝐏 𝐊𝐑 𝐓𝐌𝐊𝐂 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐓𝐄𝐑A 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈🤣 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
    "{target}  𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐎 𝐁𝐀𝐀𝐏 𝐁𝐎𝐋 𝐂𝐇𝐀𝐋  𝐁𝐎𝐋 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈 🏑🏴‍☠️ 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
    "{target}  𝐓𝐄𝐑𝐈 𝐁𝐇𝐄𝐍 𝐊𝐈 𝐂𝐇𝐔𝐓 𝐌𝐀𝐑 𝐆𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ💀🤣 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐁𝐇𝐄𝐍 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐒𝐄 CHUD TI 𝐇𝐀𝐈 🇦🇱🚩 💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐔𝐌𝐌𝐘 𝐊𝐈 𝐊𝐀𝐋𝐈 𝐂𝐇𝐔𝐓 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐈 M𝐔𝐇 𝐌𝐄 🍑()  💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜😙𒆜𒆜👄𒆜𒆜💥𒆜𒆜👁️‍🗨️𒆜𒆜💨𒆜𒆜🐕𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🍓𒆜𒆜🍆𒆜𒆜🧿𒆜𒆜🌹𒆜𒆜🌵𒆜𒆜🐢𒆜𒆜🐲𒆜𒆜🐍𒆜𒆜🥵𒆜𒆜💖𒆜𒆜💦𒆜𒆜⚡𒆜𒆜👅𒆜𒆜👄𒆜𒆜💥𒆜𒆜💨𒆜𒆜🍑𒆜𒆜🍒𒆜𒆜🥵𒆜𒆜💦𒆜𒆜🧿",
]

REPLY_MESSAGES = [
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𝐒𝐀𝐑𝐖𝐀𝐍 𝐊𝐀 🍆🍆",
    "{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐧e 𝐬𝐨 𝐬𝐚𝐝 🍷🥂",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛",
    "{target}  𝐂𝐇𝐔𝐏 𝐊𝐑 𝐓𝐌𝐊𝐂 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐓𝐄𝐑𝐈 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈🤣 😍",
    "{target}  𝐒𝐀𝐑𝐖𝐀𝐍 𝐊𝐎 𝐁𝐀𝐀𝐏 𝐁𝐎𝐋 𝐂𝐇𝐀𝐋  𝐁𝐎𝐋 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈 🏑🏴‍☠️",
    "{target}  𝐓𝐄𝐑𝐈 𝐁𝐇𝐄𝐍 𝐊𝐈 𝐂𝐇𝐔𝐓 𝐌𝐀𝐑 𝐆𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ💀🤣",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐁𝐇𝐄𝐍 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐒𝐄 𝐒𝐀𝐓 𝐇𝐀𝐈 🇦🇱🚩",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐔𝐌𝐌𝐘 𝐊𝐈 𝐊𝐀𝐋𝐈 𝐂𝐇𝐔𝐓 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐈 M𝐔𝐇 𝐌𝐄 🍑() ",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆",
    "{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐧𝐚 𝐬𝐨 𝐬𝐚𝐝 🍷🥂",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛",
    "{target}  𝐂𝐇𝐔𝐏 𝐊𝐑 𝐓𝐌𝐊𝐂 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐓𝐄𝐑𝐈 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈🤣 😍",
    "{target}  𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐎 𝐁𝐀𝐀𝐏 𝐁𝐎𝐋 𝐂𝐇𝐀𝐋  𝐁𝐎𝐋 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐁𝐀𝐀𝐏 𝐇𝐀𝐈 🏑🏴‍☠️",
    "{target}  𝐓𝐄𝐑𝐈 𝐁𝐇𝐄𝐍 𝐊𝐈 𝐂𝐇𝐔𝐓 𝐌𝐀𝐑 𝐆𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ💀🤣",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐁𝐇𝐄𝐍 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐒𝐄 CHUD TI 𝐇𝐀𝐈 🇦🇱🚩",
    "{target}  𝐓𝐄𝐑𝐈 𝐌𝐔𝐌𝐌𝐘 𝐊𝐈 𝐊𝐀𝐋𝐈 𝐂𝐇𝐔𝐓 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐈 M𝐔𝐇 𝐌𝐄 🍑() ",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆",
    "{target}  𝐂𝐇𝐀𝐋 𝐓𝐌𝐊𝐂 𝐋𝐔𝐍𝐃 𝐂𝐇𝐔𝐒 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐊𝐀 🍆🍆",
]

SPAM_MESSAGE_TEMPLATE = """ {target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐧𝐚 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 💦






{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐧𝐚 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 💦






{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐧𝐚 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 💦






{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 Sar𝐖an 𝐧𝐚 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 💦





{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐧𝐚 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 💦






{target}  𝐓𝐄𝐑𝐈 𝐛𝐚𝐡𝐚𝐧 𝐤𝐨 𝐧𝐚𝐧𝐠𝐚 𝐊𝐚𝐫𝐤𝐞 𝐜𝐡𝐨𝐝𝐚 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐧𝐚 𝐬𝐨 𝐬𝐚𝐝 🍷🥂 💦






{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛 💦






{target}  𝐓𝐄𝐑𝐈 𝐌𝐀 𝐊𝐀 𝐃𝐔𝐃𝐔 𝐏𝐈 𝐋𝐘𝐀 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ 𝐍𝐄 🍼🥛 💦





 """


def extract_retry_after(error_str):
    match = re.search(r'retry after (\d+)', error_str.lower())
    if match:
        return int(match.group(1))
    return None


class BotInstance:
    def __init__(self, bot_number, owner_id):
        self.bot_number = bot_number
        self.owner_id = owner_id
        self.sudo_users = set()
        self.active_spam_tasks = {}
        self.active_name_change_tasks = {}
        self.active_ncv2_tasks = {}
        self.active_ncv3_tasks = {}
        self.active_dotzkeng_tasks = {}
        self.active_curly_tasks = {}
        self.active_reply_tasks = {}
        self.active_reply_targets = {}
        self.pending_replies = {}
        self.chat_delays = {}
        self.chat_threads = {}
        self.locks = {}

    def get_lock(self, chat_id):
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]

    def is_owner(self, user_id):
        return user_id == self.owner_id or user_id in self.sudo_users

    async def sudo_command(self, update, context):
        if update.effective_user.id != self.owner_id:
            return

        if not context.args and not update.message.reply_to_message:
            await update.message.reply_text("Usage: -sudo @username or reply to a message with -sudo")
            return

        user_to_sudo = None
        if update.message.reply_to_message:
            user_to_sudo = update.message.reply_to_message.from_user.id
        else:
            arg = context.args[0]
            if arg.startswith("@"):
                await update.message.reply_text("Please reply to the user's message with -sudo to grant sudo.")
                return
            else:
                try:
                    user_to_sudo = int(arg)
                except ValueError:
                    await update.message.reply_text("Invalid User ID.")
                    return

        if user_to_sudo:
            self.sudo_users.add(user_to_sudo)
            await update.message.reply_text(f"User {user_to_sudo} granted SUDO powers! ✅")

    async def refresh_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        await update.message.reply_text(f"Bot {self.bot_number} is active and refreshed! ⚡")

    async def check_owner(self, update):
        user_id = update.effective_user.id
        if not self.is_owner(user_id):
            try:
                await update.message.reply_text(UNAUTHORIZED_MESSAGE)
            except Exception:
                pass
            return False
        return True

    async def start(self, update, context):
        if not await self.check_owner(update):
            return

        help_text = f"""
⚡  〔 𝐁𝐎𝐓 {self.bot_number} 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃 〕 ⚡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━𝐑𝐄𝐕𝐄𝐍𝐆𝐄𝐑━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚔️  [ 𝐑𝐄𝐕𝐄𝐍𝐆𝐄𝐑 SPAM ]🌚
➔  /target <t>       »  SPM + NCS  ✔️
➔  /spam <t>         »  SPM WITH THREADS  ✔️
➔  /reaply <t>       »  REAPLY ALL TRGT  ✔️

🔮  [ NAMECHANGER MULTI-VERSIONS ]
➔  /nc <t>           »  NC LOOP WITH THREADS  ✔️
➔  /Ncv2 <t>         »  NC LOOP WITH THREADS (V2)  ✔️
➔  /Ncv3 <t>         »  NC LOOP WITH THREADS (V3)  ✔️
➔  /ncv4 <t>         »  NC LOOP WITH THREADS (V4)  ✔️
➔  /ncv5 <t> <t>     »  NC LOOP WITH THREADS (V5)  ✔️
➔  /ncv6 <t> <t>     »  NC LOOP WITH THREADS (V6)  ✔️

⚙️  [ SYSTEM CONFIGURATION ]
➔  /ping             »  CHECK BOT LATENCY / SPEED  ✔️
➔  /gc               »  AUTH GC IMAGE CHANGER  ✔️
➔  /setgc <1 or 2>   »  SET IMAGE SLOT 1 OR 2  ✔️
➔  /delay <ms>       »  SET DELAY BETWEEN <1-10>  ✔️
➔  /threads <1-50>   »  SET THREADS FOR NC + SPM  ✔️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔱〔𝐌𝐄𝐍𝐔 𝐑𝐄𝐕𝐄𝐍𝐆𝐄𝐑 𝐊𝐎 𝐁𝐀𝐀𝐏 𝐁𝐎𝐋 𝐓𝐌𝐊𝐂 〕
"""
        await update.message.reply_text(help_text)

    async def name_change_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NAME_CHANGE_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] Name change LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NAME_CHANGE_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.1))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 1.0)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(1.0)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 1.0)
                    else:
                        await asyncio.sleep(1.0)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Name change LOOP #{worker_id} stopped after {success_count} changes")

    async def flower_nc_loop(self, chat_id, base_name, context):
        msg_index = 0
        num_messages = len(FLOWER_NC_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] FLOWER NC LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = FLOWER_NC_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] FLOWER NC LOOP stopped after {success_count} changes")

    async def nc_emo_loop(self, chat_id, base_name, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] NC EMO LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    emoji = random.choice(HEART_EMOJIS)
                    display_name = f"{emoji} {base_name} {emoji}"
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except Exception:
                    await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] NC EMO LOOP stopped after {success_count} changes")

    async def nc_v2_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NC_V2_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] NC V2 LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NC_V2_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] NC V2 LOOP #{worker_id} stopped after {success_count} changes")

    async def nc_v3_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NC_FLAG_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] NC V3 LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NC_FLAG_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] NC V3 LOOP #{worker_id} stopped after {success_count} changes")

    async def dotzkeng_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(DOTZKENG_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] DOTZKENG LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = DOTZKENG_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] DOTZKENG LOOP #{worker_id} stopped after {success_count} changes")

    async def curly_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NC_CURLY_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] CURLY LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    current_msg = NC_CURLY_MESSAGES[msg_index % num_messages]
                    display_name = current_msg.format(target=base_name)
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                    msg_index += 1
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.05))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 0.1)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 0.1)
                    else:
                        await asyncio.sleep(0.5)
                    msg_index += 1
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] CURLY LOOP #{worker_id} stopped after {success_count} changes")

    async def gc_loop(self, chat_id, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] GC LOOP started for chat {chat_id}")
        image_paths = ["gc_image_1.png", "gc_image_2.png"]
        msg_index = 0
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    available_images = [p for p in image_paths if os.path.exists(p)]
                    
                    if available_images:
                        current_path = available_images[msg_index % len(available_images)]
                        with open(current_path, 'rb') as photo:
                            await context.bot.set_chat_photo(chat_id=chat_id, photo=photo)
                        success_count += 1
                        msg_index += 1
                        await asyncio.sleep(max(delay, 2.0))
                    else:
                        await asyncio.sleep(5.0)
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 1.0)
                except Exception as e:
                    print(f"[Bot {self.bot_number}] GC Error: {e}")
                    await asyncio.sleep(5.0)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] GC LOOP stopped after {success_count} changes")

    async def set_gc_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        message = update.message
        photo = None
        
        if message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo[-1]
        elif message.photo:
            photo = message.photo[-1]
            
        if not photo:
            await update.message.reply_text("Usage: Reply to a photo with -setgc [1 or 2] or send a photo with -setgc [1 or 2] caption")
            return
            
        slot = "1"
        if context.args:
            if context.args[0] in ["1", "2"]:
                slot = context.args[0]
            
        filename = f"gc_image_{slot}.png"
        file = await context.bot.get_file(photo.file_id)
        await file.download_to_drive(filename)
        await update.message.reply_text(f"Group image saved to Slot {slot}! ✅ Use -gc to start the loop cycling between available images.")

    async def ping_command(self, update, context):
        if not await self.check_owner(update):
            return
        
        import time
        start_time = time.time()
        sent_message = await update.message.reply_text("Pinging...")
        end_time = time.time()
        
        latency = (end_time - start_time) * 1000
        await sent_message.edit_text(f"Bot {self.bot_number} Ping: {latency:.2f}ms ⚡")

    async def spam_loop(self, chat_id, target_name, context, worker_id):
        success_count = 0
        print(f"[Bot {self.bot_number}] Spam LOOP #{worker_id} started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                try:
                    spam_msg = SPAM_MESSAGE_TEMPLATE.format(target=target_name)
                    await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                    success_count += 1
                    await asyncio.sleep(max(delay, 0.1))
                except asyncio.CancelledError:
                    raise
                except RetryAfter as e:
                    wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                    await asyncio.sleep(wait_time + 1.0)
                except (TimedOut, NetworkError):
                    await asyncio.sleep(1.0)
                except Exception as e:
                    error_str = str(e).lower()
                    retry_after = extract_retry_after(error_str)
                    if retry_after:
                        await asyncio.sleep(retry_after + 1.0)
                    else:
                        await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Spam LOOP #{worker_id} stopped after {success_count} messages")

    async def reply_loop(self, chat_id, target_name, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] Reply LOOP started for chat {chat_id}")
        try:
            while True:
                delay = self.chat_delays.get(chat_id, 0)
                if chat_id in self.pending_replies and self.pending_replies[chat_id]:
                    async with self.get_lock(chat_id):
                        messages_to_reply = self.pending_replies[chat_id].copy()
                        self.pending_replies[chat_id] = []

                    for msg_id in messages_to_reply:
                        try:
                            reply_msg = random.choice(REPLY_MESSAGES).format(target=target_name)
                            await context.bot.send_message(
                                chat_id=chat_id, 
                                text=reply_msg,
                                reply_to_message_id=msg_id
                            )
                            success_count += 1
                            await asyncio.sleep(max(delay, 0.05))
                        except asyncio.CancelledError:
                            raise
                        except RetryAfter as e:
                            wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                            await asyncio.sleep(wait_time + 0.1)
                        except Exception:
                            await asyncio.sleep(0.5)
                else:
                    await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print(f"[Bot {self.bot_number}] Reply LOOP stopped after {success_count} replies")

    async def message_collector(self, update, context):
        if not update.message or not update.message.text:
            return

        text = update.message.text.lower()
        chat_id = update.effective_chat.id

        if "gulamchutiya" in text:
            await update.message.reply_text("𝗚𝗨𝗟𝗔𝗠 𝗧🇪🇷🇮 🇲🇦 🇵🇺🇷🇪 🇨🇴🇲 🇲🇪 🇨🇭🇺🇩 🇬🇾🇮 👑♥️")
            return

        if chat_id in self.active_reply_targets:
            msg_id = update.message.message_id
            async with self.get_lock(chat_id):
                if chat_id not in self.pending_replies:
                    self.pending_replies[chat_id] = []
                self.pending_replies[chat_id].append(msg_id)

    async def nc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /nc <name>")
            return

        base_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_name_change_tasks:
            old_tasks = self.active_name_change_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.name_change_loop(chat_id, base_name, context, i+1))
            tasks.append(task)

        self.active_name_change_tasks[chat_id] = tasks

        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ Name change LOOP started with {num_threads} threads!")

    async def stop_nc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_name_change_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Name change LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active name change loop!")

    async def spam_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /spam <target>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i+1))
            tasks.append(task)

        self.active_spam_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 💣 Spam LOOP started with {num_threads} threads! Running continuously...")

    async def stop_spam_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_spam_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Spam LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active spam loop!")

    async def target_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /target <name>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_name_change_tasks:
            old_tasks = self.active_name_change_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        if chat_id in self.active_spam_tasks:
            tasks = self.active_spam_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)

        nc_tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.name_change_loop(chat_id, target_name, context, i+1))
            nc_tasks.append(task)
        self.active_name_change_tasks[chat_id] = nc_tasks

        spam_tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i+1))
            spam_tasks.append(task)
        self.active_spam_tasks[chat_id] = spam_tasks

        total_threads = num_threads * 2
        await update.message.reply_text(f"[Bot {self.bot_number}] 🎯 target MODE: NC ({num_threads}) + SPAM ({num_threads}) = {total_threads} threads running!")

    async def reply_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /reply <target>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_reply_tasks:
            old_task = self.active_reply_tasks[chat_id]
            old_task.cancel()
            try:
                await old_task
            except asyncio.CancelledError:
                pass

        self.active_reply_targets[chat_id] = target_name
        self.pending_replies[chat_id] = []

        task = asyncio.create_task(self.reply_loop(chat_id, target_name, context))
        self.active_reply_tasks[chat_id] = task

        await update.message.reply_text(f"[Bot {self.bot_number}] 💬 Reply LOOP activated! Replying to every message...")

    async def stop_reply_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        if chat_id in self.active_reply_tasks:
            task = self.active_reply_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                    pass
            del self.active_reply_tasks[chat_id]

        if chat_id in self.active_reply_targets:
            del self.active_reply_targets[chat_id]

        if chat_id in self.pending_replies:
            del self.pending_replies[chat_id]

        await update.message.reply_text(f"[Bot {self.bot_number}] Reply LOOP stopped!")

    async def delay_command(self, update, context):
        if not await self.check_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: /delay <seconds>")
            return

        try:
            delay = float(context.args[0])
            if delay < 0:
                await update.message.reply_text("Delay must be >= 0")
                return

            chat_id = update.effective_chat.id
            self.chat_delays[chat_id] = delay
            await update.message.reply_text(f"[Bot {self.bot_number}] Delay set to {delay}s (applies to all loops)")
        except ValueError:
            await update.message.reply_text("Invalid delay value!")

    async def threads_command(self, update, context):
        if not await self.check_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: /threads <number>")
            return

        try:
            threads = int(context.args[0])
            if threads < 1 or threads > 50:
                await update.message.reply_text("Threads must be between 1 and 50")
                return

            chat_id = update.effective_chat.id
            self.chat_threads[chat_id] = threads
            await update.message.reply_text(f"[Bot {self.bot_number}] Threads set to {threads} (applies to NC + SPAM)")
        except ValueError:
            await update.message.reply_text("Invalid threads value!")

    async def stop_all_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id
        stopped = []

        task_categories = [
            (self.active_name_change_tasks, "name change loop"),
            (self.active_ncv2_tasks, "nc v2 loop"),
            (self.active_ncv3_tasks, "nc v3 loop"),
            (self.active_dotzkeng_tasks, "dotzkeng loop"),
            (self.active_curly_tasks, "curly loop"),
            (self.active_spam_tasks, "spam loop")
        ]

        for task_dict, label in task_categories:
            if chat_id in task_dict:
                tasks = task_dict[chat_id]
                if not isinstance(tasks, list):
                    tasks = [tasks]
                for task in tasks:
                    task.cancel()
                for task in tasks:
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                del task_dict[chat_id]
                stopped.append(label)

        if chat_id in self.active_reply_tasks:
            task = self.active_reply_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_reply_tasks[chat_id]
            stopped.append("reply loop")

        if chat_id in self.active_reply_targets:
            del self.active_reply_targets[chat_id]

        if chat_id in self.pending_replies:
            del self.pending_replies[chat_id]

        if hasattr(self, 'active_gc_tasks') and chat_id in self.active_gc_tasks:
            task = self.active_gc_tasks[chat_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_gc_tasks[chat_id]
            stopped.append("gc loop")

        if stopped:
            await update.message.reply_text(f"[Bot {self.bot_number}] Stopped: {', '.join(stopped)} ✅")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active loops to stop!")

    async def flower_nc_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: -flowernc <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        
        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks: task.cancel()
            del self.active_name_change_tasks[chat_id]
            
        task = asyncio.create_task(self.flower_nc_loop(chat_id, base_name, context))
        self.active_name_change_tasks[chat_id] = [task]
        await update.message.reply_text(f"[Bot {self.bot_number}] 🌸 FLOWER NC LOOP started!")

    async def nc_emo_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: /ncemo <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        if chat_id in self.active_name_change_tasks:
            tasks = self.active_name_change_tasks[chat_id]
            for task in tasks: task.cancel()
            del self.active_name_change_tasks[chat_id]
        task = asyncio.create_task(self.nc_emo_loop(chat_id, base_name, context))
        self.active_name_change_tasks[chat_id] = [task]
        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ NC EMO LOOP started!")

    async def ncv2_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: /ncv2 <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        if chat_id in self.active_ncv2_tasks:
            old_tasks = self.active_ncv2_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.nc_v2_loop(chat_id, base_name, context, i+1))
            tasks.append(task)
        self.active_ncv2_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 🌙 NC V2 LOOP started with {num_threads} threads!")

    async def stop_ncv2_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_ncv2_tasks:
            tasks = self.active_ncv2_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_ncv2_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] NC V2 LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active NC V2 loop!")

    async def ncv3_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: /ncv3 <name>")
            return
        base_name = " ".join(context.args)
        chat_id = chat.id
        if chat_id in self.active_ncv3_tasks:
            old_tasks = self.active_ncv3_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.nc_v3_loop(chat_id, base_name, context, i+1))
            tasks.append(task)
        self.active_ncv3_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] 🚩 NC V3 LOOP started with {num_threads} threads!")

    async def stop_ncv3_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_ncv3_tasks:
            tasks = self.active_ncv3_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_ncv3_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] NC V3 LOOP stopped!")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active NC V3 loop!")

    async def dotzkeng_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: -dotzkeng <name>")
            return

        base_name = " ".join(context.args)
        chat_id = chat.id

        if chat_id in self.active_dotzkeng_tasks:
            old_tasks = self.active_dotzkeng_tasks[chat_id]
            for task in old_tasks:
                task.cancel()
            for task in old_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        num_threads = self.chat_threads.get(chat_id, 1)
        tasks = []
        for i in range(num_threads):
            task = asyncio.create_task(self.dotzkeng_loop(chat_id, base_name, context, i+1))
            tasks.append(task)

        self.active_dotzkeng_tasks[chat_id] = tasks
        await update.message.reply_text(f"[Bot {self.bot_number}] ⚡ DOTZKENG LOOP started with {num_threads} threads!")

    async def stop_dotzkeng_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_dotzkeng_tasks:
            tasks = self.active_dotzkeng_tasks[chat_id]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_dotzkeng_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ LOOP stopped!")
        else:
            await update.message.reply_text("No active 𓆰𓆩⃟𝐏𝐑𝐈𝐍𝐂𝐄ꪶ LOOP found.")

    async def nccurly_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        if not context.args:
            await update.message.reply_text("Usage: -nccurly <name>")
            return
        
        target_name = " ".join(context.args)
        chat_id = chat.id
        threads = self.chat_threads.get(chat_id, 1)

        if chat_id in self.active_curly_tasks:
            for task in self.active_curly_tasks[chat_id]:
                task.cancel()
        
        self.active_curly_tasks[chat_id] = []
        for i in range(threads):
            task = asyncio.create_task(self.curly_loop(chat_id, target_name, context, i+1))
            self.active_curly_tasks[chat_id].append(task)
        
        await update.message.reply_text(f"[Bot {self.bot_number}] Double Curly loop started for '{target_name}' with {threads} threads! 🌀")

    async def stop_nccurly_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_curly_tasks:
            for task in self.active_curly_tasks[chat_id]:
                task.cancel()
            for task in self.active_curly_tasks[chat_id]:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            del self.active_curly_tasks[chat_id]
            await update.message.reply_text(f"[Bot {self.bot_number}] Double Curly loop stopped! 🛑")
        else:
            await update.message.reply_text(f"[Bot {self.bot_number}] No active Double Curly loop!")

    async def gc_command(self, update, context):
        if not await self.check_owner(update):
            return
        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return
        chat_id = chat.id
        task = asyncio.create_task(self.gc_loop(chat_id, context))
        if not hasattr(self, 'active_gc_tasks'): self.active_gc_tasks = {}
        self.active_gc_tasks[chat_id] = task
        await update.message.reply_text(f"[Bot {self.bot_number}] 🖼️ Group Image Change LOOP started!")


def create_bot_application(token, bot_number, owner_id):
    application = Application.builder().token(token).build()
    bot_instance = BotInstance(bot_number, owner_id)

    application.add_handler(CommandHandler("start", bot_instance.start))
    application.add_handler(CommandHandler("nc", bot_instance.nc_command))
    application.add_handler(CommandHandler("ncemo", bot_instance.nc_emo_command))
    application.add_handler(CommandHandler("ncv2", bot_instance.ncv2_command))
    application.add_handler(CommandHandler("ncv3", bot_instance.ncv3_command))
    application.add_handler(CommandHandler("stopnc", bot_instance.stop_nc_command))
    application.add_handler(CommandHandler("stopncv2", bot_instance.stop_ncv2_command))
    application.add_handler(CommandHandler("stopncv3", bot_instance.stop_ncv3_command))
    application.add_handler(CommandHandler("spam", bot_instance.spam_command))
    application.add_handler(CommandHandler("stopspam", bot_instance.stop_spam_command))
    application.add_handler(CommandHandler("target", bot_instance.target_command))
    application.add_handler(CommandHandler("reply", bot_instance.reply_command))
    application.add_handler(CommandHandler("stopreply", bot_instance.stop_reply_command))
    application.add_handler(CommandHandler("delay", bot_instance.delay_command))
    application.add_handler(CommandHandler("threads", bot_instance.threads_command))
    application.add_handler(CommandHandler("stopall", bot_instance.stop_all_command))
    application.add_handler(CommandHandler("gc", bot_instance.gc_command))
    application.add_handler(CommandHandler("sudo", bot_instance.sudo_command))

    async def prefix_handler(update, context):
        if not update.message or not update.message.text:
            return
        text = update.message.text
        if text.startswith('-'):
            parts = text[1:].split()
            if not parts:
                return
            command = parts[0].lower()
            context.args = parts[1:]
            
            cmd_map = {
                "start": bot_instance.start,
                "nc": bot_instance.nc_command,
                "stopnc": bot_instance.stop_nc_command,
                "spam": bot_instance.spam_command,
                "stopspam": bot_instance.stop_spam_command,
                "delay": bot_instance.delay_command,
                "threads": bot_instance.threads_command,
                "target": bot_instance.target_command,
                "stopall": bot_instance.stop_all_command,
                "ncv2": bot_instance.ncv2_command,
                "stopncv2": bot_instance.stop_ncv2_command,
                "ncv3": bot_instance.ncv3_command,
                "stopncv3": bot_instance.stop_ncv3_command,
                "dotzkeng": bot_instance.dotzkeng_command,
                "stopdotzkeng": bot_instance.stop_dotzkeng_command,
                "flowernc": bot_instance.flower_nc_command,
                "ncemo": bot_instance.nc_emo_command,
                "reply": bot_instance.reply_command,
                "stopreply": bot_instance.stop_reply_command,
                "gc": bot_instance.gc_command,
                "sudo": bot_instance.sudo_command,
                "refresh": bot_instance.refresh_command,
            }
            
            if command in cmd_map:
                await cmd_map[command](update, context)
            elif command == "flowernc":
                await bot_instance.flower_nc_command(update, context)

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), prefix_handler))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, bot_instance.message_collector))

    return application


async def run_bot(token, bot_number, owner_id):
    max_retries = 30
    retry_delay = 15

    for attempt in range(max_retries):
        application = Application.builder().token(token).build()
        bot_instance = BotInstance(bot_number, owner_id)

        application.add_handler(CommandHandler("start", bot_instance.start))
        application.add_handler(CommandHandler("nc", bot_instance.nc_command))
        application.add_handler(CommandHandler("ncemo", bot_instance.nc_emo_command))
        application.add_handler(CommandHandler("ncv2", bot_instance.ncv2_command))
        application.add_handler(CommandHandler("ncv3", bot_instance.ncv3_command))
        application.add_handler(CommandHandler("nccurly", bot_instance.nccurly_command))
        application.add_handler(CommandHandler("stopnc", bot_instance.stop_nc_command))
        application.add_handler(CommandHandler("stopncv2", bot_instance.stop_ncv2_command))
        application.add_handler(CommandHandler("stopncv3", bot_instance.stop_ncv3_command))
        application.add_handler(CommandHandler("stopnccurly", bot_instance.stop_nccurly_command))
        application.add_handler(CommandHandler("dotzkeng", bot_instance.dotzkeng_command))
        application.add_handler(CommandHandler("stopdotzkeng", bot_instance.stop_dotzkeng_command))
        application.add_handler(CommandHandler("flowernc", bot_instance.flower_nc_command))
        application.add_handler(CommandHandler("spam", bot_instance.spam_command))
        application.add_handler(CommandHandler("stopspam", bot_instance.stop_spam_command))
        application.add_handler(CommandHandler("target", bot_instance.target_command))
        application.add_handler(CommandHandler("reply", bot_instance.reply_command))
        application.add_handler(CommandHandler("stopreply", bot_instance.stop_reply_command))
        application.add_handler(CommandHandler("delay", bot_instance.delay_command))
        application.add_handler(CommandHandler("threads", bot_instance.threads_command))
        application.add_handler(CommandHandler("stopall", bot_instance.stop_all_command))
        application.add_handler(CommandHandler("gc", bot_instance.gc_command))
        application.add_handler(CommandHandler("setgc", bot_instance.set_gc_command))
        application.add_handler(CommandHandler("ping", bot_instance.ping_command))
        application.add_handler(CommandHandler("sudo", bot_instance.sudo_command))
        application.add_handler(CommandHandler("refresh", bot_instance.refresh_command))

        async def prefix_handler(update, context):
            if not update.message or not update.message.text:
                return
            text = update.message.text
            if text.startswith('-'):
                parts = text[1:].split()
                if not parts:
                    return
                command = parts[0].lower()
                context.args = parts[1:]
                
                cmd_map = {
                    "start": bot_instance.start,
                    "nc": bot_instance.nc_command,
                    "stopnc": bot_instance.stop_nc_command,
                    "spam": bot_instance.spam_command,
                    "stopspam": bot_instance.stop_spam_command,
                    "delay": bot_instance.delay_command,
                    "threads": bot_instance.threads_command,
                    "target": bot_instance.target_command,
                    "stopall": bot_instance.stop_all_command,
                    "ncv2": bot_instance.ncv2_command,
                    "stopncv2": bot_instance.stop_ncv2_command,
                    "ncv3": bot_instance.ncv3_command,
                    "stopncv3": bot_instance.stop_ncv3_command,
                    "nccurly": bot_instance.nccurly_command,
                    "stopnccurly": bot_instance.stop_nccurly_command,
                    "dotzkeng": bot_instance.dotzkeng_command,
                    "stopdotzkeng": bot_instance.stop_dotzkeng_command,
                    "flowernc": bot_instance.flower_nc_command,
                    "ncemo": bot_instance.nc_emo_command,
                    "reply": bot_instance.reply_command,
                    "stopreply": bot_instance.stop_reply_command,
                    "ping": bot_instance.ping_command,
                    "gc": bot_instance.gc_command,
                    "setgc": bot_instance.set_gc_command,
                    "sudo": bot_instance.sudo_command,
                    "refresh": bot_instance.refresh_command,
                }
                
                if command in cmd_map:
                    await cmd_map[command](update, context)
            else:
                await bot_instance.message_collector(update, context)

        application.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), prefix_handler))

        try:
            await application.initialize()
            await application.start()
            if application.updater:
                await asyncio.sleep(0.1)
                await application.updater.start_polling(drop_pending_updates=True)
            print(f"Bot {bot_number} started successfully!")

            while True:
                await asyncio.sleep(3600)

        except Exception as e:
            error_str = str(e).lower()
            if "conflict" in error_str:
                print(f"Bot {bot_number} conflict (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                try:
                    if application.updater:
                        await application.updater.stop()
                    await application.stop()
                    await application.shutdown()
                except Exception:
                    pass
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay + 10, 200)
                continue
            else:
                print(f"Bot {bot_number} error: {e}")
                break
        finally:
            try:
                if application.updater:
                    await application.updater.stop()
                await application.stop()
                await application.shutdown()
            except Exception:
                pass
        break
    else:
        print(f"Bot {bot_number} failed after {max_retries} attempts - token may be used elsewhere")

async def main():
    print(f"Starting {len(BOT_TOKENS)} bots for owner ID: {OWNER_ID}")
    print("All actions (name change, spam, reply) run in LOOPS!")

    tasks = []
    for i, token in enumerate(BOT_TOKENS, 1):
        task = asyncio.create_task(run_bot(token, i, OWNER_ID))
        tasks.append(task)
        await asyncio.sleep(0.05)

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\nShutting down all bots...")


if __name__ == "__main__":
    asyncio.run(main())
