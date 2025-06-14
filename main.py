from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.com/maps")
time.sleep(3)

# Step 1: Search for location
def search_place():
    search_box = driver.find_element(By.CSS_SELECTOR, ".searchboxinput")
    search_box.clear()
    search_box.send_keys("Paris")
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

# Step 2: Click on Directions button
def direction():
    time.sleep(3)
    direction_btn = driver.find_element(By.XPATH, '//button[@data-value="Directions"]')
    direction_btn.click()
    time.sleep(5)

# Step 3: Enter destination point
def search_point():
    time.sleep(3)
    # Get both input fields
    input_fields = driver.find_elements(By.CSS_SELECTOR, 'input.tactile-searchbox-input')
    if len(input_fields) >= 2:
        # First input = FROM, Second input = TO
        from_box = input_fields[0]
        to_box = input_fields[1]

        # Optional: Clear and retype location in FROM
        from_box.clear()
        from_box.send_keys("Paris")
        time.sleep(1)

        # Now type destination point in destination (TO)
        to_box.clear()
        to_box.send_keys("London")
        to_box.send_keys(Keys.ENTER)
        time.sleep(5)
    else:
        print("Error: Input boxes not found.")

# Step 4: print directions
def print_info():
    time.sleep(5)
    try:
        routes = driver.find_elements(By.CSS_SELECTOR, ".section-directions-trip-title span")
        for r in routes:
            print("Route:", r.text)
    except Exception as e:
        print("Failed to print route info:", str(e))

import csv
import json

# New: Save route info to a file
def save_route_info():
    try:
        routes = driver.find_elements(By.CSS_SELECTOR, ".section-directions-trip")
        route_data = []
        for r in routes:
            title = r.find_element(By.CLASS_NAME, "section-directions-trip-title").text
            duration = r.find_element(By.CLASS_NAME, "section-directions-trip-duration").text
            distance = r.find_element(By.CLASS_NAME, "section-directions-trip-distance").text

            route_data.append({
                "route": title,
                "duration": duration,
                "distance": distance
            })

        # Save to JSON
        with open("data/routes.json", "w") as jf:
            json.dump(route_data, jf, indent=4)

        # Save to CSV
        with open("data/routes.csv", "w", newline='') as cf:
            writer = csv.DictWriter(cf, fieldnames=["route", "duration", "distance"])
            writer.writeheader()
            writer.writerows(route_data)

        print("Routes saved to data/routes.json and data/routes.csv")

    except Exception as e:
        print("Saving failed:", e)

# Run steps
search_place()
direction()
search_point()
print_info()
save_route_info()


# driver.quit()
