import asyncio
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEB_SERVICE_URL = "http://localhost:5000"
WEB_SERVICE_LOGIN = os.getenv('WEB_SERVICE_LOGIN')
WEB_SERVICE_PASSWORD = os.getenv('WEB_SERVICE_PASSWORD')
CHROMEDRIVER_PATH = "./chromedriver.exe"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_selenium_driver():
    chrome_options = Options()
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_and_get_code(driver):
    try:
        driver.get(f"{WEB_SERVICE_URL}/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(WEB_SERVICE_LOGIN)
        password_field.send_keys(WEB_SERVICE_PASSWORD)
        password_field.submit()

        generate_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Сгенерировать Код')]"))
        )

        generate_button.click()
        
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(By.ID, "codeDisplay").text != "---"
        )
        
        code_element = driver.find_element(By.ID, "codeDisplay")
        generated_code = code_element.text
        logger.info(f"Код получен: {generated_code}")

        return generated_code

    except Exception as e:
        logger.error(f"Ошибка бота-парсера: {e}")
        return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Используй /get_code для получения секретного кода."
    )

async def get_code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wait_message = await update.message.reply_text("Запускаю бота для получения кода...")

    code = await asyncio.get_event_loop().run_in_executor(None, _get_code_wrapper)

    await wait_message.delete()

    if code:
        await update.message.reply_text(f"SUCCESS : Ваш код: `{code}`", parse_mode='Markdown')
    else:
        await update.message.reply_text("FAILURE : Не удалось получить код")

def _get_code_wrapper():
    driver = setup_selenium_driver()
    try:
        return login_and_get_code(driver)
    finally:
        driver.quit()

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("get_code", get_code_command))
    application.run_polling()

if __name__ == '__main__':
    main()