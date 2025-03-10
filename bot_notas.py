from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters
from supabase import create_client, Client
import os

# Configura Supabase
SUPABASE_URL = "https://ydjccbucpabhizgcmily.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlkamNjYnVjcGFiaGl6Z2NtaWx5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwNjM4MTgsImV4cCI6MjA1NDYzOTgxOH0.-e8ooST4IfCiemzUT3pgw5bTTRrXGJzDrTKpd4SdidU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configura el bot de Telegram
TELEGRAM_TOKEN = "7470830401:AAGvoJXEEsRq3V6-Zp0s5I3SciV_Bjpq-x4"

# Función para manejar el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Bienvenido a ia_prueba_bot.\n\n"
        "Usa /notas <nombre_alumno> para obtener tus notas.\n"
        "Usa /contenido <tema> para obtener enlaces de descarga.\n"
        "Usa /cronograma <clases> para obtener el cronograma académico.\n"
    )

# Función para manejar el comando /notas
async def obtener_notas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre_alumno = " ".join(context.args)
    if not nombre_alumno:
        await update.message.reply_text("Por favor, ingresa tu nombre. Ejemplo: /notas Juan Pérez")
        return

    # Consulta la base de datos
    print(f"Consultando notas para: {nombre_alumno}")  # Depuración
    response = supabase.table("notas").select("*").eq("nombre_alumno", nombre_alumno).execute()
    notas = response.data
    print(f"Resultados de la consulta: {notas}")  # Depuración

    if notas:
        mensaje = f"Notas de {nombre_alumno}:\n"
        for nota in notas:
            mensaje += f"- {nota['nota']}\n"
        await update.message.reply_text(mensaje)
    else:
        await update.message.reply_text(f"No se encontraron notas para {nombre_alumno}.")

# Función para manejar el comando /contenido
async def obtener_contenido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tema = " ".join(context.args)
    if not tema:
        await update.message.reply_text("Por favor, ingresa un tema. Ejemplo: /contenido Álgebra")
        return

    # Consulta la base de datos para obtener el enlace del tema
    print(f"Consultando enlaces de descarga para: {tema}")  # Depuración
    response = supabase.table("contenido").select("*").eq("tema", tema).execute()
    contenido = response.data
    print(f"Resultados de la consulta: {contenido}")  # Depuración

    if contenido:
        mensaje = f"Enlaces de descarga para el tema '{tema}':\n"
        for descarga in contenido:
            mensaje += f"- {descarga['titulo']}: {descarga['link']}\n"
        await update.message.reply_text(mensaje)
    else:
        await update.message.reply_text(f"No se encontraron enlaces de descarga para el tema '{tema}'.")

# Función principal para ejecutar el bot
def main():
    # Crea la aplicación del bot
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Registra los manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("notas", obtener_notas))
    application.add_handler(CommandHandler("contenido", obtener_contenido))

    # Inicia el bot
    print("Bot en ejecución...")
    application.run_polling()

if __name__ == "__main__":
    main()
