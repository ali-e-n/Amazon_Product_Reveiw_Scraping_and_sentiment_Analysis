import time
import csv
import os
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
nltk.download('vader_lexicon')

def scrape_reviews(product_url):
    # Open Chrome browser
    opts = Options()
    driver = webdriver.Chrome('chromedriver')

    # Load Amazon product page
    driver.get(product_url)
    time.sleep(random.uniform(2.5, 4.9))

    # Click on "See all reviews" button
    see_all_reviews = driver.find_element(By.XPATH,"//a[@data-hook='see-all-reviews-link-foot']")
    see_all_reviews.click()
    time.sleep(random.uniform(2.5, 4.9))

    # Scrape reviews
    reviews = []
    review_elems = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-hook='review']")))
    reviews = [elem.text for elem in review_elems]
    print(len(reviews))
    # # Scroll down to load all reviews
    
    while True:
        try:
            see_all_reviews = driver.find_element(By.XPATH,"//li[@class='a-last']/a")
            see_all_reviews.click()
            time.sleep(random.uniform(2.5, 4.9))
            # Scrape reviews
            reviews1=[]
            review_elems1 = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-hook='review']")))
            reviews1 = [elem.text for elem in review_elems1]
            
            reviews.extend(reviews1)
            print(reviews)
    
        except NoSuchElementException:
            print('Nothing more to load')
            continue
    print(len(reviews))   

    # Close browser
    driver.quit()

    return reviews

def analyze_sentiments(reviews):
    # Initialize sentiment analyzer
    sid = SentimentIntensityAnalyzer()
    
    # Analyze sentiments
    sentiments = []
    for review in reviews:
        sentiment = sid.polarity_scores(review)
        sentiments.append(sentiment)
    
    # Convert sentiments to DataFrame
    df_sentiments = pd.DataFrame(sentiments)
    
    return df_sentiments

def main():
    # Scrape reviews
    product_url = "https://www.amazon.com/Samsung-Galaxy-Factory-Unlocked-Smartphone/dp/B08FYTSXGQ"
    reviews = scrape_reviews(product_url)

    # Perform sentiment analysis
    df_sentiments = analyze_sentiments(reviews)

    # Save results to CSV file
    output_file = "amazon_reviews_sentiments.csv"
    df_sentiments.to_csv(output_file, index=False)

    # Print absolute path of output file
    abs_path = os.path.abspath(output_file)
    print(f"Sentiment analysis results saved to: {abs_path}")

    # Check if file was created
    if os.path.exists(output_file):
        print("CSV file created successfully!")
    else:
        print("Failed to create CSV file.")

if __name__ == "__main__":
    main()
