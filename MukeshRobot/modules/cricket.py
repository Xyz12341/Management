import requests
from telegram import Update, ParseMode
from telegram.ext import CommandHandler, CallbackContext

# Add your CricAPI or another Cricket API key here
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

# Add this to your dispatcher or updater
dispatcher.add_handler(CommandHandler("cs", cricket_score))

__help__ = """
» Available commands for Cricket 

● /cs : get cricket live score.

(✿◠‿◠)"""

__mod_name__ = "Cricket"

