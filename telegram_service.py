from pyrogram import Client


def send_telegram_text_as_me_to_bot(message):
    # Check if an argument is passed, and use it as the message
    # if len(sys.argv) > 1:
    #     message = sys.argv[1]
    # else:
    #     message = "Default message"  # You can set a default message here

    app = Client("my_account")

    async def main():
        async with app:
            await app.send_message("lunkstealth_bot", message)

    app.run(main())

send_telegram_text_as_me_to_bot("wussup?!")