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
    INSPECT_BUTTON = (By.CLASS_NAME, "market_actionmenu_button")
    BUY_BUTTON_END = (By.CLASS_NAME, "item_market_action_button")
    LOGIN_FORM = (By.CLASS_NAME, "newlogindialog_TextInput_2eKVn")
    LOGIN_BUTTON = (By.CLASS_NAME, "newlogindialog_SubmitButton_2QgFE")
    PAGE_NUMBER = (By.CLASS_NAME, "market_paging_pagelink active")
    LAST_PAGE = (By.CLASS_NAME, "market_paging_pagelink")

    """CSS SELECTOR"""
    POPUP = (By.CSS_SELECTOR, "#market_action_popup_itemactions > a")
