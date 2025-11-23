import logging
import asyncio 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from inference_engine import InferenceEngine

TOKEN = "" 

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

engine = InferenceEngine()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Determine which group they are in (for your own debugging)
    group = "A (Rules)" if user_id % 2 == 0 else "B (AI)"
    
    await update.message.reply_text(
        f"👋 **Welcome.**\n\n"
        f"I am your AI Journaling Assistant.\n"
        f"Just write down what's on your mind. I will help you spot unhelpful thinking patterns.\n\n"
        f"_(Research Debug: You are in Group {group})_" 
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    
    await asyncio.sleep(1) 
    
    # 1. Predict
    label, system_used = engine.predict(user_text, user_id)
    
    engine.log_interaction(user_id, user_text, label, system_used, feedback="PENDING")
    
    # 2. Store context
    context.user_data['last_text'] = user_text
    context.user_data['last_label'] = label
    context.user_data['last_system'] = system_used
    
    # 3. Formulate Response (Softer, more therapeutic tone)
    response_text = ""
    
    if label == "ALL_OR_NOTHING":
        response_text = (
            "⛓️ **I noticed a pattern here.**\n\n"
            "This sounds like **All-or-Nothing Thinking** (viewing things in black-and-white terms).\n\n"
            "💡 *Reflect:* Are you using words like 'always', 'never', or 'everyone'? Is the situation really that absolute?"
        )
    elif label == "MIND_READING":
        response_text = (
            "🔮 **I noticed a pattern here.**\n\n"
            "This sounds like **Mind Reading** (assuming you know what others are thinking).\n\n"
            "💡 *Reflect:* Do you have solid evidence for this thought, or is it an assumption?"
        )
    else:
        # Neutral response - validate without analyzing
        response_text = "Thank you for sharing that. 🍃\n\n*Journaling is a great way to process emotions. Keep going if you'd like.*"

    # 4. Feedback Buttons (Only show if a distortion was found)
    reply_markup = None
    if label != "NEUTRAL_DISTRESS":
        keyboard = [
            [
                InlineKeyboardButton("👍 Helpful", callback_data='helpful'),
                InlineKeyboardButton("👎 Off base", callback_data='not_helpful')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(response_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    feedback = query.data
    user_id = update.effective_user.id
    
    # Retrieve data
    text = context.user_data.get('last_text', 'N/A')
    label = context.user_data.get('last_label', 'N/A')
    system = context.user_data.get('last_system', 'N/A')
    
    engine.log_interaction(user_id, text, label, system, feedback)
    
    msg = "✅ Thanks for the feedback." if feedback == 'helpful' else "📝 Thanks. I'll learn from this."
    await query.edit_message_text(text=msg)

if __name__ == '__main__':
    if TOKEN == "":
        print("❌ ERROR: Token missing.")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        application.add_handler(CallbackQueryHandler(button_click))
        application.run_polling()