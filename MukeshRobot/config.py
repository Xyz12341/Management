
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = "25614292" # integer value, dont use ""
    API_HASH = "59ee8005ce6b056fa639d956f028eeeb"
    TOKEN = "6909402640:AAErcuUlvVxg7NNbLT-_5SD1j90GkLqVpwE"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 7006715434 # If you dont know, run the bot and do /id in your private chat with it, also an integer
    
    SUPPORT_CHAT = "kittybothub"  # Your own group for support, do not add the @
    START_IMG = "https://telegra.ph/file/5618197d321f4f555bb9c.jpg"
    EVENT_LOGS = (-1002024032988)  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    MONGO_DB_URI= "mongodb+srv://chalcogen:dumb980@cluster0.u25jq25.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # RECOMMENDED
    DATABASE_URL = "postgresql://xrlkskby:gobwyeqocauwmdrggqom@alpha.mkdb.sh:5432/rjfvbvce"  # A sql database url from elephantsql.com
    CASH_API_KEY = (
        "4Z5UHYEW3LJ7U99J"  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "V33SSMCSDT6L"
    
    # Get your API key from https://timezonedb.com/api


    # Optional fields
    BL_CHATS = [] # List of groups that you want blacklisted.
    DRAGONS = [7006715434] # User id of sudo users
    DEV_USERS = [7006715434] # User id of dev users
    DEMONS = [7006715434]  # User id of support users
    TIGERS = [7006715434]  # User id of tiger users
    WOLVES = [7006715434]  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8
    

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
