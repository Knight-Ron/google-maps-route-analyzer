from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import json

# City pairs to test
city_pairs = [
    ("Paris", "London"),
    ("New York", "Boston"),
    ("Berlin", "Munich"),
    ("Tokyo", "Kyoto"),
    ("Delhi", "Mumbai"),
    ("San Francisco", "Los Angeles"),
    ("Sydney", "Melbourne"),
    ("Rome", "Venice"),
    ("Toronto", "Montreal"),
    ("Beijing", "Shanghai")
]

# To store results
results = []

# Setup Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Loop through city pairs
for from_city, to_city in city_pairs:
    print(f"\nSearching route from {from_city} to {to_city}...")
    result = {
        "from": from_city,
        "to": to_city,
        "status": ""
    }

    driver.get("https://www.google.com/maps")
    time.sleep(4)

    try:
        search_box = driver.find_element(By.CSS_SELECTOR, ".searchboxinput")
        search_box.clear()
        search_box.send_keys(from_city)
        search_box.send_keys(Keys.ENTER)
        time.sleep(4)

        direction_btn = driver.find_element(By.XPATH, '//button[@data-value="Directions"]')
        direction_btn.click()
        time.sleep(4)

        boxes = driver.find_elements(By.CSS_SELECTOR, 'input.tactile-searchbox-input')
        if len(boxes) >= 2:
            boxes[0].clear()
            boxes[0].send_keys(from_city)
            time.sleep(1)

            boxes[1].clear()
            boxes[1].send_keys(to_city)
            boxes[1].send_keys(Keys.ENTER)
            time.sleep(6)

            routes = driver.find_elements(By.CSS_SELECTOR, ".section-directions-trip-title span")
            if routes:
                print("[✓] Route found.")
                result["status"] = "Route found"
            else:
                print("[X] No route found.")
                result["status"] = "No route found"
        else:
            print("[X] Could not find input boxes.")
            result["status"] = "Input box error"

    except Exception as e:
        print("[X] Error:", e)
        result["status"] = f"Error: {str(e)}"

    results.append(result)

driver.quit()

# Write results to CSV
with open("results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["from", "to", "status"])
    writer.writeheader()
    writer.writerows(results)

# Write results to JSON
with open("results.json", mode="w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print("\n✅ Results saved to results.csv and results.json")
