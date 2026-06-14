import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918914057:AAGoajYd1afX-aAvFLwHI2toeJ4pS1J0_R4")
CHANNEL = "@VALXOfficial"

logging.basicConfig(level=logging.INFO)

async def check_member(bot, user_id):
    try:
        m = await bot.get_chat_member(CHANNEL, user_id)
        return m.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_member(context.bot, update.effective_user.id):
        kb = [[InlineKeyboardButton("👑 Join VALX Official", url="https://t.me/VALXOfficial")],
              [InlineKeyboardButton("✅ I Joined", callback_data="check")]]
        await update.message.reply_text(
            "👑 *Welcome to VALX Bot*\n\nJoin our channel to access $VALX info.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb))
    else:
        await send_info(update.message.reply_text)

async def send_info(fn):
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
        "📢 @VALXOfficial | 🐦 @VALX\\_SOL\n\n"
        "🚀 Launch coming soon. Stay close. 🔱",
        parse_mode="Markdown")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if await check_member(context.bot, q.from_user.id):
        await q.message.delete()
        await send_info(q.message.reply_text)
    else:
        await q.answer("❌ Please join the channel first!", show_alert=True)

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("VALX Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
