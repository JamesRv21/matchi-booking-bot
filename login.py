from playwright.sync_api import sync_playwright
import json
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("MATCHI_USERNAME")
PASSWORD = os.getenv("MATCHI_PASSWORD")

def save_cookies(context, filename="cookies.json"):
    cookies = context.cookies()
    with open(filename, "w") as f:
        json.dump(cookies, f)
    print(f"[+] Saved cookies to {filename}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the login page
    page.goto("https://www.matchi.se/login")

    # Accept cookies if prompt appears
    try:
        page.locator("text=ACCEPT ALL").click(timeout=3000)
        print("[✓] Accepted cookies")
    except:
        print("[!] No cookie prompt found or it was already accepted")

    # Fill and submit login form
    page.fill("input[name='j_username']", EMAIL)
    page.fill("input[name='j_password']", PASSWORD)
    page.click("button:has-text('Log in')")

    # Wait until login redirect completes
    page.wait_for_url("**/home", timeout=10000)

    save_cookies(context)
    browser.close()
