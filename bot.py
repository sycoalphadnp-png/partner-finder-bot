from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
"  # <-- Replace with your Telegram token

AGE, GENDER, LOOKING, CITY = range(4)

# Database
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLEimport os
TOKEN = os.getenv("8387773388:AAF4vj09znBOFqppb1Xbk2ZQsJBJA_3RWzw") IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    looking TEXT,
    city TEXT
)
""")
conn.commit()
