from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
import pandas as pd

driver = webdriver.Chrome()
driver.maximize_window()

all_product_url = []

all_data = []

for all_pages in range(1,51):
    driver.get(f"https://books.toscrape.com/catalogue/category/books_1/page-{all_pages}.html")
    
    url_elements = driver.find_elements(By.XPATH, "//h3/a")
    
    for single_url in url_elements:
        all_url = single_url.get_attribute("href")
        all_product_url.append(all_url)
        
for urls in all_product_url:
    driver.get(urls)
    
    try:
        name = driver.find_element(By.XPATH, "//h1").text
    except:
        name = ""
        
    try:
        price = driver.find_element(By.XPATH, "(//div[@class='col-sm-6 product_main']/p)[1]").text.strip()
        price = price.replace("£","$")
    except:
        price = ""
        
    try:
        stock = driver.find_element(By.XPATH, "(//div[@class='col-sm-6 product_main']/p)[2]").text
        stock = re.sub(r"\D", "", stock)
    except:
        stock = ""
        
    try:
        review = driver.find_element(By.XPATH, "(//div[@class='col-sm-6 product_main']/p)[3]").get_attribute("class")
        review = review.replace("star-rating", "")
    except:
        review = ""
        
    try:
        description = driver.find_element(By.XPATH, "//article[@class='product_page']/p").text
    except:
        description = ""
        
    product_list = {
        "name": name,
        "price": price,
        "stock": stock,
        "review": review,
        "description": description,
    }
    
    all_data.append(product_list)
    print(f"Scrape Done {len(all_data)}")
    
    # if(len(all_data)==5): break

df = pd.DataFrame(all_data)
df.to_excel("alldata_toscrape.xlsx", index=False)

#Driver close
driver.quit()