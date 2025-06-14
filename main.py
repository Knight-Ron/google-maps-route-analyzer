from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import json

# Your city list
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

# Setup browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
results = []

# Main loop
for from_city, to_city in city_pairs:
    print(f"Checking route from {from_city} to {to_city}...")
    try:
        driver.get("https://www.google.com/maps/dir/")
        time.sleep(3)

        # Source input
        from_input = driver.find_element(By.XPATH, '//input[@aria-label="Choose starting point, or click on the map..."]')
        from_input.send_keys(from_city)
        from_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Destination input
        to_input = driver.find_element(By.XPATH, '//input[@aria-label="Choose destination, or click on the map..."]')
        to_input.send_keys(to_city)
        to_input.send_keys(Keys.RETURN)
        time.sleep(6)

        # Check if any directions are visible
        steps = driver.find_elements(By.CSS_SELECTOR, '.section-directions-trip-title')
        if steps:
            status = "Route found"
        else:
            status = "No route"

    except Exception as e:
        status = "Error"
        print(f"Error for {from_city} to {to_city}: {e}")

    results.append({
        "from": from_city,
        "to": to_city,
        "status": status
    })

driver.quit()

# Save CSV
with open("routes_result.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["from", "to", "status"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

# Save JSON
with open("routes_result.json", "w", encoding="utf-8") as j:
    json.dump(results, j, indent=2)

print("✅ Done. Data saved in routes_result.csv and routes_result.json.")
