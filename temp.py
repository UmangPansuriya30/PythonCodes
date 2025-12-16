from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://veritas.art/en/auctions/previous/")

elements = driver.find_elements(By.XPATH, "//span[@class='overlay']/preceding-sibling::a")
links = [ele.get_attribute("href") for ele in elements]

for auctionUrl in links:
    driver.get(auctionUrl)
    time.sleep(3)

    # nav_filters = driver.find_elements(By.XPATH, "//nav[@class='filters']")

    cats = driver.find_elements(By.XPATH, ".//a[@data-cat='68']")

    if len(cats) != 0:
        print(auctionUrl)
        break

driver.quit()
