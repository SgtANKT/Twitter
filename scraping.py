# from bs4 import BeautifulSoup
import time
import pandas as pd
from csv import DictWriter
# import pprint
# from selenium.webdriver.common.keys import Keys
# import datetime
# from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException


class Twitter:
    def __init__(self, driver_type, start_date, end_date, words, lang, max_time):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options, executable_path=driver_type)
        self.start_date = start_date
        self.end_date = end_date
        self.words = words
        self.lang = lang
        self.max_time = max_time

    # def drivers(self):
    #     if self.driver == 1:
    #         driver = webdriver.Firefox(executable_path="C:\\Drivers\\FD\\geckodriver.exe")
    #     elif self.driver == 2:
    #         options = Options()
    #         options.headless = True
    #         driver = webdriver.Chrome(options=options ,executable_path="C:\\Drivers\\CD\\chromedriver.exe")
    #     elif self.driver == 3:
    #         driver = webdriver.Ie(executable_path="C:\\Drivers\\IED\\IEDriverServer.exe")
    #     elif self.driver == 4:
    #         driver = webdriver.Opera(executable_path="C:\\Drivers\\OD\\operadriver.exe")
    #     return driver

    def scroll_find_tweets(self):
        wrd = self.words
        drv = self.driver
        stdt = self.start_date
        endt = self.end_date
        lan = self.lang
        max_time = self.max_time
        languages = {1: 'en', 2: 'it', 3: 'es', 4: 'fr', 5: 'de', 6: 'ru', 7: 'zh'}
        url = "https://twitter.com/search?q="
        words_to_search = wrd.split(',')
        for w in words_to_search:
            w = w.strip()
        for w in words_to_search[:-1]:
            url += "{}%20OR".format(w)
        url += "{}%20".format(words_to_search[-1])
        url += "since%3A{}%20until%3A{}&".format(stdt, endt)
        if lan != 0:
            url += "l={}&".format(languages[lan])
        url += "src=typd"
        print(url)
        drv.get(url)
        start_time = time.time()
        # Goes onto the url and starts scrolling
        # Could've used send_keys(keys.Page_Down) but it gives an error
        while (time.time() - start_time) < max_time:
            tweets = []
            # drv.send_keys(Keys.PAGE_DOWN)
            drv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)
            # finds the location of our tweet and saves it
            for i in range(1):
                names = drv.find_elements_by_css_selector("#react-root > div > div > "
                                                          "div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div "
                                                          "> div > div > div > div > div:nth-child(2) > div > div > "
                                                          "section > div > div > div:nth-child({}) > div > div > "
                                                          "article > div > div > div > div.css-1dbjc4n.r-18u37iz > "
                                                          "div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > "
                                                          "div:nth-child(1) > div > div > "
                                                          "div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2 > "
                                                          "div.css-1dbjc4n.r-1wbh5a2.r-dnmrzs > a > div > "
                                                          "div.css-1dbjc4n.r-18u37iz.r-1wbh5a2.r-1f6r7vd > div > "
                                                          "span".format(i))
                articles = drv.find_elements_by_css_selector("#react-root > div > div > "
                                                             "div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > "
                                                             "div > div > div > div > div > div:nth-child(2) > div > "
                                                             "div > section > div > div > div:nth-child({}) > div > "
                                                             "div > article > div > div > div > "
                                                             "div.css-1dbjc4n.r-18u37iz > "
                                                             "div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o "
                                                             "> div:nth-child(2) > div:nth-child(1) > div".format(i))
                
                for tw, nm in zip(articles, names):
                    dict = {"name":nm.text, "tweets":tw.text}
                    print("============================================================================\n",dict,"\n============================================================================")
                    tweets.append(dict)
                    # print("============================================================================\n",tw.text,"\n============================================================================")
                # df.to_csv("twitterData.csv", encoding="utf-8-sig", index=False)
                # print("Running")
            print(str(time.time() - start_time) + " < " + str(max_time))
            df = pd.DataFrame(tweets)
            
            # print(df)
            df.to_csv("twitterData.csv", encoding="utf-8-sig", index=False)
    # def write_csv_header(self):
    #     sc = self.scroll_find_tweets()
    #     with open("twitterData.csv", "w+") as csv_file:
    #         fieldnames = ['Tweets']
    #         writer = DictWriter(csv_file, fieldnames=fieldnames)
    #         writer.writeheader()

    # def write_csv(self, date, tweet, name):
    #     with open("twitterData.csv", "a+") as csv_file:
    #         fieldnames = ['Date', 'Name', 'Tweets', 'Tags']
    #         writer = DictWriter(csv_file, fieldnames=fieldnames)
    #         # writer.writeheader()
    #         writer.writerow({'Date': date, 'Name': name, 'Tweets': tweet})
    #
    # def make_csv(self, data):
    #     l = len(data['date'])
    #     print("count: %d" % l)
    #     with open("twitterData.csv", "a+") as file:
    #         fieldnames = ['Date', 'Name', 'Tweets']
    #         writer = DictWriter(file, fieldnames=fieldnames)
    #         writer.writeheader()
    #         for i in range(l):
    #             writer.writerow({'Date': data['date'][i],
    #                              'Name': data['name'][i],
    #                              'Tweets': data['tweet'][i],
    #                              })
    #
    # def get_all_dates(self, start_date, end_date):
    #     dates = []
    #     start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    #     end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    #     step = timedelta(days=1)
    #     while start_date <= end_date:
    #         dates.append(str(start_date.date()))
    #         start_date += step
    #
    #     return dates
    #
    # def main(self):
    #     driver_type = int(
    #         input("1) Firefox | 2) Chrome | 3) IE | 4) Opera | 5) PhantomJS\nEnter the driver you want to use: "))
    #     wordsToSearch = input("Enter the words: ").split(',')
    #     for w in wordsToSearch:
    #         w = w.strip()
    #     start_date = input("Enter the start date in (YYYY-MM-DD): ")
    #     end_date = input("Enter the end date in (YYYY-MM-DD): ")
    #
    #     lang = int(input(
    #         "0) All Languages 1) English | 2) Italian | 3) Spanish | 4) French | 5) German | 6) Russian | 7) Chinese\nEnter the language you want to use: "))
    #     all_dates = self.get_all_dates(start_date, end_date)
    #     print(all_dates)
    #     self.write_csv_header()
    #     driver = "C:\\Drivers\\CD\\chromedriver.exe"
    #     for i in range(len(all_dates) - 1):
    #         # driver = self.init_driver(driver_type)
    #         self.scroll(driver, str(all_dates[i]), str(all_dates[i + 1]), wordsToSearch, lang)
    #         # self.scrape_tweets(driver)
    #         time.sleep(5)
    #         print("The tweets for {} are ready!".format(all_dates[i]))
    #         # driver.quit()


if __name__ == "__main__":
    ed = Twitter("C:\\Drivers\\CD\\chromedriver.exe", "2020-07-20", "2020-07-29", "Football", 1, 20)
    ed.scroll_find_tweets()