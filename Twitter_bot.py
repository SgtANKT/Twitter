from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import tweepy as tp
import pandas as pd
import bs4

tweets_list = []


class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome(executable_path="C:\\CD\\chromedriver_win32\\chromedriver.exe")

    def login(self):
        bot = self.bot
        self.url = bot.get('https://twitter.com')
        time.sleep(4)
        email = bot.find_element_by_name("session[username_or_email]")
        password = bot.find_element_by_name("session[password]")
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        time.sleep(3)

    def liketweet(self, hashtag):
        bot = self.bot
        # try:
        #     Pulling individual tweets from query
            # for tweet in tp.api.search(q=hashtag, count=count):
            #     Adding to list that contains all tweets
                # tweets_list.append((tweet.created_at, tweet.id, tweet.text))
        # except BaseException as e:
        #     print('failed on_status,', str(e))
        #     time.sleep(3)
        bot.get('https://twitter.com/search?q=' + hashtag + '&src=typed_query')
        time.sleep(3)

        for i in range(1,5):
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(5)
            tweet = bot.find_elements_by_class_name("css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
            tweets_list.append(tweet.text)
            print(tweet.text)
            tweets = bot.find_element_by_class_name("r-4qtqp9 r-yyyyoo r-1xvli5t r-dnmrzs r-bnwqim r-1plcrui r-lrvibr r-1hdv0qi")
            links = [elem.get_attribute('data-permalink-path') for elem in tweets]
            for link in links:
                bot.get('https://twitter.com' + link)
                try:
                    bot.find_elements_by_xpath("/html/body/div/div/div/div/main/div/div/div/div/div/div[2]/div/section/div/div/div/div[1]/div/article/div/div[7]/div[3]/div/div/div/svg")
                    time.sleep(10)
                except Exception as ex:
                    time.sleep(60)
    def get_tweets(self, hashtag):
        self.bot.get('https://twitter.com/search?q=' + hashtag + '&src=typed_query')
        time.sleep(3)

        body = self.bot.find_element_by_tag_name('body')

        # for _ in range(10):
        #         body.send_keys(Keys.PAGE_DOWN)
        #         time.sleep(0.3)

        try:
            tweet_divs = self.bot.page_source
            obj = bs4.BeautifulSoup(tweet_divs, "html.parser")
            content = obj.find_all("div", class_="content")
            print(content)

            print("content printed")
            print(len(content))
            for c in content:
                tweets = c.find("p", class_="tweet-text").strings
                tweet_text = "".join(tweets)
                print(tweet_text)
                print("-----------")
                try:
                    name = (c.find_all("strong", class_="fullname")[0].string).strip()
                except AttributeError:
                    name = "Anonymous"
                date = (c.find_all("span", class_="_timestamp")[0].string).strip()

                datestring = str(c.find_all("span", class_="_timestamp")[0])
                print(datestring)
                datestring = datestring[datestring.index("data-time") + 11:]
                datestring = datestring[:datestring.index("\"")]
                print(datestring)
                # print(tweet_text)
                try:
                    write_csv(datestring, tweet_text, name)
                except:
                    print('csv error')

        except Exception as e:
            print("Something went wrong!")
            print(e)
            driver.quit()
        # timeline = self.bot.find_element_by_id('timeline')
        # tweet_nodes = timeline.find_elements_by_css_selector('.tweet-text')
        # print(tweet_nodes)
        # df = pd.DataFrame({'tweets': [tweet_node.text for tweet_node in tweet_nodes]})
        # print(df)

ed = TwitterBot('ankitpratihast4545@gmail.com', 'Ankit@1997')
ed.login()
ed.get_tweets('COVID19')



