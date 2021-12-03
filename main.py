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

def get_openai_response(review_obj):
    response = openai.Completion.create(
        engine="curie",
        prompt='This is a Sentence sentiment classifier\n\n\
            Sentence: "I loved the new Batman movie!"\
            \nSentiment: Positive\n\
            ###\n\
            Sentence: "I hate it when my phone battery dies."\n\
            Sentiment: Negative\n\
            ###\n\
            Sentence: "This is the link to the article"\n\
            Sentiment: Neutral\n\
            ###\n\
            Sentence: "' + review_obj.text + '"\n\
            Sentiment:',
        temperature=0,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["###", "\n"]
    )
    return response

def popup(result_text):
    layout = [[sg.Text(result_text)]], [sg.Button("Ok")]
    window = sg.Window("Shopee Scrapper", layout, layout, size=(720, 720))
    while True:
        event, values = window.read()
        if event == "Ok" or event == sg.WIN_CLOSED:
            break
    window.close()

def get_product_price():
    product_price_xpath = "/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div[3]/div/div[3]/div/div"
    product_price = driver.find_element(By.XPATH, product_price_xpath).text
    #print("1 "+product_price)
    return product_price

def get_product_info():
    star_rating_xpath = "/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div[1]"
    total_ratings_xpath = "/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div[2]/div[1]"
    sold_xpath = "/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div[3]/div[1]"

    star_rating = driver.find_element(By.XPATH, star_rating_xpath).text
    total_ratings = driver.find_element(By.XPATH, total_ratings_xpath).text
    sold = driver.find_element(By.XPATH, sold_xpath).text
    return(f" {star_rating}/5, {total_ratings} ratings, {sold} sold")

# soup = BeautifulSoup(html, "html.parser")

s = Service("chromedriver.exe")
driver = webdriver.Chrome(service = s)
driver.get('https://shopee.com.my/autobotic/867583382')

WebDriverWait(driver, 6)
print('Click')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"modal\"]/div[1]/div[1]/div/div[3]/div[1]/button"))).click()
driver.execute_script("window.scrollTo(0, 2080)")

result_text = "Result:\n"
print('start scrapping')

for i in range(1, 4):
    review_xpath = "//*[@id=\"main\"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[1]/div["+str(i)+"]/div/div[@class = 'shopee-product-rating__content']"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, review_xpath)))
    review_obj = driver.find_element(By.XPATH, review_xpath)
    print(review_obj.text)

    response = get_openai_response(review_obj)

    print('Sentiment:'+response.choices[0].text)
    result_text = f"{result_text} Review {i}\n {review_obj.text}\n Sentiment: {response.choices[0].text}\n\n"

result_text += get_product_price()
result_text += get_product_info()
print(result_text)
popup(result_text)

next_buttton = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[2]/button[@class = 'shopee-button-solid shopee-button-solid--primary ']/following-sibling::button")

if next_buttton == '':
    print('no more reviews')
else:
    print('next page!')
    next_buttton.click()


# image use get_attribute('class') //*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[5]/div/div[1]/div[2]/div/div[2]
# .value_of_css_property("background-image"), re.split('[()]', text)
