# chatgpt generated, tweaked by Kenji Her

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def url_scraper():
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Base URL for tournament listings
    base_url = "https://play.usaultimate.org/events/tournament/"
    driver.get(base_url)
    time.sleep(3)  # Wait for the page to load

    tournament_links = set()
    cutoff_date = datetime(2021, 9, 1)  # September 1, 2021

    # Loop through pages
    while True:
        # Parse page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        stop_scraping = False  # Flag to stop looping
        
        # Find all tournament rows
        for row in soup.find_all("tr", class_=["row", "alternate", "alt"]):
            # Extract tournament link
            link_tag = row.find("a", href=True)
            if not link_tag or "/events/" not in link_tag["href"]:
                continue  # Skip if no valid link

            tournament_url = "https://play.usaultimate.org" + link_tag["href"] + '/schedule/Men/CollegeMen/'
            
            # Extract competition groups (e.g., "College - Men", "High School - Boys")
            competition_groups = row.find("ul", class_="bulletless")
            if not competition_groups or "College - Men" not in competition_groups.get_text():
                continue  # Skip tournaments that are not "College - Men"

            # Extract tournament date
            date_tag = row.find_all("td")[-1]  # Last <td> contains date
            if date_tag:
                raw_date = date_tag.get_text(strip=True)
                
                # Convert text date to datetime object
                try:
                    # Handle date ranges (e.g., "Mar 08, 2025 - Mar 09, 2025")
                    date_str = raw_date.split(" - ")[-1]  # Use the latest date
                    tournament_date = datetime.strptime(date_str, "%b %d, %Y")

                    # Stop if tournament date is before Fall 2021
                    if tournament_date < cutoff_date:
                        print(f"Stopping at tournament: {tournament_url} (Date: {tournament_date.strftime('%b %d, %Y')})")
                        stop_scraping = True
                        break  # Exit loop
                    else:
                        tournament_links.add(tournament_url)

                except ValueError:
                    continue  # Skip if date format is unexpected

        # Stop scraping if an old tournament is found
        if stop_scraping:
            break

        # Find the "Next 20" button (pagination)
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next 20 »")
            next_button.click()
            time.sleep(3)  # Allow time for the next page to load
        except:
            print("No more pages to load.")
            break  # Exit loop if no "Next 20" button

    # Close Selenium browser
    driver.quit()

    export_urls(list(tournament_links))

def export_urls(tournament_links):
    csv_filename = "urls.csv"

    # Writing to CSV
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL"])  # Column header
        for url in tournament_links:
            writer.writerow([url])