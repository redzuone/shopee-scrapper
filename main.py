from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.environ.get('openai_api_key')
import PySimpleGUI as sg
from bs4 import BeautifulSoup

# soup = BeautifulSoup(html, "html.parser")

s = Service("chromedriver.exe")
driver = webdriver.Chrome(service = s)
driver.get('https://shopee.com.my/autobotic/867583382')

WebDriverWait(driver, 6)
print('Click')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button"""))).click()
driver.execute_script("window.scrollTo(0, 2080)")

"""

"""
result_text = "Result:\n"

# sleep(4)
print('find')
for i in range(1, 4):
    review_xpath = """//*[@id="main"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[1]/div["""+str(i)+"""]/div/div[@class = 'shopee-product-rating__content']"""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, review_xpath)))
    # print(review_xpath)
    review_obj = driver.find_element(By.XPATH, review_xpath)
    print(review_obj.text)
    review_text = [review_obj.text]

    response = openai.Completion.create(
        engine="curie",
        prompt="This is a Sentence sentiment classifier\n\n\
        Sentence: \"I loved the new Batman movie!\"\
        \nSentiment: Positive\n\
        ###\n\
        Sentence: \"I hate it when my phone battery dies.\"\n\
        Sentiment: Negative\n\
        ###\n\
        Sentence: \"This is the link to the article\"\n\
        Sentiment: Neutral\n\
        ###\n\
        Sentence: \""+review_obj.text+"\"\n\
        Sentiment:",
        temperature=0,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###", "\n"]
    )
    print('Sentiment:'+response.choices[0].text)
    result_text = f"{result_text} Review {i}\n {review_obj.text}\n Sentiment: {response.choices[0].text}\n"
print(result_text)

layout = [[sg.Text(result_text)]], [sg.Button("Ok")]
window = sg.Window("Shopee Scrapper", layout, layout,size=(720, 252))
while True:
    event, values = window.read()
    if event == "Ok" or event == sg.WIN_CLOSED:
        break
window.close()

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
