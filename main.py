from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import json
import random

# Random wait to mimic user behavior
def wait_random(min_sec=3, max_sec=6):
    time.sleep(random.uniform(min_sec, max_sec))

# Test different origin-destination pairs
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

results = []

# Set up Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # run in full screen
# options.add_argument("--headless")       # headless can cause issues with Google Maps

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Loop through each pair and test directions
for origin, destination in city_pairs:
    print(f"\nChecking route: {origin} -> {destination}")
    entry = {"from": origin, "to": destination, "status": ""}

    try:
        driver.get("https://www.google.com/maps")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".searchboxinput")))
        wait_random()

        # Enter the origin
        search_input = driver.find_element(By.CSS_SELECTOR, ".searchboxinput")
        search_input.clear()
        search_input.send_keys(origin)
        search_input.send_keys(Keys.ENTER)
        wait_random()

        # Click the Directions button
        directions_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-value="Directions"]'))
        )
        directions_btn.click()
        wait_random()

        # Fill both input boxes (origin and destination)
        inputs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input.tactile-searchbox-input'))
        )

        if len(inputs) >= 2:
            inputs[0].clear()
            inputs[0].send_keys(origin)
            wait_random(1, 2)

            inputs[1].clear()
            inputs[1].send_keys(destination)
            inputs[1].send_keys(Keys.ENTER)
            wait_random(8, 12)

            # Check if any routes were found
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".section-directions-trip-title span"))
                )
                print("✓ Route found")
                entry["status"] = "Route found"
            except:
                print("× No route found")
                entry["status"] = "No route found"
        else:
            print("× Couldn't find input fields")
            entry["status"] = "Missing input boxes"

    except Exception as e:
        print(f"× Error while processing: {e}")
        entry["status"] = f"Error: {str(e)}"

    results.append(entry)
    wait_random(2, 4)

driver.quit()

# Save to CSV
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["from", "to", "status"])
    writer.writeheader()
    writer.writerows(results)

# Save to JSON
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

print("\nAll done. Results saved to results.csv and results.json.")
