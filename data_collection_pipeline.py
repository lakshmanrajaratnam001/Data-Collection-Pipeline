import requests
import json
import time 
import os
import uuid
import boto3 
import psycopg2
import s3fs
from sqlalchemy import create_engine
import pandas as pd
import sqlite3 as lite
from unittest.main import main
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


class Scraper:
    '''
    This class is used to scrape data from websites.
    '''  
    def __init__(self):
        self.link_list = []
        self.image_list = []      
        self.dict_properties = {'uuid': [],
            'Friendly id': [],
            'Product name': [], 
            'Price': [],
            'Product amount': [],
            'Product savings amount': [],
            'Product flavour': [],
            'Number of reviews': [],
            }

        self.url = f'https://www.myprotein.com/nutrition/protein.list'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gp')
        options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(self.url)
            
      
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = 'aicorelr.csvkstywya3e.us-east-1.rds.amazonaws.com' # Change it for your AWS endpoint
        USER = 'postgres'
        PASSWORD = 'twinkleandfluffy'
        PORT = 5432
        DATABASE = 'postgres'
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}",  pool_pre_ping=True)
        self.engine.connect()
        
    #clicks on sign in button 
    def sign_in_button(self):
        '''
        This method is used to click on the sign-in pop up that appears when first navigating to the website.
        '''
        time.sleep(10)
        try:
            sign_in = self.driver.find_element(By.CLASS_NAME, 'emailReengagement_close_button')
            sign_in.click()
        except TimeoutException:
          print('No sign in button found')
   
    
    #retrieve product links on first page. 
    def get_product_links(self):
        '''
        This method is used to gather the URL links of all the products on the first page.
        '''
        product_container = self.driver.find_element(By.CLASS_NAME, 'productListProducts_products')
        product_list = product_container.find_elements(By.CLASS_NAME, 'athenaProductBlock')
        
        for product in product_list:
            a_tag = product.find_element(By.CLASS_NAME, 'athenaProductBlock_linkImage')
            link = a_tag.get_attribute('href')
            self.link_list.append(link)
           
              
        
       
    #retrieve product links on second page. 
    def get_all_links(self):  
      '''
      This method is used to navigate and get links of all the products on the second page
      '''
      self.driver.execute_script("window.scrollTo(0, 500)")
      time.sleep(10)
      next_button = self.driver.find_element(By.CLASS_NAME, 'responsivePaginationButton')
      next_button.click()
      time.sleep(5)
      self.get_product_links()
   
    def all_links(self):
      '''
      This method is used to call the methods that retreive the product URL's
      '''
      self.get_product_links()
      self.get_all_links()
      print(self.link_list)

    

    #retreiving images from first page
    def get_images(self):
      '''
      This method is used to obtain each product image URL and download the corrosponding image to a specific folder. 
      '''

      image = self.driver.find_element(By.CLASS_NAME, 'athenaProductImageCarousel_image')
      src = str(image.get_attribute('src'))
      self.image_list.append(src)
      
      for img in self.image_list:
          file_name = img.split('/')[-1]
          r = requests.get(img, stream=True)
          if r.status_code == 200:
             with open(file_name, 'wb') as f:
              for chunk in r:
                  f.write(chunk)
              else:
                pass
           

    def friendly_id(self):
      '''
      This method is used to create a friendly ID for each proudct
      '''
      friendly_id1 =self.driver.find_element(By.CLASS_NAME, 'productAddToWishlist')
      friendly_id2 = friendly_id1.get_attribute('data-product-id')
      self.dict_properties['Friendly id'].append(friendly_id2)
      
          
    def product_properties(self,dir2: str='./raw_data/images/'):
            '''
            This method is used to retrieve specific data for each product. 
            '''
            os.makedirs(dir2, exist_ok=True)
            os.chdir('./raw_data/images')
                
            property_list = self.link_list
            for properties in property_list:
                    url = properties
                    self.driver.get(url)


                    product_item_number = self.driver.find_element(By.CLASS_NAME, 'productAddToWishlist')
                    product_2 = product_item_number.get_attribute('data-product-id')
                    x = product_2
                    cur = self.engine.execute(f'''SELECT * from my_protein_dataset where "Friendly id" = {x} ''')
                    
                     #statment to see if product data has been scraped 
                    if cur:
                        print('product data found in database, product will not be scraped')     
                    #friendly product ID could not befound in database so data for this product will be scraped
                    else:
                        print('product data not found in database, product data will be scraped')
        
                
                        time.sleep(3)
                        self.friendly_id()
                        self.get_images()
                        id = str(uuid.uuid4())
                        self.dict_properties['uuid'].append(id)
                        
                        try:
                            product_name = self.driver.find_element(By.CLASS_NAME, 'productName_title').text
                            self.dict_properties['Product name'].append(product_name)
                        except NoSuchElementException:
                            self.dict_properties['Product name'].append('N/A')
                            
                        try:
                            price = self.driver.find_element(By.CLASS_NAME, 'productPrice_price').text
                            self.dict_properties['Price'].append(price)     
                        except NoSuchElementException:
                            self.dict_properties['Price'].append('N/A')     

                        try:
                            product_amount = self.driver.find_element(By.CLASS_NAME, 'athenaProductVariations_listItem').text
                            self.dict_properties['Product amount'].append(product_amount)
                        except NoSuchElementException:
                            self.dict_properties['Product amount'].append('N/A')

                        try:
                            product_savings_amount = self.driver.find_element(By.CLASS_NAME, 'productPrice_savingAmount').text
                            self.dict_properties['Product savings amount'].append(product_savings_amount)
                        except NoSuchElementException:
                            self.dict_properties['Product savings amount'].append('N/A')

                        try:
                            product_flavour = self.driver.find_element(By.CLASS_NAME, 'athenaProductVariations_dropdownSegment').text
                            self.dict_properties['Product flavour'].append(product_flavour)
                        except NoSuchElementException:
                            self.dict_properties['Product flavour'].append('N/A')

                        try:
                            reviews = self.driver.find_element(By.CLASS_NAME, 'productReviewStars_numberOfReviews').text
                            self.dict_properties['Number of reviews'].append(reviews)
                        except NoSuchElementException:
                            self.dict_properties['Number of reviews'].append('N/A')

            self.dump_data()


    def dump_data(self,dir: str='./raw_data/', filename: str='data.json') -> None:
        '''
        This method dumps the poplated dictionary into a .json file  
        '''

        os.chdir('../celebrity_example/raw_data')
        filepath = os.path.join(dir, filename)
        print('\nPerforming JSON dump...')

        try:
            with open(filepath, 'w') as jsonFile:
                json.dump(self.dict_properties, jsonFile)
            print('Dump complete.')
        except Exception as e:
            print('ERROR: Could not perform dump.')
            print(e)

  
    def upload_to_cloud(self, engine):
      '''
      This method uploads the .json file containing the populated dictionary to Amazon S3. Using pandas, the dictionary is 
      transformed into a tabular format and uploaded to the RDS database. 
      '''  
      s3_client = boto3.client('s3')
      s3_client.upload_file('./raw_data/data.json', 'lakshaicore', 'my_protein_data')
      

       #uploads tabular data to rds
      data = pd.read_json('./raw_data/data.json', encoding = 'utf-8-sig')
      data.to_sql('my_protein_dataset', engine, if_exists='replace')
      df = pd.read_sql_table('my_protein_dataset', engine)
      df.head()
      self.upload_images()
            

    def upload_images(self):
        '''
      This method uploads the image data folder to Amazon s3 
        '''  
        s3_file = s3fs.S3FileSystem()
        local_path = "/Users/lakshmanrajaratnam/Desktop/selenium_demo/celebrity_example/raw_data/images"
        s3_path = "lakshaicore//Users/lakshmanrajaratnam/Desktop/selenium_demo/celebrity_example/raw_data/images"
        s3_file.put(local_path, s3_path, recursive=True)

    def stop_scraping(self):
      '''
      This method stops the scraper once all product details have been scraped and uploaded to AWS. 
      '''
      self.driver.quit()

if __name__ == "__main__":   
  bot = Scraper()
  bot.sign_in_button()
  bot.all_links()
  bot.product_properties()
  bot.upload_to_cloud()
  bot.stop_scraping()





