from selenium import webdriver
from time import sleep
from datetime import datetime
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

LOGIN_PAGE = "https://x.com/i/flow/login"
pac_file_url = "https://proxymesh.com/pac/open_us-tx.pac" # Proxy PAC file URL

class TwitterScrapper:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'--proxy-pac-url={pac_file_url}') # set proxy
        # self.options.add_argument("--headless") # to run without a gui
        self.options.add_argument("start-maximized") # open Browser in maximized mode
        self.options.add_argument("--disable-blink-features") # disables all Blink (rendering engine) features in the browser
        self.options.add_argument("--disable-blink-features=AutomationControlled") # disables the AutomationControlled feature in Blink (often used to detect and block automated bots)

        self.service = Service()

        self.driver = self.new_driver()
        self.driver.maximize_window()

        self.LOGIN_URL = LOGIN_PAGE
        self.my_ip = self.driver.execute_script("return fetch('https://api.ipify.org').then(r => r.text())")
        print(f"My IP: {self.my_ip}")
        self.trending_topics = []

    def new_driver(self):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        return driver

    def login(self, driver):
        driver.get(self.LOGIN_URL)

        print("Title: " + driver.title)

        driver.implicitly_wait(10)

        username_input = driver.find_element(by = By.XPATH, value ='//input[@autocomplete="username"]')
        username_input.send_keys(self.username)
        

        next_button = driver.find_element(by = By.XPATH, value = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
        next_button.click()

        driver.implicitly_wait(10)

        password_input = driver.find_element(by = By.XPATH, value = '//input[@autocomplete="current-password"]')
        password_input.send_keys(self.password)

        login_button = driver.find_element(by = By.XPATH, value = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button')
        login_button.click()
    
    def get_driver(self):
        return self.driver
    
    def scrape_trending(self, driver):
        driver.implicitly_wait(10)

        what_is_happening = driver.find_element(by = By.XPATH, value = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/div/section/div/div')

        for i in range(3, 8):
            trending_topic = what_is_happening.find_element(by = By.XPATH, value = f'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/div/section/div/div/div[{i}]/div/div/div/div[2]').text
            self.trending_topics.append(trending_topic)

    def store_trending_topics(self):
        from db import get_database
        db = get_database()
        trending_topics = db['trendingX']

        trending_topics.insert_one({
            "trending_topics": self.trending_topics,
            "data": datetime.now().strftime("%d-%m-%Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            'ip': self.my_ip
        })

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    twitterScrapper = TwitterScrapper(
        username=username,
        password=password
    )

    driver = twitterScrapper.get_driver()
    twitterScrapper.login(driver)
    sleep(10)

    twitterScrapper.scrape_trending(driver)
    sleep(10)

    twitterScrapper.store_trending_topics()

    twitterScrapper.close()
