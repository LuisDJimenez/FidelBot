import unicodedata

from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters     

import os

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME = '@FidelSingaoBot'

#Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
         f"Hola, soy {BOT_USERNAME}, intenta decir algo como 'Raul' o 'Fidel'.\n"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Ayuda? Eso pideselo a los Rusos. \n'
        'Puedes decir "Raul" o "Fidel" para ver que pienso de ellos.\n'
    
    )

# Normalize text function
def normalize_text(text: str) -> str:
    # Remove accents and make lowercase
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()



#Responses
def handle_response(text: str) -> str:
    normalized = normalize_text(text)

    if 'raul' in normalized:
        return 'Ay Mi Hermanita'
    
    if 'fidel' in normalized:
        return 'Viva la Robolucion'

    if 'rogelio' in normalized:
        return 'Ese es un chivato'
    
    if 'canel' in normalized:
        return 'Ese un SINGAO!'
    
    if 'limon' in normalized:
        return 'La base de todo'
    
    if 'resingo' in normalized or 'cago' in normalized:
        return 'Te voy a desaparecer como a Camilo'
    
    if 'camilo' in normalized:
        return 'A ese lo desaparecio mi hermana Raul'

    if 'etecsa' in normalized:
        return 'NO AL TARIFAZO DE ETECSA!'
    
    if 'humberto' in normalized or 'humbertico' in normalized:
        return 'Apex Chivatente'   

    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type = update.message.chat.type
        text: str = update.message.text

        print(f'user({update.effective_user.id}) in chat {message_type}: "{text}"')

        response = handle_response(text)
        if response:
            await update.message.reply_text(response)
        else:
            if message_type == 'private':
                await update.message.reply_text('No entendí eso. ¿Quieres hablar de Raul o Fidel?')
            print("No matching response found.")

        

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    application = ApplicationBuilder().token(TOKEN).build()

    #Commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))

    #Messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    #Error Handler
    application.add_error_handler(error)

    #Run the bot
    print('Polling for updates...')
    application.run_polling()
