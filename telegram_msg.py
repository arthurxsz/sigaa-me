import asyncio
import telegram


bot = telegram.Bot(token=API)

async def send_message(text, chat_id = chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)

async def main():
    # Sending a message
    await send_message(text='LIBEROU VAGA', chat_id=chat_id)


if __name__ == '__main__':
    asyncio.run(main())
    