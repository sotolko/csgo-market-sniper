from functions import *


# Login page load
cls()
driver.get("https://steamcommunity.com/login/home/?goto=market%2Flistings%2F730")

# Make default array for url information
urls = OpenUrls("skins.txt")
url_info = [[0 for x in range(5)] for y in range(urls.counter)]
count = 0

take_user_input(url_info, urls.counter)

# Search loop
cls()
print("\n\n")
while True:
    if urls.counter < 1:
        print("Populate skins.txt file and rerun. Exiting...")
        driver.quit()
        sys.exit()

    if count == urls.counter:
        count = 0
    driver.get(urls.urls[count])
    check_whole_page(count, url_info)
    count += 1
