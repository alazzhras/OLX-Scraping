import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime


# Browser configuration 
options = Options()
options.binary_location = "/Applications/Burp Suite Community Edition.app/Contents/Resources/app/burpbrowser/133.0.6943.127/Chromium.app" # Path to browser binary (Optional)
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
options.page_load_strategy = "eager"
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)

# URL to scrape 
url = "https://www.olx.co.id/jawa-barat_g2000009/q-Mobil-bekas"
driver.get(url)

# Wait until the page is fully loaded
wait = WebDriverWait(driver, 3)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "li")))

# XPath to the "Load More" button
xpath_button = "//button[@data-aut-id='btnLoadMore']"

# Load more products on page
while True:
    try:
        max_clicks = int(input("❓ How many 'Load More' button to click? "))
        if max_clicks > 0:
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
            time.sleep(random.uniform(1, 3))
            click_count += 1
            print(f"🔄 Click {click_count} succeed.")
        else:
            print("⚠️ Button not visible.")
            break
    except Exception as e:
        print(f"ℹ️ No more 'Load More' button or error occurred: {e}")
        break

# Scrape product list
data = []
itemlist = driver.find_elements(By.CSS_SELECTOR, '[data-aut-id="itemBox"]')

# Scrape data from list
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
print(f"📊 Total data loaded: {len(data)}")

# Data counter
total_data = len(data)
success_count = 0
fail_count = 0

# Scrape detail data on each item
for idx, item in enumerate(data, start=1):
    try:
        driver.get(item["Link"])
        time.sleep(random.uniform(2, 5))
        
        fuel = driver.find_element(By.CSS_SELECTOR, '[data-aut-id="itemAttribute_fuel"]').text
        mileage = driver.find_element(By.CSS_SELECTOR, '[data-aut-id="itemAttribute_mileage"]').text
        transmission = driver.find_element(By.CSS_SELECTOR, '[data-aut-id="itemAttribute_transmission"]').text
        
        item["Fuel"] = fuel if fuel else "N/A"
        item["Mileage"] = mileage if mileage else "N/A"
        item["Transmission"] = transmission if transmission else "N/A"
        
        success_count += 1
        print(f"✅ {idx}/{total_data}. Success: {item['Car Name']}")

    except Exception as e:
        fail_count += 1
        print(f"❌ {idx}/{total_data}. Failed to scrape: {item['Car Name']} - Error: {e}")
        continue

# Statistic
print("\n=== Scraping Summary ===")
print(f"📊Total data scraped     : {total_data}")
print(f"✅ Successfully scraped: {success_count}")
print(f"❌ Failed to scrape    : {fail_count}")

# Save data to CSV
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"OLX-Car_Scraped_{timestamp}.csv"

df = pd.DataFrame(data)
df.to_csv(filename, index=False)
print(f"✅ Data saved to {filename}.")

# Close the browser
driver.quit()