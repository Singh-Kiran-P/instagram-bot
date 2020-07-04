from selenium import webdriver
from time import sleep
from secrets import *
import sqlite3

IG_LINK = "https://www.instagram.com"


class InstaBot:
    def __init__(self):
        # set member variables
        self.driver = webdriver.Chrome()
        self.conn = sqlite3.connect('instagram.db')
        self.user = ""
    # Loggin in to Instagram account
    def login(self, username, pw):
        self.user = username
        self.driver.get(IG_LINK)
        sleep(1)
        login_username = self.driver.find_element_by_xpath(
            '//input[@name=\"username\"]').send_keys(username)
        login_password = self.driver.find_element_by_xpath(
            '//input[@name=\"password\"]').send_keys(pw)
        login_btn = self.driver.find_element_by_xpath(
            '//button[@type="submit"]').click()
        sleep(4)  # waiting for login
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div/div/section/div/button').click()
        sleep(2)
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        sleep(2)

    # Liking pic based on the provided hastag
    def likeAndFollow(self, text, type_, folow):

        # cursor for the SQLite db
        c = self.conn.cursor()

        url = self.generateURL(text, type_)

        driver = self.driver
        driver.get(url)
        sleep(2)

        # scrolling the page to get more items
        for i in range(0, 1):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)

        # search for pic href links
        href = driver.find_elements_by_tag_name('a')
        pic_href = [elem.get_attribute('href') for elem in href]

        final_href = []
        for href in pic_href:

            # check constaints on the links
            temp = '/p/' in href
            if temp == True:
                c.execute(
                    "SELECT * FROM Profiles WHERE liked_href like '{}' and user like ".format(href,self.user))
                if len(c.fetchall()) == 0:
                    final_href.append(href)

        print(text + ' photos: ' + str(len(final_href)))

        # looping over the links and liking each pic
        for pic_href in final_href:
            driver.get(pic_href)
            sleep(1)
            username = driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/div/a').get_attribute("innerHTML")

            # click on the like button
            Liked = driver.find_element_by_class_name(
                '_8-yf5').get_attribute("aria-label")

            # check if pic is already liked if not Like it
            if Liked == "Like":
                # Like
                driver.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button').click()
                c.execute("INSERT INTO Profiles VALUES('{}','{}','{}','{}')".format(str(self.user),
                                                                                    str(username),
                                                                                    str(pic_href),
                                                                                    str(text)))

                if folow == True:
                    # Follow
                    driver.find_element_by_class_name("oW_lN").click()
                    # c.execute("INSERT INTO Following VALUES('{}','{}','{}')".format(
                    # str(username), str(pic_href), str(text)))

                self.conn.commit()

            sleep(2)

        self.conn.close()

    def generateURL(self, text, type_):
        dirver = self.driver
        if type_ == "hashtag":
            return "https://www.instagram.com/explore/tags/{}/".format(text)
        elif type_ == "place":
            dirver.find_element_by_xpath(
                '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys(text)
            sleep(1)
            url = dirver.find_element_by_xpath(
                '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]').get_attribute("href")
            return url


my_bot = InstaBot()
my_bot.login(username2, pw2)
my_bot.likeAndFollow("freelancer", "hashtag", True)
