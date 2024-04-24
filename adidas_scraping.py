import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
# from lxml import html
from selenium.webdriver.common.keys import Keys
import requests
# from scrapingant_client import ScrapingAntClient
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time


def tshirts(page):
    url = f'https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops&type=t_shirts&condition=6&page={page}'
    print(f"Fetching URL: {url}")
    r = requests.get(url)
    print(f"HTTP Status Code: {r.status_code}")
    
    # Handle HTTP status codes
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    elif r.status_code == 429:
        print("Rate-limited. Exponential backoff...")
        for i in range(1, 4):
            wait_time = 2 ** i  # Exponential backoff (2, 4, 8 seconds)
            print(f"Sleeping for {wait_time} seconds...")
            time.sleep(wait_time)
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                return soup
        print("Exhausted retries due to rate limiting.")
        return None
    else:
        print(f"Failed to fetch the URL: {url}")
        return None


def extract(soup, num_pages):
    
    all_href_values = []

    for page in range(1, num_pages + 1):
        # Fetch the page content
        print(f"Fetching page {page}")
        url = f"https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops&type=t_shirts&condition=6&page={page}"
        r = requests.get(url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            divs = soup.find_all('div', class_='articleDisplayCard-children')
            
            if not divs:
                print("No items found on the page with the specified class.")
                continue
            
            # Iterate over each div found
            for item in divs:
                a_element = item.find('a', class_='image_link')
                
                if a_element:
                    href_value = a_element.get('href')
                    print(f"Found href: {href_value}")
                    all_href_values.append(href_value)
                    
        else:
            print(f"Failed to fetch page {page}")

    return all_href_values

def extract_size_chart(url):
    # url = f"https://shop.adidas.jp{all_href_value}"
    service = Service('/usr/bin/chromedriver')  # Update path to chromedriver
    driver = webdriver.Chrome(service=service)
    driver.get(url)
        # Scroll to the bottom of the page
    # driver.execute_script("window.scrollBy(0, 15);")

    # # Wait for a moment to see the result (you might need to adjust the duration based on your needs)
    # time.sleep(2)
    elm = driver.find_element(By.TAG_NAME, "html")
    elm.send_keys(Keys.END)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    time.sleep(3)
    elm.send_keys(Keys.END)
    time.sleep(3)
    driver.implicitly_wait(2)
    
    try:
        coordinated_pro = driver.find_element(By.XPATH, "(//div[@class='coordinate_item_tile test-coordinate_item_tile'])[1]")
    except:
        coordinated_pro = ''
    
    actions = ActionChains(driver)
    actions.move_to_element(coordinated_pro).perform()

    # Click the element
    coordinated_pro.click()
    time.sleep(1)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    try:
        # Create a list to store the extracted data
        data = []
        breadcrumb_items = soup.find_all('li', class_='breadcrumbListItem')
        text_values_string = ""
        for item in breadcrumb_items:
            a_element = item.find('a')
            if a_element:
                text_value = a_element.get_text(strip=True)
                if text_value:
                    text_values_string += text_value + ","
        text_values_string = text_values_string.rstrip(",")

        # Extract title
        try:
            title = soup.find('h1', class_='itemTitle test-itemTitle').text
        except:
            title = ''
        
        product_images = soup.select_one('img', class_='test-img image test-image')
        product_image = product_images.attrs['src']
        print(product_image)
        try:
            specialfunction = soup.find('a', class_='tecTextTitle').text.strip()
        except:
            specialfunction = ''
        try:
            specialfunctiondescription = soup.find('div', class_='item_part details').text.strip()
        except:
            specialfunctiondescription = ''

        coordinated_products = []
        coordinated_product_image_url = soup.select_one('img', class_='coordinate_image_body test-img')
        coordinated_product_image_url_value = coordinated_product_image_url.attrs['src']
        print(coordinated_product_image_url_value)
        coordinated_products.append(coordinated_product_image_url_value)
        coordinated_product_elements = soup.find_all('div', class_='coordinate_item_container test-coordinate_item_container add-open')

        # Iterate over each coordinated product element
        for coordinated_product in coordinated_product_elements:
            # Extract coordinated product information
            coordinated_product_name = coordinated_product.find('span', class_='title').text.strip() 
            coordinated_products.append(coordinated_product_name)
            coordinated_product_pricing = coordinated_product.find('span', class_='price-value test-price-salePrice-value').text.strip()
            coordinated_products.append(coordinated_product_pricing)

            
            coordinated_product_page_url = coordinated_product.find('a', class_='detailLink')
            print("coordinated_product_page_url", coordinated_product_page_url)
            if coordinated_product_page_url:
                coordinated_product_page_url_value = coordinated_product_page_url['href']
                coordinated_products.append(coordinated_product_page_url_value)
        print(coordinated_products)
        
        SenseofFittingitsrating = soup.find('div', class_='BVRRRatingRadioImage')
        if SenseofFittingitsrating:
            img_tag = SenseofFittingitsrating.find('img')
            if img_tag:
                alt_value = img_tag.get('alt')
                title_value = img_tag.get('title')
                SenseofFittingitsrating_output = f"{alt_value} {title_value}"
            else:
                SenseofFittingitsrating_output = "N/A"
        else:
            SenseofFittingitsrating_output = "N/A"

        
        rating_comment_date =  soup.find('span', class_='BVRRValue BVRRReviewDate').text.strip()
        print('rating_comment_date',rating_comment_date)    
        rating_comment =  soup.find('span', class_='BVRRValue BVRRReviewTitle').text.strip()
        print('BVRRNumber BVRRBuyAgainTotal',rating_comment)
        rating_comment_description =  soup.find('span', class_='BVRRReviewText').text.strip()
        print('rating_comment_description BVRRBuyAgainTotal',rating_comment)    
        Recommended_rate = soup.find('span', class_='BVRRNumber').text.strip()
        print('Recommended_rate',Recommended_rate)
        rating = soup.find('span', class_='BVRRNumber BVRRRatingNumber').text.strip()
        print('rating',rating)
        reviews = soup.find('span', class_='BVRRNumber BVRRBuyAgainRecommend').text.strip()
        print(reviews)
        
        # Extract category name
        group_name_element = soup.find('a', class_='groupName')
        gender_name = group_name_element.find('span', class_='genderName').get_text(strip=True)
        category_name = group_name_element.find('span', class_='categoryName').get_text(strip=True)
        category_name_output = f"{gender_name} {category_name}"
        
        # Extract sizes
        size_list_element = soup.find('ul', class_='sizeSelectorList')
        sizes = []
        if size_list_element:
            size_elements = size_list_element.find_all('li', class_='sizeSelectorListItem')
            sizes = [size.find('button', class_='sizeSelectorListItemButton').text.strip() for size in size_elements]
        
        # Extract span values
        size_fit_bar_div = soup.find('div', class_='sizeFitBar')
        span_values = []
        if size_fit_bar_div:
            label_div = size_fit_bar_div.find('div', class_='label')
            if label_div:
                span_elements = label_div.find_all('span')
                span_values = [span.text for span in span_elements]
        
        # Extract product description
        Productdescription = soup.find('div', class_='inner')
        titleOfdescription = Productdescription.find('h2', class_='heading itemName test-commentItem-topHeading').text.strip()
        GeneralDescriptionoftheproduct = Productdescription.find('h4', class_='heading itemFeature test-commentItem-subheading').text.strip()
        
        # Extract size chart
        size_chart = soup.find('div', class_='sizeChart')
        table_data = []
        headers = []
        if size_chart:
            rows = size_chart.find_all('tr', class_='sizeChartTRow')
            th_elements = size_chart.select('thead.sizeChartTHeader th')
            headers = [th.text.strip() for th in th_elements if th.text.strip()]
            for row in rows:
                cells = row.find_all(['td', 'th'], class_='sizeChartTCell')
                row_data = [cell.text.strip() for cell in cells]
                if all(cell.name == 'th' for cell in cells):
                    headers.extend(row_data)
                else:
                    table_data.append(row_data)
        table_data.insert(0, headers)

        print(table_data)

        # Append extracted data to the list
        data.append({
            "breadcrumb(Category)": text_values_string,
            "Product Name": title,
            "Product Image": product_image,
            "Category Name": category_name_output,
            "Sizes": ", ".join(sizes),
            "Coordinated product":coordinated_products,
            "Sense of the size": span_values,
            "titleOfdescription": titleOfdescription,
            "GeneralDescriptionoftheproduct": GeneralDescriptionoftheproduct,
            "Size Information": table_data,
            "Special Function": specialfunction,
            "Special Function Description": specialfunctiondescription,
            "SenseofFittingitsrating":SenseofFittingitsrating_output,
            "Rating comment date": rating_comment_date,
            "Rating":rating,
            "Reviews":reviews,
            "Recommended rate":Recommended_rate,
            "Rating comment_title": rating_comment,
            "Rating comment_description": rating_comment_description
        })
        
        # Write the data to a CSV file
        with open('Output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow(entry)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

def main():
    soup = tshirts(1)
    num_pages = 22  # Specify the number of pages you want to scrape
    href_values = extract(soup, num_pages)
    for href_value in href_values:
        url = f"https://shop.adidas.jp{href_value}"
        time.sleep(5)
        print(f"Fetching URL: {url}")
    
        try:
            extract_size_chart(url)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()