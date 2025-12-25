from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
import sqlite3

# Bot token (your token)
TOKEN = "8387773388:AAF4vj09znBOFqppb1Xbk2ZQsJBJA_3RWzw"

# Conversation states
AGE, GENDER, LOOKING, CITY = range(4)

# Database setup
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    looking TEXT,
    city TEXT
)
""")
conn.commit()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Partner Finder Bot!\n⚠️ 18+ only\n\nEnter your age:"
    )
    return AGE

# Ask age
async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = update.message.text
    if not age.isdigit() or int(age) < 18:
        await update.message.reply_text("❌ You must be 18+. Enter valid age:")
        return AGE
    context.user_data["age"] = age
    reply = ReplyKeyboardMarkup([["Male", "Female"]], one_time_keyboard=True)
    await update.message.reply_text("Select your gender:", reply_markup=reply)
    return GENDER

# Ask gender
async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gender"] = update.message.text
    reply = ReplyKeyboardMarkup([["Male", "Female"]], one_time_keyboard=True)
    await update.message.reply_text("Looking for:", reply_markup=reply)
    return LOOKING

# Ask looking for
async def looking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["looking"] = update.message.text
    await update.message.reply_text("Enter your city:")
    return CITY

# Ask city and save profile
async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    user_id = update.message.from_user.id
    data = context.user_data

    c.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)",
        (user_id, data["age"], data["gender"], data["looking"], data["city"])
    )
    conn.commit()

    await update.message.reply_text("✅ Profile saved!\nUse /find to find partners.")
    return ConversationHandler.END

# Find partner command
async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    c.execute("SELECT looking FROM users WHERE user_id=?", (user_id,))
    me = c.fetchone()
    if not me:
        await update.message.reply_text("❌ Create profile first using /start")
        return

    looking_for = me[0]
    c.execute(
        "SELECT age, gender, city FROM users WHERE gender=? AND user_id!=?",
        (looking_for, user_id)
    )
    match = c.fetchone()
    if match:
        await update.message.reply_text(
            f"💖 Match Found!\nAge: {match[0]}\nGender: {match[1]}\nCity: {match[2]}"
        )
    else:
        await update.message.reply_text("😔 No matches found yet.")

# Main function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            LOOKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, looking)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, city)],
        },
        fallbacks=[]
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("find", find))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
