from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def getRatios(symbol):
    opt = Options()
    opt.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=opt)
    driver.get('https://www.screener.in/login/?')
    email = driver.find_element(By.NAME, 'username')
    email.send_keys('shiblibaig01@gmail.com')
    password = driver.find_element(By.NAME, 'password')
    password.send_keys('shibliscreen')
    password.send_keys(Keys.ENTER)
    time.sleep(1)
    ratioList = None

    if type(symbol) == str:

        driver.get(f'https://www.screener.in/company/{symbol}/consolidated/')
        # Locate the table by its unique identifier (adjust the selector as needed)
        time.sleep(2)
        ratioListElements = driver.find_elements(By.CLASS_NAME, 'company-ratios')
        ratioList = []
        for i in ratioListElements:
            ratioList.append(i.text)

    else:

        for symbols in symbol:
            driver.get(f'https://www.screener.in/company/{symbols}/consolidated/')
            # Locate the table by its unique identifier (adjust the selector as needed)
            time.sleep(2)
            ratioListElements = driver.find_elements(By.CLASS_NAME, 'company-ratios')
            ratioList = {}
            for i in ratioListElements:
                ratioList[symbols] = i.text

    time.sleep(1)
    driver.quit()

    return ratioList


def balanceSheets(symbol):
    opt = Options()
    opt.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=opt)
    driver.get(f'https://www.screener.in/company/{symbol}/consolidated/')

    # Locate the table by its unique identifier (adjust the selector as needed)
    table = driver.find_elements(By.TAG_NAME, 'tbody')

    for i in table:
        rows = i.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                ie = row.find_element(By.CLASS_NAME, "button-plain")
                ie.click()
                print("CLICKED!!")
            except:
                pass

    for i in table:
        rows = i.find_elements(By.TAG_NAME, 'tr')

        table_data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            row_data = [col.text for col in cols]
            table_data.append(row_data)

        # Print the extracted table data
        for row in table_data:
            print(row)

    time.sleep(2)

    driver.quit()


def get_pro_con_analysis():
    pass


def quart_analysis():
    pass


def annual_analysis():
    pass


getRatios('INFY')
