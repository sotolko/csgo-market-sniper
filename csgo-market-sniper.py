import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


#Driver options (CHROME ONLY!)
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

urls = []

#Login page load
driver.get("https://steamcommunity.com/login/home/?goto=market%2Flistings%2F730")
print("Login into STEAM first!")

#Request time set
speed = float(input("How much wait time in seconds after each search (enter for default) : ") or "2")

#Reading URLs
with open('skins.txt', 'r') as findvalues:
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

count2 = 0

#Search loop
while True:
    if count2 == len(urls):
        count2 = 0
    print("Reading URL...")
    driver.get(urls[count2])

    while True:
        btns = driver.find_elements("class name","market_actionmenu_button")
        buyButtons = driver.find_elements("class name","item_market_action_button")

        for idx,btn in enumerate(btns):
            try:  
                driver.execute_script("arguments[0].click();", btn)
                popup = driver.find_element("css selector","#market_action_popup_itemactions > a")
                href = popup.get_attribute('href')
            except:
                continue

            response = requests.get('https://api.csgofloat.com/?url='+href)
            response.raise_for_status()
            jsonResponse = response.json()

            print("Reading info about item " +jsonResponse["iteminfo"]["full_item_name"])
            jsonResponseFloat = float(jsonResponse["iteminfo"]["floatvalue"])
            jsonResponsePattern = int(jsonResponse["iteminfo"]["paintseed"])

            if jsonResponseFloat < float(urlinfo[count2][0]):
                print("Found skin with float better than "+str(urlinfo[count2][0]))
                print("Checking pattern now...")
                if int(urlinfo[count2][1]) == -1 or jsonResponsePattern == int(urlinfo[count2][1]):
                    print("Found skin with pattern "+str(urlinfo[count2][1]))
                else:
                    print("Your pattern dont match any skin with your float...")
                    continue
            else:
                print("Your float dont match skin float...")
                continue

            #Buy now
            driver.execute_script("arguments[0].click();", buyButtons[idx])

            #Close if not enough money
            try:
                checkBox = driver.find_element("id","market_buynow_dialog_accept_ssa")
                driver.execute_script("arguments[0].click();", checkBox)

                buyButton = driver.find_element("id","market_buynow_dialog_purchase")
                driver.execute_script("arguments[0].click();", buyButton)

                closeButton = driver.find_element("id","market_buynow_dialog_close")
                driver.execute_script("arguments[0].click();", closeButton)
            except:
                cancelButton = driver.find_element("id","market_buynow_dialog_cancel")
                driver.execute_script("arguments[0].click();", cancelButton)
                print("Not enough funds!")
                continue
            
            #Print information about found skin
            print("Name: " +jsonResponse["iteminfo"]["full_item_name"])
            print("Wear: " +jsonResponse["iteminfo"]["wear_name"])
            print("FloatNumber: " +str(jsonResponse["iteminfo"]["floatvalue"]))
            print("Pattern: " +str(jsonResponse["iteminfo"]["paintseed"]))
            print("\n")
            time.sleep(speed)

        try:
            print("Checking next page...")
            nextPage = driver.find_element('xpath','//span[@id="searchResults_btn_next" and @class="pagebtn"]')
            driver.execute_script("arguments[0].click();", nextPage)
            time.sleep(speed)
        except:
            print("No next page, going to next URL...")
            count2 += 1
            break


#End session
driver.quit()