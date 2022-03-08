from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from time import sleep
import data


s = Service(r"C:\Program Files (x86)\chromedriver.exe")
url="https://www.amazon.de/"
session = HTMLSession()
class AmazonInformation:


    def __init__(self,) -> None:
        self.driver = webdriver.Chrome(service=s)
        self.driver.get(url)
        sleep(2)

    def cookies_accept(self):
        self.driver.find_element(By.XPATH, '//input[@id="sp-cc-accept"]').click()
        sleep(2)
        sign_in_Click = self.driver.find_element(By.XPATH, '//span[@id="nav-link-accountList-nav-line-1"]')
        sign_in_Click.click()
        sleep(2)

    def loggin(self, username, password):
        self.driver.find_element(By.NAME, "email").send_keys(username)
        self.driver.find_element(By.XPATH, '//input[@id="continue"]').click()
        sleep(2)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@id="signInSubmit"]').click()
        sleep(2)

    def search(self, search_value):
        search_lable=self.driver.find_element(By.NAME, "field-keywords")
        search_lable.click()
        search_input = self.driver.find_element(By.NAME, "field-keywords")
        search_input.send_keys(search_value)
        sleep(2)
        search_input.send_keys(Keys.ENTER)

    def get_data(self):
        _url = self.driver.current_url
        request = session.get(_url)
        request.html.render(sleep=1)
        soup = BeautifulSoup(request.html.html, 'html.parser')
        return soup

    def get_deals(self, soup):
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        counter=0
        for item in products:
            title = item.find('span', {'class': 'a-size-base-plus a-color-base'}).text.strip()
            link = item.find('a', {'class': 'a-link-normal s-no-outline'})['href']
            try:
                price = item.find('span', {'class': 'a-price-whole'}).text.strip()
            except:
                continue

            try:
                reviews = item.find('span',{'class':'a-size-base s-underline-text'}).text.strip()
            except:
                reviews = 0
            image = item.find('img', {'class': 's-image'})['src']
            response = session.get(image)
            with open('image' + str(counter) + '.png', 'wb') as w:
                w.write(response.content)

            counter += 1
            print('{} - Title: {}, Price: {}, Reviews: {},Link: {}'.format(counter,title,price,reviews,'https://www.amazon.de/-/en' + link))
    def get_pages(self):
        pages = self.driver.find_element(By.XPATH,'//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').click()

        if  pages == self.driver.find_element(By.XPATH,'//a[@class="s-pagination-item s-pagination-next s-pagination-disabled "]').click():
            return
        else:
            return pages


getinformation = AmazonInformation()
getinformation.cookies_accept()
getinformation.loggin('sample@sample.com', data.password)
getinformation.search("schuhe")
getinformation.get_deals(getinformation.get_data())


