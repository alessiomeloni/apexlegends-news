import emoji
import asyncio
import logging
import apexLegendsNews
from aiogram import Bot, Dispatcher, executor, types

######## TelegramBot Setup ########
bot = Bot(token="856854877:AAE1DGoiZ-PxgH6bnArEiemZRcUTMP7T8dg")
dp = Dispatcher(bot)
######## TelegramBot Setup ########

######## logging Setup ########
FORMAT = "[%(asctime)s] - %(levelname)s : %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
######## logging Setup ########


class emoji:
    Email = emoji.emojize(":envelope_with_arrow:", use_aliases=True)
    NoProblem = emoji.emojize(":white_circle:", use_aliases=True)
    Error = emoji.emojize(":red_circle:", use_aliases=True)


async def newsLoop(message):
    channel = "@apexlegendsit"
    maxRetry = 5
    await message.reply(f"{emoji.NoProblem} Il bot è stato avviato")

    while True:
        title, news, image = apexLegendsNews.engine()
        retry = 1
        for retry in range(retry, maxRetry):
            retry = 1
            try:
                # telegram message
                logging.info("Processing Telegram Feed")
                await bot.send_message(
                    channel,
                    f"#NEWS\n{emoji.Email} *{title}*\n\n[{emoji.NoProblem}]({image}) _{news}_ ",
                    parse_mode="Markdown",
                )
                await bot.send_message(
                    message.chat.id, f"{emoji.Email} Telegram Feed: SENT"
                )
                logging.info("Telegram Feed: SENT")
                break
            except Exception as e:
                logging.info("Telegram Feed: ERROR")
                await bot.send_message(
                    message.chat.id, f"{emoji.Error} Telegram Feed: ERROR"
                )
                await bot.send_message(
                    message.chat.id,
                    f"#####CONSOLE#####\n`{e}`\n#####CONSOLE#####",
                    parse_mode="Markdown",
                )
                await bot.send_message(
                    message.chat.id, f"{emoji.Error} Riprovo[{retry}]"
                )

        await asyncio.sleep(5)


@dp.message_handler(commands=["start"])
async def newsLoopStarter(message: types.Message):
    await newsLoop(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
else:
    logging.info("I'm not a Module")
