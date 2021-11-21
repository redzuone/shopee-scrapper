from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.environ.get('openai_api_key')
from bs4 import BeautifulSoup

# soup = BeautifulSoup(html, "html.parser")
DRIVER_PATH = "C:\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
#driver = webdriver.Chrome(executable_path=D)
driver.get('https://shopee.com.my/autobotic/867583382')

WebDriverWait(driver, 6)
# sleep(2)
print('Click')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button"""))).click()
driver.execute_script("window.scrollTo(0, 2080)")

sleep(4)
print('find')
#textt = driver.find_element_by_xpath("""//*[@id="main"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[@class = 'shopee-product-rating__content']""")
#print(textt.text)
#//*[@id="main"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[3]

for i in range(1,4):
    review_xpath = """//*[@id="main"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[1]/div["""+str(i)+"""]/div/div[@class = 'shopee-product-rating__content']"""
    # print(review_xpath)
    review_obj = driver.find_element(By.XPATH, review_xpath)
    print(review_obj.text)
    review_text = [review_obj.text]
    response = openai.Completion.create(
        engine="curie",
        prompt="This is a Sentence sentiment classifier\n\nSentence: \"I loved the new Batman movie!\"\nSentiment: Positive\n###\nSentence: \"I hate it when my phone battery dies.\"\nSentiment: Negative\n###\nSentence: \"This is the link to the article\"\nSentiment: Neutral\n###\nSentence: \""+review_obj.text+"\"\nSentiment:",
        temperature=0,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###", "\n"]
    )
    print('Sentiment:'+response.choices[0].text)
sleep(1)
next_buttton = driver.find_element(By.XPATH, """//*[@id="main"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[2]/button[@class = 'shopee-button-solid shopee-button-solid--primary ']/following-sibling::button""")

if next_buttton == '':
    print('no more reviews')
else:
    print('next page!')
    next_buttton.click()

# price
## //*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[1]/div/div[2]/div[1]
# disc //*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[1]/div/div[2]/div[2]
# image use get_attribute('class') //*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[5]/div/div[1]/div[2]/div/div[2]
# .value_of_css_property("background-image"), re.split('[()]', text)
sleep(30)
