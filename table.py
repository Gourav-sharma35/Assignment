from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def fetch_wikipedia_data():
    # Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  #Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Open the Wikipedia page
    url = "https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table"
    driver.get(url)
    
    # Locate the 1,000,000+ articles table
    tables = driver.find_elements(By.CLASS_NAME, "wikitable")
    target_table = tables[1]  # Assuming the 1,000,000+ table is the second table
    
    # Extract table data
    rows = target_table.find_elements(By.TAG_NAME, "tr")
    data = []
    for row in rows[1:]:  # Skip header row
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > 0:
            language = cells[1].text
            articles = int(cells[3].text.replace(',', ''))
            data.append([language, articles])
    
    # Close the driver
    driver.quit()
    
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=["Language", "Articles"])
    return df

def findTotalArticlesByLanguages(languages):
    # Fetch data from Wikipedia
    df = fetch_wikipedia_data()
    
    # Filter rows where the Language column matches any in the provided languages list
    filtered_df = df[df['Language'].isin(languages)]
    
    # Calculate the sum of Articles for the filtered languages
    total_articles = filtered_df['Articles'].sum()
    
    return total_articles

# Example usage
languages = ["English", "German"]
total_articles = findTotalArticlesByLanguages(languages)
print("Total articles for selected languages:", total_articles)





