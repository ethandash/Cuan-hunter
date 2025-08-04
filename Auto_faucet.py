
# auto_faucet.py - Auto claim BNB & Polygon testnet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

# Ambil alamat wallet dari GitHub Secrets
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)

def claim_bnb():
    driver = create_driver()
    try:
        print("🔧 Membuka BNB Faucet...")
        driver.get("https://faucet.bnbchain.org")
        time.sleep(5)

        # Input wallet
        driver.find_element(By.XPATH, "//input[@type='text']").send_keys(WALLET_ADDRESS)
        time.sleep(2)

        # Klik tombol
        driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()
        time.sleep(5)

        print("✅ BNB Faucet: Claim submitted!")
        return "BNB: ✅ Claim berhasil!"
    except Exception as e:
        print(f"❌ BNB Faucet: Gagal - {e}")
        return "BNB: ❌ Gagal (sudah claim atau error)"
    finally:
        driver.quit()

def claim_polygon():
    driver = create_driver()
    try:
        print("🔧 Membuka Polygon Faucet...")
        driver.get("https://faucet.polygon.technology")
        time.sleep(5)

        # Input wallet
        driver.find_element(By.XPATH, "//input[@placeholder='Enter your address']").send_keys(WALLET_ADDRESS)
        time.sleep(2)

        # Klik tombol
        driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
        time.sleep(5)

        print("✅ Polygon Faucet: Claim submitted!")
        return "Polygon: ✅ Claim berhasil!"
    except Exception as e:
        print(f"❌ Polygon Faucet: Gagal - {e}")
        return "Polygon: ❌ Gagal (sudah claim atau error)"
    finally:
        driver.quit()

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        print("❌ Telegram tidak dikonfigurasi")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        import requests
        requests.post(url, data=payload)
        print("📤 Notif Telegram terkirim!")
    except Exception as e:
        print(f"❌ Gagal kirim Telegram: {e}")

def main():
    if not WALLET_ADDRESS:
        print("❌ WALLET_ADDRESS tidak diatur di Secrets!")
        return

    print(f"🚀 Mulai auto-claim untuk: {WALLET_ADDRESS[:10]}...")

    result_bnb = claim_bnb()
    result_polygon = claim_polygon()

    message = f"""
🧪 **Auto-Claim Testnet**  
{result_bnb}  
{result_polygon}  

💡 Cek dompet kamu di:  
- BNB Testnet: [https://testnet.bscscan.com](https://testnet.bscscan.com)  
- Polygon Testnet: [https://mumbai.polygonscan.com](https://mumbai.polygonscan.com)
"""
    send_telegram(message)

if __name__ == "__main__":
    main()
