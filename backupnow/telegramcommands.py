from telegram import Update, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

api_token = '6127325854:AAGsCeqD6SZApUMGU5yWHmMpwX0Y7TNLRpY'
chat_id = '-1001926809085'

def callcolor():
    from main import maintotelegramColorStatus
    result = maintotelegramColorStatus()
    return result


def statusmapping(color):
    color_mapping = {
        "Green": 'Baseline(Normal Monitoring)',
        "Yellow": 'Normal(Alert or Ready)',
        "Orange": 'Warning(Pre-Emptive Evacuation',
        "Red": 'Evacuate(Assisted Evacuation)',
    }
    return color_mapping.get(color, -1)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! This is your bot.')


# Define a function to handle commands other than /start
def handle_commands(update: Update, context: CallbackContext):
    # Get the text of the incoming message
    text = update.message.text

    # Check if the message starts with "/"
    if text.startswith('/'):
        colorget = callcolor()
        #print(colorget)
        # Split the message into command and arguments
        command, *args = text[1:].split()
        # Handle different commands here
        if 'image' in command:
            image_path = 'picture.jpg' # change to camera live image
            update.message.reply_photo(open(image_path, 'rb'))
        elif 'help' in command:
            update.message.reply_text('Use "/" commands. ')
        elif 'status' in command:
            update.message.reply_text(f'Warning Code:{colorget}\n'
                                      f'Status:{statusmapping(colorget)}')
        elif 'contact' in command:
            update.message.reply_text('EMERGENCY CONTACTS: 09123456789')
        # Add more commands as needed
        else:
            update.message.reply_text('I can only understand commands starting with "/."')

# Define a function to handle all non-command messages
def handle_non_commands(update: Update, context: CallbackContext):
    text = update.message.text
    # Check if the message starts with "/"
    if not text.startswith('/'):
        # Delete the incoming message
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


def telegram():
    # Replace 'YOUR_BOT_TOKEN' with your Telegram Bot API token
    updater = Updater(token=api_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler('start', start))

    # Register a message handler for non-command messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_non_commands))

    # Register a message handler to handle commands
    dp.add_handler(MessageHandler(Filters.text & Filters.command, handle_commands))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it (e.g., Ctrl+C)
    updater.idle()
