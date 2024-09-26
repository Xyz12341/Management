import requests
from telegram import Update, ParseMode
from telegram.ext import CommandHandler, CallbackContext, Updater
import logging

# Set up logging for debugging purposes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Add your bot token and CricAPI or another Cricket API key here
BOT_TOKEN = '6909402640:AAErcuUlvVxg7NNbLT-_5SD1j90GkLqVpwE'
API_KEY = 'f77d8180-084b-4968-a2f0-177bebe802cb'
CRICKET_API_URL = f"https://cricapi.com/api/matches/?apikey={API_KEY}"

# Function to fetch live cricket score
def get_live_score():
    try:
        response = requests.get(CRICKET_API_URL)
        data = response.json()
        
        if 'matches' not in data:
            return "Couldn't retrieve any matches at the moment."

        live_matches = []
        for match in data['matches']:
            if match['matchStarted']:
                team1 = match['team-1']
                team2 = match['team-2']
                status = match['status']
                live_matches.append(f"{team1} vs {team2}\nStatus: {status}\n")
        
        if live_matches:
            return "\n\n".join(live_matches)
        else:
            return "No live matches at the moment."

    except Exception as e:
        return f"Error fetching live score: {str(e)}"

# Command handler for /cs
def cricket_score(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    live_score = get_live_score()
    context.bot.send_message(chat_id=chat_id, text=live_score, parse_mode=ParseMode.MARKDOWN)

def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f"Update {update} caused error {context.error}")

def main():
    # Initialize Updater with your bot token
    updater = Updater(token=BOT_TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # Register the cricket score command
    dispatcher.add_handler(CommandHandler("cs", cricket_score))
    
    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()

__help__ = """
» Available commands for Cricket 

● /cs : Get live cricket score.

(✿◠‿◠)
"""

__mod_name__ = "Cricket"
