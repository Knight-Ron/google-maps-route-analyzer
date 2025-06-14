# Google Maps Route Analyzer

A Python automation tool that uses Selenium WebDriver to simulate user interactions with Google Maps, extract directions between two cities, and export route details in both CSV and JSON formats.

---

## Features

- Automates route search between any two cities
- Extracts route names, durations, and distances
- Supports multiple available route options
- Saves results into structured `.csv` and `.json` formats
- Modular and beginner-friendly codebase
- Easily extendable with new features (CLI, UI, batch processing)

---

## Use Case

This project is ideal for:
- Demonstrating Selenium automation skills
- Learning web scraping and browser automation
- Building a portfolio project for data engineering or map-related roles
- Automating dynamic data collection for city-to-city routes

---

## Technologies Used

- Python 3.x
- Selenium WebDriver
- ChromeDriver (via `webdriver-manager`)
- Web scraping and DOM parsing
- CSV and JSON for structured data export

---

## How to Run

### Step 1: Clone the Repository

    ```bash
        git clone https://github.com/Knight-Ron/google-maps-route-analyzer.git
        cd google-maps-route-analyzer

### Step 2: Install Dependencies
    ```bash
    pip install selenium webdriver-manager

### Step 3: Run the Script
    ```bash
    python main.py

The script will:
- Open Google Maps
- Search for directions 
- Extract route information 
- Save the results

---

## To Do / Future Improvements

- Add support for dynamic user input (command-line or GUI)
- Support batch processing of multiple city pairs
- Integrate Google Maps API for more stable data access
- Add web interface using Flask
- Implement logging and performance metrics

---

## License
This project is licensed under the MIT License.

---

## Author
Ronald Jacob
GitHub: Knight-Ron
LinkedIn: linkedin.com/in/ronaldjacob
