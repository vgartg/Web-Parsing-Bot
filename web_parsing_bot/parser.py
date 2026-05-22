"""Selenium routines that log into the web service and scrape the generated code."""

from __future__ import annotations

import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .config import BotConfig

logger = logging.getLogger(__name__)


def build_driver(config: BotConfig) -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if config.chromedriver_path:
        service = Service(executable_path=config.chromedriver_path)
        return webdriver.Chrome(service=service, options=options)
    return webdriver.Chrome(options=options)


def login_and_get_code(driver: webdriver.Chrome, config: BotConfig, timeout: float = 10.0) -> str | None:
    """Performs a login + generate-code round trip and returns the scraped code."""
    try:
        driver.get(f"{config.web_service_url}/login")

        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.NAME, "username")))

        driver.find_element(By.NAME, "username").send_keys(config.web_service_login)
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(config.web_service_password)
        password_field.submit()

        generate_button = wait.until(EC.element_to_be_clickable((By.ID, "generateBtn")))
        generate_button.click()

        wait.until(lambda d: d.find_element(By.ID, "codeDisplay").text != "---")

        code = driver.find_element(By.ID, "codeDisplay").text
        logger.info("Код получен: %s", code)
        return code
    except Exception as exc:
        logger.error("Ошибка бота-парсера: %s", exc)
        return None


def fetch_code(config: BotConfig) -> str | None:
    driver = build_driver(config)
    try:
        return login_and_get_code(driver, config)
    finally:
        driver.quit()
