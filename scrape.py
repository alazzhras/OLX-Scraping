import random
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Browser configuration 
options = Options()
options.binary_location = "/Applications/Burp Suite Community Edition.app/Contents/Resources/app/burpbrowser/133.0.6943.127/Chromium.app" # Path to browser binary (Optional)
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
options.page_load_strategy = "eager"

def get_driver():
    """Make new WebDriver instance."""
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(15)
    return driver

# WebDriver initialization
main_driver = get_driver()
url = "https://www.olx.co.id/jawa-barat_g2000009/q-Mobil-bekas"
main_driver.get(url)
wait = WebDriverWait(main_driver, 3)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-aut-id="itemBox"]')))

# Load more items
xpath_button = "//button[@data-aut-id='btnLoadMore']"
while True:
    try:
        max_clicks = int(input("❓ How many 'Load More' button to click? "))
        if max_clicks >= 0:
            break
        else:
            print("⚠️ Please input a positive number.")
    except ValueError:
        print("⚠️ Please input a valid number.")

click_count = 0

while click_count < max_clicks:
    try:
        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_button)))
        if load_more_button.is_displayed():
            load_more_button.click()
            time.sleep(random.uniform(1, 2))
            click_count += 1
            print(f"🔄 Click {click_count} succeed.")
        else:
            print("⚠️ Button not visible.")
            break
    except Exception as e:
        print(f"ℹ️ No more 'Load More' button or error occurred: {e}")
        break

# Scrape item list
data = []
itemlist = main_driver.find_elements(By.CSS_SELECTOR, '[data-aut-id="itemBox"]')

# Scrape general info from item list
for item in itemlist:
    try:
        name = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemTitle"]').text
        year = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemDetails"]').text
        location = item.find_element(By.CSS_SELECTOR, '[data-aut-id="item-location"]').text
        price = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemPrice"]').text
        link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        data.append({
            "Car Name": name,
            "Year": year,
            "Fuel": "",
            "Mileage": "",
            "Transmission": "",
            "Location": location,
            "Price": price,
            "Link": link
        })
    except Exception as e:
        print(f"❌ Error scraping list: {e}")
        continue
print(f"📊 Total items loaded: {len(data)}")
main_driver.quit()

# Scrape details info on each item
def scrape_details(item):
    """Scrape details of each item"""
    driver = get_driver()

    try:
        driver.get(item["Link"])
        time.sleep(random.uniform(1, 2))

        item["Fuel"] = driver.find_element(By.CSS_SELECTOR, '[data-aut-id="itemAttribute_fuel"]').text if driver.find_elements(By.CSS_SELECTOR, '[data-aut-id="itemAttribute_fuel"]') else "N/A"
        item["Mileage"] = driver.find_element(By.CSS_SELECTOR, '[data-aut-id="itemAttribute_mileage"]').text if driver.find_elements(By.CSS_SELECTOR, '[data-aut-id="itemAttribute_mileage"]') else "N/A"
        item["Transmission"] = driver.find_element(By.CSS_SELECTOR, '[data-aut-id="itemAttribute_transmission"]').text if driver.find_elements(By.CSS_SELECTOR, '[data-aut-id="itemAttribute_transmission"]') else "N/A"

    except Exception as e:
        item["error"] = f"Failed to scrape {item['Car Name']} - {e}"
    finally:
        driver.quit()
    return item

# Statistic counter
start_time = time.time()
total_data = len(data)
success_count, fail_count = 0, 0

# Multi-threading to scrape details
updated_data = []

with ThreadPoolExecutor(max_workers=5) as executor: # Adjust max_workers to your preference
    future_to_item = {executor.submit(scrape_details, item): item for item in data}
    for idx, future in enumerate(as_completed(future_to_item), start=1):
        result = future.result()
        if "error" in result:
            fail_count += 1
            print(f"❌ {idx}/{total_data}. {result['error']}")
        else:
            success_count += 1
            updated_data.append(result)
            print(f"✅ {idx}/{total_data}. Success: {result['Car Name']}")

# Save data to CSV
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"OLX-Car_Scraped_{timestamp}.csv"
df = pd.DataFrame(updated_data)
df.to_csv(filename, index=False)

# Statistic
end_time = time.time()

print("\n=== Scraping Summary ===")
print(f"📊Total data scraped   : {total_data}")
print(f"✅ Successfully scraped: {success_count}")
print(f"❌ Failed to scrape    : {fail_count}")
print(f"⏳ Total time taken    : {round(end_time - start_time, 2)} seconds")
print(f"✅ Data saved to {filename}.")