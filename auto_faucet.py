# auto_faucet.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

WALLET = os.getenv("WALLET_ADDRESS")

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def claim_bnb():
    driver = get_driver()
    try:
        driver.get("https://faucet.bnbchain.org")
        time.sleep(5)
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(WALLET)
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
        time.sleep(5)
        return "BNB: ✅"
    except Exception as e:
        return "BNB: ❌"
    finally:
        driver.quit()

def claim_polygon():
    driver = get_driver()
    try:
        driver.get("https://faucet.polygon.technology")
        time.sleep(5)
        driver.find_element(By.XPATH, "//input[@placeholder='Enter your address']").send_keys(WALLET)
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
        time.sleep(5)
        return "Polygon: ✅"
    except Exception as e:
        return "Polygon: ❌"
    finally:
        driver.quit()

def main():
    if not WALLET:
        print("❌ WALLET_ADDRESS tidak diatur!")
        return

    print(f"🚀 Mulai auto-claim untuk: {WALLET[:10]}...")
    result_bnb = claim_bnb()
    result_polygon = claim_polygon()

    # Kirim ke Telegram
    send_telegram(f"🧪 Auto-Claim Testnet\n{result_bnb}\n{result_polygon}")

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        import requests
        requests.post(url, data=data)
    except:
        pass

if __name__ == "__main__":
    main()
