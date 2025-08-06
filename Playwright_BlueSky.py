from asyncio import wait_for

from playwright.sync_api import sync_playwright
import time
from datetime import datetime

stamp = datetime.now().strftime("%Y-%m-%d-%H.%M.%S")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("https://bsky.app")

    page.click('button[aria-label="Войти"]')
    print('✅ Нажата кнопка "Войти"')

    page.get_by_placeholder("Псевдоним или электронная почта").fill("qatest.06082025@gmail.com")
    print('✅ В поле "Псевдоним или электронная почта" введена почта "qatest.06082025@gmail.com"')

    page.get_by_placeholder("Пароль").fill("123459_BlueSky")
    print('✅ В поле "Пароль" введен пароль "123459_BlueSky"')

    page.click('button[aria-label="Далее"]')
    print('✅ Нажата кнопка "Далее"')


    if page.is_visible('button[class="css-g5y9jx r-1loqt21 r-1otgn73"]') is True:
        print("✅ 1/3 Тест прошёл")

    else:
        print('❌ 1/3 Тест не прошёл')


    a = page.get_by_label("Discover")
    time.sleep(2)
    if a.is_visible():
        print("✅ 2/3 Тест прошёл")
    else:
        print("❌ 2/3 Тест не прошёл")


    if page.is_visible('button[aria-label="Найти людей, чтобы подписаться"]') is True:
        print("✅ 3/3 Тест прошёл")

    else:
        print('❌ 3/3 Тест не прошёл')

    browser.close()