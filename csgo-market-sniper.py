import time
import logging
import sys
import requests
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from re import sub
from decimal import Decimal

chromedriver_autoinstaller.install()

#Driver options (CHROME ONLY!)
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

urls = []
priceTextNum = []

def check_user_balance():
    """Function that is checking user balance"""

    print("Checking user balance...")
    userBalance = driver.find_element("id","header_wallet_balance")
    userBalNum = (int(''.join(c for c in userBalance.text if c.isdigit()))/100)
    return userBalNum

def buyLog(itemName,itemFloat,itemPattern,itemPrice):
    """Function that will save informaiton about purchase to logfile"""

    logger = logging.getLogger('BUYLOGGER')
    logger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler("purchaseHistory.log",mode='a')
    fileHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p %Z')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.info("Item name: {} , Float: {} , Pattern: {} , Price: {}".format(itemName,itemFloat,itemPattern,itemPrice))  

#Login page load
driver.get("https://steamcommunity.com/login/home/?goto=market%2Flistings%2F730")
print("Login into STEAM first!")

#Request time set
speed = float(input("How much wait time in seconds after each search (enter for default) : ") or "2")

#Reading URLs
with open('skins.txt', 'r', encoding="utf-8") as findvalues:
    for line in findvalues:
        line = line.rstrip()
        if line.startswith('https://steamcommunity.com/market/listings/730/'):
          urls.append(line)
        else:
          continue

#Make default array for url information
urlinfo = [[0 for x in range(3)] for y in range(len(urls))]

#User input for each url
for x in range(len(urls)):
    urlinfo[x][0] = float(input("Input float for skin number "+str(x+1)+ " (enter for any): ") or "1")
    urlinfo[x][1] = float(input("Input pattern for skin number "+str(x+1)+ " (enter for any): ") or "-1")
    print("\n")

count = 0

#Search loop
while True:
    if count == len(urls):
        count = 0
    print("Reading URL...")
    driver.get(urls[count])
    
    while True:
        btns = driver.find_elements("class name","market_actionmenu_button")
        buyButtons = driver.find_elements("class name","item_market_action_button")
        prices = driver.find_elements('xpath','//span[@class="market_listing_price market_listing_price_with_fee"]')
        for price in prices:
            priceTextNum.append(int(''.join(c for c in price.text if c.isdigit()))/100)

        for idx,btn in enumerate(btns):
            #Check item float and save JSON
            try:  
                driver.execute_script("arguments[0].click();", btn)
                popup = driver.find_element("css selector","#market_action_popup_itemactions > a")
                href = popup.get_attribute('href')

                response = requests.get('https://api.csgofloat.com/?url='+href)
                response.raise_for_status()
                jsonResponse = response.json()
            except:
                continue

            #Check user balance
            try:
                userBalNum = check_user_balance()
            except:
                print("Cant get user balance. Are you logged in?")
                driver.quit()
                sys.exit()

            #Check if user have enough money for skin
            if userBalNum < priceTextNum[idx]:
                print("You dont have enough money for this skin, checking next...")
                continue
            else:
                print("Enough funds, continue...")

            #Check if float and pattern match with user input
            jsonResponseName = str(jsonResponse["iteminfo"]["full_item_name"])
            jsonResponseFloat = float(jsonResponse["iteminfo"]["floatvalue"])
            jsonResponsePattern = int(jsonResponse["iteminfo"]["paintseed"])
            print("Reading info about item " +jsonResponseName)

            if jsonResponseFloat < float(urlinfo[count][0]):
                print("Found skin with float better than "+str(urlinfo[count][0]))
                print("Checking pattern now...")
                if int(urlinfo[count][1]) == -1 or jsonResponsePattern == int(urlinfo[count][1]):
                    print("Found skin with pattern "+str(urlinfo[count][1]))
                else:
                    print("Your pattern dont match any skin with your float...")
                    continue
            else:
                print("Your float dont match skin float...")
                continue

            #Buy now button
            driver.execute_script("arguments[0].click();", buyButtons[idx])

            #Execute order
            try:
                checkBox = driver.find_element("id","market_buynow_dialog_accept_ssa")
                driver.execute_script("arguments[0].click();", checkBox)

                buyButton = driver.find_element("id","market_buynow_dialog_purchase")
                driver.execute_script("arguments[0].click();", buyButton)

                closeButton = driver.find_element("id","market_buynow_dialog_close")
                driver.execute_script("arguments[0].click();", closeButton)

                print("Buying item for "+ str(priceTextNum[idx]))

                userBalNum = check_user_balance()
                print("Current wallet balance is "+ str(userBalNum))
            except:
                print("Something went wrong, skipping to next skin!")
                continue

            #Save information to file
            buyLog(jsonResponseName,jsonResponseFloat,jsonResponsePattern,priceTextNum[idx])
            time.sleep(speed)

        #Clear information about previous page
        priceTextNum.clear()

        #Search for next page
        try:
            print("Checking next page...")
            nextPage = driver.find_element('xpath','//span[@id="searchResults_btn_next" and @class="pagebtn"]')
            driver.execute_script("arguments[0].click();", nextPage)
            time.sleep(speed)
        except:
            print("No next page, going to next URL...")
            count += 1
            break
