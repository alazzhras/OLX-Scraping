# OLX Car Scraper

## 📌 Overview
OLX Car Scraper is a Python-based tool that uses Selenium to collect used car listings from the OLX Indonesia website. This tool extracts details such as car name, year, location, price, fuel type, mileage, and transmission.

## 🛠 Features
- **Scraping Data**: Extracts car information from OLX search pages.
- **Load More Automation**: Automatically clicks the “Load More” button to load additional listings.
- **Detail Extraction**: Visits each car listing page to collect fuel type, mileage, and transmission details.
- **Error Handling**: Displays statistics on successfully and unsuccessfully scraped data.
- **CSV Export**: Automatically saves the scraped data in a CSV file.

## 📋 Requirements
Before running the script, ensure you have the following:
- Python 3.x
- Google Chrome
- ChromeDriver (matching your installed Chrome version)
1. **Clone Repository**
   ```bash
   git clone https://github.com/alazzhras/OLX-Scraping.git
   cd OLX-Scraping
   ```
2. **Make Virtual Env (Optional, but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # for macOS/Linux
   venv\Scripts\activate     # for Windows
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 How to Use
1. Run script:
   ```sh
   python scrape.py
   ```

3. Enter the number of “Load More” button clicks as needed.
4. Wait for the scraping process to complete.
5. The data will be saved in a CSV file with the format `OLX-Car_Scraped_YYYY-MM-DD_HH-MM-SS.csv`.

## 🖼 Example Output
```
❓ How many 'Load More' button to click? 5
🔄 Click 1 succeed.
🔄 Click 2 succeed.
...
📊 Total data loaded: 100
✅ 1/100. Success: Toyota Avanza 2018
❌ 2/100. Failed to scrape: Honda Jazz 2019 - Error: NoSuchElementException
...
=== Scraping Summary ===
📊 Total data scraped     : 100
✅ Successfully scraped: 90
❌ Failed to scrape    : 10
✅ Data saved to OLX-Car_Scraped_2025-03-12_15-30-00.csv.
```

## ⚠️ Notes
- **Use responsibly**: Avoid excessive scraping to prevent being blocked by OLX.
- **Ensure ChromeDriver compatibility** with your Google Chrome version.

## 📜 License
This project is licensed under the MIT License. You are free to use, modify, and redistribute this project.

---

✉️ For further inquiries, feel free to contact me at contact@alazzhr.my.id.