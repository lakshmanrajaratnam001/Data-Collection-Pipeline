import unittest
import data_collection_pipeline
from selenium.webdriver.common.by import By
from selenium import webdriver
import time 


#Unit testing is the lower level granuality of testing, whereby individual units of code are tested. 
class ScraperTestCase(unittest.TestCase):
    '''
    Various methods within the class Scraper tested. Assertions made 
    for each unit of code, comparing the expected value with actual value. 
    '''
     
    def setUp(self):
        self.bot = data_collection_pipeline.Scraper()

    def test_sign_in(self):
        time.sleep(5)
        self.bot.sign_in_button()
        expected_value = self.bot.driver.find_element(By.CLASS_NAME, 'headerLogo' )
        actual_value = str
        self.assertTrue(expected_value, actual_value)

    def test_get_product_links(self):
        self.bot.sign_in_button()
        self.bot.get_product_links()
        expected_value = str
        self.assertTrue(expected_value)
    
    def test_get_all_links(self):
        self.bot.sign_in_button()
        self.bot.get_all_links()
        expected_value = ('https://www.myprotein.com/nutrition/protein.list?pageNumber=2') 
        self.assertTrue(expected_value)

    def test_get_images(self):
        self.bot.driver.get('https://www.myprotein.com/sports-nutrition/impact-whey-protein/10530943.html')
        expected_value = list
        actual_value = self.bot.get_images()
        self.assertTrue(expected_value, actual_value)

    def test_friendly_id(self):
        self.bot.sign_in_button()
        self.bot.all_links()
        self.bot.friendly_id()
        expected_value = str
        actual_value = self.bot.driver.find_element(By.CLASS_NAME, 'productAddToWishlist')
        self.assertTrue(expected_value, actual_value)


if __name__ == "__main__":   
    unittest.main(verbosity=2)
