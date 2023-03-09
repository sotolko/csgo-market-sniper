from functions import *
from config import load_config

# Login page load
cls()
driver.get("https://steamcommunity.com/login/home/?goto=market%2Flistings%2F730")

#Load config
url_info = load_config()
if url_info == None:
    driver.quit()
    sys.exit()
    
count = 0

input("Press enter to start if you are logged in and ready!")

# Search loop
cls()
print("\n\n")
while True:
    if len(url_info) < 1:
        print("Populate config.yaml file and rerun. Exiting...")
        driver.quit()
        sys.exit()

    if count == len(url_info):
        count = 0

    driver.get(url_info[count][5])
    check_whole_page(count, url_info)
    count += 1
