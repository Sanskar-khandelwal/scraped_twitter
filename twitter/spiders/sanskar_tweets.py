import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from shutil import which
from scrapy.selector import Selector
from selenium.webdriver.support.ui import WebDriverWait
import time
import scrapy
import pandas as pd



class SanskarTweetsSpider(scrapy.Spider):
    name = "sanskar_tweets"
    allowed_domains = ["twitter.com"]
    start_urls = ["https://twitter.com/login"]
    username = "useyourtweeterusername"
    password = "useryourtweeterpassword"
    subject = "iamsrk"

    def __init__(self):
       
        chrome_options = Options()
        # Set user agent string if needed
        user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36"
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_path = which("chromedriver")
        driver = webdriver.Chrome(
            executable_path=chrome_path, chrome_options=chrome_options)
        driver.get("https://twitter.com/login")
        # wait = WebDriverWait(driver, 10)
        time.sleep(10)
        username = driver.find_element(By.XPATH, "//input[@name = 'text']")
        username.send_keys(self.username)
        nextButton = driver.find_element(By.XPATH, "//span[text()='Next']")
        nextButton.click()
        time.sleep(5)

        password = driver.find_element(By.XPATH, "//input[@type = 'password']")
        password.send_keys(self.password)

        loginButton = driver.find_element(By.XPATH, "//span[text()='Log in']")
        loginButton.click()
        time.sleep(10)

        # Searching the subject

        searchBar = driver.find_element(By.XPATH, "//div[@dir = 'ltr']/input")
        searchBar.send_keys(self.subject)
        searchBar.send_keys(Keys.ENTER)
        time.sleep(5) 
        People = driver.find_element(By.XPATH, "(//div[@dir= 'ltr']/span[text() = 'People'])[1]")   
        People.click()
        time.sleep(10)

        profile = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div/section/div/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div[1]/a/div/div[1]/span/span[1]")
        profile.click()

        time.sleep(15)

        user_tags = []
        tweets = []
        replies = []
        retweets = []
        likes = []

   
        articles = driver.find_elements(By.XPATH, "//article[@data-testid = 'tweet']")
        print(len(articles))     
        
        while True:
            for article in articles: 
                user_tag = article.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
                user_tags.append(user_tag)
                tweet = article.find_element(By.XPATH, ".//div[@data-testid= 'tweetText']").text
                tweets.append(tweet)

                reply = article.find_element(By.XPATH, ".//div[@data-testid= 'reply']").text
                replies.append(reply)

                retweet = article.find_element(By.XPATH, ".//div[@data-testid= 'retweet']").text
                retweets.append(retweet)

                like = article.find_element(By.XPATH, ".//div[@data-testid= 'like']").text
                likes.append(like)
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            articles = driver.find_elements(By.XPATH, "//article[@data-testid = 'tweet']")
            length_tweets = len(list(set(tweets)))
            
            if length_tweets > 50:
                break
    
        df = pd.DataFrame(zip(user_tags, tweets, replies, likes, retweets), columns = ['usertags', 'tweets', 'replies', 'likes', 'retweets'])
        df.to_excel(r"C:\Users\test\OneDrive\Documents\swaptweets.xlsx", index = False)
        self.html = driver.page_source

        

        driver.close()
        

    def parse(self, response):
        resp =  Selector(text = self.html)
        print(resp)
