from selenium.webdriver.common.by import By

class PageLocators(object):
    """ID"""
    CHECK_BOX = (By.ID, "market_buynow_dialog_accept_ssa")
    BUY_BUTTON = (By.ID, "market_buynow_dialog_purchase")
    CLOSE_BUTTON = (By.ID, "market_buynow_dialog_close")
    USER_BALANCE = (By.ID, "header_wallet_balance")

    """XPATH"""
    NEXT_PAGE = (By.XPATH, '//span[@id="searchResults_btn_next" and @class="pagebtn"]')
    PRICES_BOX = (By.XPATH, '//span[@class="market_listing_price market_listing_price_with_fee"]')

    """CLASS NAME"""
    MARKET_LISTING_ROW = (By.CLASS_NAME, "market_recent_listing_row")
    BUY_BUTTON_END = (By.CLASS_NAME, "item_market_action_button")
    PAGE_NUMBER = (By.CLASS_NAME, "market_paging_pagelink active")
    LAST_PAGE = (By.CLASS_NAME, "market_paging_pagelink")
    ITEM_NAME = (By.CLASS_NAME, "market_listing_item_name")

    """CSS SELECTOR"""
    BODY = (By.CSS_SELECTOR, "body")
    A = (By.CSS_SELECTOR, "a")
    DIV = (By.CSS_SELECTOR, "div")
    CSGOFLOAT_UTILITY_BELT = (By.CSS_SELECTOR, "csgofloat-utility-belt")
    CSGOFLOAT_SORT_FLOATS = (By.CSS_SELECTOR, "csgofloat-sort-floats")
    CSGOFLOAT_STEAM_BUTTON = (By.CSS_SELECTOR, "csgofloat-steam-button")
    CSGOFLOAT_ITEM_ROW_WRAPPER = (By.CSS_SELECTOR, "csgofloat-item-row-wrapper")
