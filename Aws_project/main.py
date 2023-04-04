import time
import csv
import os
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
nltk.download('vader_lexicon')
import re
def scrape_reviews(product_url,count):
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
    
    # Scroll down to load all reviews
    while True:
        try:
            see_all_reviews = driver.find_element(By.XPATH,"//li[@class='a-last']/a")
            see_all_reviews.click()
            time.sleep(random.uniform(2.5, 4.9))
            # Scrape reviews
            review_elems1 = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-hook='review']")))
            reviews1 = [elem.text for elem in review_elems1]
            
            reviews.extend(reviews1)
            #Limists the number of reviews
            if len(reviews) >= count:
                break
        except NoSuchElementException:
            print('Nothing more to load')
            break
    print(len(reviews))   

    # Close browser
    driver.quit()

    return reviews


def analyze_sentiments(reviews):
    # Initialize sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Preprocess reviews
    reviews = [review.lower().replace('\n', ' ').replace('\r', '') for review in reviews]
    reviews = [' '.join(re.findall(r'\w+', review)) for review in reviews]

    # Analyze sentiments
    sentiments = []
    for review in reviews:
        sentiment = sid.polarity_scores(review)
        sentiment['review'] = review  # Add review to sentiment dictionary
        sentiments.append(sentiment)

    # Convert sentiments to DataFrame
    df_sentiments = pd.DataFrame(sentiments)

    # Reorder columns
    cols = ['review', 'neg', 'neu', 'pos', 'compound']
    df_sentiments = df_sentiments[cols]

    return df_sentiments


def analyze_sentiments(reviews, output_file):
    # Initialize sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Preprocess reviews
    reviews = [review.lower().replace('\n', ' ').replace('\r', '') for review in reviews]
    reviews = [' '.join(re.findall(r'\w+', review)) for review in reviews]

    # Analyze sentiments
    sentiments = []
    for review in reviews:
        sentiment = sid.polarity_scores(review)
        sentiment['review'] = review  # Add review to sentiment dictionary
        sentiments.append(sentiment)

    # Convert sentiments to DataFrame
    df_sentiments = pd.DataFrame(sentiments)

    # Reorder columns
    cols = ['review', 'neg', 'neu', 'pos', 'compound']
    df_sentiments = df_sentiments[cols]

    # Create plot
    plt.plot(df_sentiments.index, df_sentiments['compound'])
    plt.xlabel('Review Number')
    plt.ylabel('Sentiment Score')
    plt.title('Sentiment Analysis')
    plt.savefig(output_file.replace('.csv', '.png'))

    return df_sentiments

def main():
    # Scrape reviews
    count =int(input("Enter the number of reviews you want to scrape: "))
    product_url = input("Enter the product url: ")
    reviews = scrape_reviews(product_url,count)

    # Perform sentiment analysis
    output_file = "amazon_reviews_sentiments.csv"
    df_sentiments = analyze_sentiments(reviews, output_file)

    # Save results to CSV file
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

