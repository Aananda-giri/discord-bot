import telegram.ext

# with open('token.txt', 'r') as f:
#     TOKEN = f.read()
#     print(f'token:\'{TOKEN}\'')

def start(update, context):
    update.message.reply_text('Hello! welcome to neuralBot')

def help(update, context):
    update.message.reply_text("""
    The following commands are available:
    /start -> welcome Message
    /help -> This Message
    /content -> Information about neuralNone Content
    /contact -> Information about Contact
    """)
def content(update, context):
    update.message.reply_text("We have videos and books! watch and read them")

def contact(update, context):
    update.message.reply_text("You can contact Nathan on the discord server")

def start_bot(TOKEN):
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(telegram.ext.CommandHandler("start", start))
    disp.add_handler(telegram.ext.CommandHandler("help", help))
    disp.add_handler(telegram.ext.CommandHandler("content", content))
    disp.add_handler(telegram.ext.CommandHandler("contact", contact))

    updater.start_polling()
    # updater.idle()


