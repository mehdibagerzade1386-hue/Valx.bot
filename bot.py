import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918914057:AAHEaBklKqON0_ADLVUp0_7P5UzTaSWcLjg")
CHANNEL = "@VALXOfficial"
ADMIN_ID = None  # بعد پر میکنیم
WHITELIST_FILE = "whitelist.txt"
MAX_WHITELIST = 100

logging.basicConfig(level=logging.INFO)

def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return []
    with open(WHITELIST_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_to_whitelist(username, user_id):
    with open(WHITELIST_FILE, "a") as f:
        f.write(f"{len(load_whitelist())+1}|{user_id}|{username}\n")

async def check_member(bot, user_id):
    try:
        m = await bot.get_chat_member(CHANNEL, user_id)
        return m.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not await check_member(context.bot, user.id):
        kb = [[InlineKeyboardButton("👑 Join VALX Official", url="https://t.me/VALXOfficial")],
              [InlineKeyboardButton("✅ I Joined", callback_data="check")]]
        await update.message.reply_text(
            "👑 *Welcome to VALX Bot*\n\nJoin our channel to access $VALX info.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb))
    else:
        await register_and_send(update.message.reply_text, user)

async def register_and_send(fn, user):
    whitelist = load_whitelist()
    user_ids = [entry.split("|")[1] for entry in whitelist]
    spot = None

    if str(user.id) not in user_ids and len(whitelist) < MAX_WHITELIST:
        save_to_whitelist(user.username or user.first_name, user.id)
        whitelist = load_whitelist()
        spot = len(whitelist)

    await fn(
        "👑 *VALX — The New Standard*\n\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "🔱 *What is $VALX?*\n"
        "Not just a token. A standard.\n"
        "Built on Solana for those who see real value.\n\n"
        "💰 *Token Info:*\n"
        "• Ticker: $VALX\n"
        "• Chain: Solana\n"
        "• Contract: 🔜 Coming Soon\n\n"
        "⚡ *Why $VALX?*\n"
        "Real Value. Real Wealth.\n"
        "Early believers always win.\n\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        f"{'🎉 *You are whitelist member #' + str(spot) + ' of 100!* 👑' + chr(10) if spot else ''}"
        "📢 @VALXOfficial | 🐦 @VALX\\_SOL\n\n"
        "🚀 Launch coming soon. Stay close. 🔱",
        parse_mode="Markdown")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user = q.from_user
    if await check_member(context.bot, user.id):
        await q.message.delete()
        await register_and_send(q.message.reply_text, user)
    else:
        await q.answer("❌ Please join the channel first!", show_alert=True)

async def list_whitelist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_ID):
        return
    whitelist = load_whitelist()
    if not whitelist:
        await update.message.reply_text("Whitelist is empty.")
        return
    text = "👑 *Whitelist Members:*\n\n"
    for entry in whitelist:
        parts = entry.split("|")
        text += f"{parts[0]}. @{parts[2]} (ID: {parts[1]})\n"
    await update.message.reply_text(text, parse_mode="Markdown")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_whitelist))
    app.add_handler(CallbackQueryHandler(button))
    print("VALX Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
