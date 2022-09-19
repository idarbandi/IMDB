from selenium import webdriver
from selenium.webdriver.common.by import By


from personal_config import UserName, Password
from time import sleep
from config import *
from models import Movie, Genre
from queue import Queue

q = Queue()


class PureLink:
    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance == None:
            cls.instance = super().__new__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        self.con = webdriver.Chrome()

    def get(self):
        driver = self.con
        if protocols['LinkCrawler']:
            driver.get(
                'https://www.imdb.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com'
                '%2Fregistration%2Fap-signin-handler%2Fimdb_us&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0'
                '%2Fidentifier_select&openid.assoc_handle=imdb_us&openid.mode=checkid_setup&siteState'
                '=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl91cyIsInJlZGlyZWN0VG8iOiJodHRwczovL3d3dy5pbWRiLmNvbS8_cmVmXz1s'
                'b2dpbiJ9&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http'
                '%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&tag=imdbtag_reg-20')
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
        if protocols['DataCrawler']:
            file = open('storage/links.json', 'r')
            for lnk in file:
                q.put(lnk)
            while True:
                URL = q.get()
                driver.get(URL)
                driver.implicitly_wait(50)
                genre = Genre.create(name=driver.find_element(By.CLASS_NAME, genre_Cls).text)
                movie = Movie.create(url=URL,
                              title=driver.find_element(By.XPATH, title_xpth).text,
                              rate=driver.find_element(By.XPATH, rate_xpth).text,
                              awards=driver.find_element(By.XPATH, awards_xpth).text,
                              year=driver.find_element(By.XPATH, year1_xpth).text,
                              platform=driver.find_element(By.XPATH, platform_xpth).text,
                              summary=driver.find_element(By.XPATH, body_xpth).text,
                              genre=genre)
                q.task_done()
                print(movie)
        q.join()
        driver.close()

    def save(self, data):
        with open('storage/links.json', 'a') as file:
            file.writelines(f'{data}\n')
            file.close()
        print('saved')
