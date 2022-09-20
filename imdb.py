from selenium import webdriver
from selenium.webdriver.common.by import By

from personal_config import UserName, Password
from time import sleep
from models import Movie, Genre
from queue import Queue
from config import *

q = Queue()


class PureLink:
    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance == None:
            cls.instance = super().__new__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        self.driver = webdriver.Chrome()
        if protocols['link_crawler']:
            self.LinkCrawler()
        if protocols['data_crawler']:
            self.Getdata()
            while True:
                continue
            self.driver.close()


    @property
    def title(self):
        try:
            title_tag = self.driver.find_element(By.XPATH, title_xpth).text
            return title_tag
        except:
            return None

    @property
    def rate(self):
        try:
            rate_tag = self.driver.find_element(By.XPATH, rate_xpth).text
            return rate_tag
        except:
            return None

    @property
    def awards(self):
        try:
            awards_tag = self.driver.find_element(By.XPATH, awards_xpth).text
            return awards_tag
        except:
            return None

    @property
    def year(self):
        try:
            year_tag = self.driver.find_element(By.XPATH, year_xpth1).text
            if len(year_tag) < 5:
                return year_tag
        except:
            year_tag = self.driver.find_element(By.XPATH, year_xpth2).text
            return year_tag
    @property
    def platform(self):
        platform_tag = self.driver.find_element(By.XPATH, platform_xpth).text
        if len(platform_tag) > 4:
            return platform_tag
        else:
            return 'Cinema'



    @property
    def summary(self):
        try:
            body_tag = self.driver.find_element(By.XPATH, body_xpth).text
            return body_tag
        except:
            return None

    @property
    def genre(self):
        try:
            genre_tag = self.driver.find_element(By.CLASS_NAME, genre_Cls).text
            return genre_tag
        except:
            return None

    def LinkCrawler(self):
        driver = self.driver
        if protocols['connection_type'] == 'dynamic':
            driver.get(Base_link)
            sleep(3)
            user = driver.find_element(By.XPATH, '//*[@id="ap_email"]')
            user.clear()
            user.send_keys(UserName)
            sleep(3)
            password = driver.find_element(By.XPATH, '//*[@id="ap_password"]')
            password.clear()
            password.send_keys(Password)
            signin = driver.find_element(By.XPATH, '//*[@id="signInSubmit"]')
            sleep(3)
            signin.click()
            sleep(3)
            for a in driver.find_elements(By.CLASS_NAME, 'ipc-focusable'):
                href = a.get_attribute('href')
                if href is not None and href.startswith('https://www.imdb.com/title'):
                    self.save(href)
            driver.implicitly_wait(50)
            protocols['LinkCrawler'] = False
            driver.close()

    def Getdata(self):
        driver = self.driver
        file = open('storage/links.json', 'r')
        for lnk in file:
            q.put(lnk)
        while True:
            URL = q.get()
            driver.get(URL)
            genre = Genre.create(name=self.genre)
            movie = Movie.create(url=URL,
                                 title=self.title,
                                 rate=self.rate,
                                 awards=self.awards,
                                 year=self.year,
                                 platform=self.platform,
                                 summary=self.summary,
                                 genre=genre.name,
                                 is_completed=True)
            print(f'{movie} is extracted out of imdb')
            q.task_done()
            if q.empty():
                driver.close()
    q.join()


    def save(self, data):
        with open('storage/links.json', 'a') as file:
            file.writelines(f'{data}\n')
            file.close()
        print('saved')
