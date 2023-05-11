from selenium.webdriver.common.by import By


class PageLocators(object):
    """ID"""
    SEARCH_RESULTS = (By.ID, "searchResults_end")
    CHECK_BOX = (By.ID, "market_buynow_dialog_accept_ssa")
    BUY_BUTTON = (By.ID, "market_buynow_dialog_purchase")
    CLOSE_BUTTON = (By.ID, "market_buynow_dialog_close")
    USER_BALANCE = (By.ID, "header_wallet_balance")

    """XPATH"""
    NEXT_PAGE = (By.XPATH, '//span[@id="searchResults_btn_next" and @class="pagebtn"]')
    LISTING_PRICE = (By.XPATH, '//span[@class="market_listing_price market_listing_price_with_fee"]')

    """CLASS NAME"""
    BUY_BUTTON_END = (By.CLASS_NAME, "item_market_action_button")
    PAGE = (By.CLASS_NAME, "market_paging_pagelink")
    ACTIVE_PAGE = (By.CLASS_NAME, "market_paging_pagelink active")
    LISTING_NAME = (By.CLASS_NAME, "market_listing_item_name")

    """CSS SELECTOR"""
    LOGOUT_BUTTON = (By.CSS_SELECTOR, 'a[href="javascript:Logout();"]')
    BODY = (By.CSS_SELECTOR, "body")
    A = (By.CSS_SELECTOR, "a")
    DIV = (By.CSS_SELECTOR, "div")
    MARKET_LISTING_ROW = (By.CSS_SELECTOR, "#searchResultsRows > .market_listing_row")
    CSGOFLOAT_UTILITY_BELT = (By.CSS_SELECTOR, "csgofloat-utility-belt")
    CSGOFLOAT_SORT_FLOATS = (By.CSS_SELECTOR, "csgofloat-sort-floats")
    CSGOFLOAT_STEAM_BUTTON = (By.CSS_SELECTOR, "csgofloat-steam-button")
    CSGOFLOAT_ITEM_ROW_WRAPPER = (By.CSS_SELECTOR, "csgofloat-item-row-wrapper")
