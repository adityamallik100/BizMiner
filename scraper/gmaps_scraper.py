import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_google_maps(category, location):
    query = f"{category} in {location}"
    print(f"🚗 Opening Google Maps for: {query}")

    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 25)  # Increased wait time

    driver.get("https://www.google.com/maps")
    time.sleep(3)

    # Search box
    try:
        print("🔍 Waiting for search box...")
        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)
    except Exception as e:
        print("❌ Search box error:", e)
        driver.quit()
        return []

    # Wait for listing container
    print("🔄 Looking for listings container...")
    try:
        listings_container = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='feed']"))
        )
        print("✅ Listings container found!")
    except Exception as e:
        print("❌ Listings not found:", e)
        driver.quit()
        return []

    # Scroll to load more cards
    print("🔃 Scrolling listings pane...")
    for _ in range(4):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", listings_container)
        time.sleep(2)

    cards = listings_container.find_elements(By.XPATH, ".//a[contains(@href, '/place')]")
    print(f"🔍 Found {len(cards)} listings\n")

    results = []

    for i, card in enumerate(cards[:10]):  # Only first 10 results
        try:
            print(f"🖱 Clicking business card {i+1}...")
            ActionChains(driver).move_to_element(card).click().perform()
            time.sleep(5)

            business = {
                "business_name": "",
                "address": "",
                "phone": "",
                "website": "",
                "category": category,
                "source": "Google Maps",
                "email": ""
            }

            # Name
            try:
                business["business_name"] = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf.lfPIob"))
                ).text.strip()
            except:
                print("⚠️ Business name not found.")

            # Address
            try:
                addr_el = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Address')]")
                business["address"] = addr_el.text.strip()
            except:
                pass

            # Phone
            try:
                tel_link = driver.find_element(By.XPATH, "//a[starts-with(@href, 'tel:')]")
                business["phone"] = tel_link.get_attribute("href").replace("tel:", "").strip()
            except:
                try:
                    phone_btn = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Phone number')]")
                    business["phone"] = phone_btn.text.strip()
                except:
                    pass

            # Website
            try:
                website_btn = driver.find_element(By.XPATH, "//a[contains(@aria-label, 'Website')]")
                business["website"] = website_btn.get_attribute("href").strip()
            except:
                pass

            # Email scraping (from website)
            if business["website"]:
                email = scrape_email_from_website(business["website"])
                business["email"] = email

            results.append(business)
            print(f"✅ Collected: {business['business_name']}")

        except Exception as e:
            print(f"❌ Error scraping card {i+1}:", e)
            continue

    driver.quit()
    print(f"\n📁 Scraping complete. Total businesses: {len(results)}")
    return results

def scrape_email_from_website(website_url):
    import requests
    import re

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(website_url, timeout=10, headers=headers)
        if resp.status_code == 200:
            # Find emails in page source
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", resp.text)
            if emails:
                return emails[0]  # Return first email found
    except:
        pass
    return ""

# If you want to test directly
if __name__ == "__main__":
    data = scrape_google_maps("salon", "kolkata")
    with open("data/google_maps_leads.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
