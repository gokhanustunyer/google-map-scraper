from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver import Keys, ActionChains

from lib.CVHelper import CVHelper
from lib.CitiesHelper import WorldCitiesHelper
from lib.GoogleMapModels import CompanyModel, LocationModel

import time
import os

import pyautogui


class GoogleMapScraper:
    
    BASE_URL = "https://www.google.com/maps"

    def __init__(self) -> None:
        self.worldCitiesHelper = WorldCitiesHelper()
        self.driver = None
        self.is_moved_to_coordinates = False
        self.cv_helper = CVHelper()
        
        self.counter = 1
    
    def start_scraping(self, start_from: LocationModel):
        if (start_from.city != None):
            districts = self.worldCitiesHelper.getDistrictsByCity(start_from.city)
        
        self.towords_coordinates(start_from)
        self.start_crawling()
        time.sleep(5)
        return
        
    def start_crawling(self):
        print("ss saving")
        if not self.is_moved_to_coordinates:
            print("Firstly you have to move a coordinate with towords_coordinates function")
            return
        
        screen_width, screen_height = pyautogui.size()

        center_x = screen_width // 2
        center_y = screen_height  // 2
        
        while self.counter < 200:
            pyautogui.screenshot().save(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', f'temp.png'))
            
            results = self.cv_helper.run_inference()
            
            self.scrap_results_by_click(results)
            
            pyautogui.moveTo(center_x, center_y)
            pyautogui.mouseDown()
            pyautogui.moveRel(-500, 0, duration=0.5)  # -100 piksel sola kaydır, 0.5 saniyede
            pyautogui.mouseUp()
            self.counter += 1
            time.sleep(2)
        
    def crawl_results_by_click(self, shop_coordinates):
        for coordinate in shop_coordinates:
            center_x = coordinate["bbox"]["center_x"]
            center_y = coordinate["bbox"]["center_y"]

            print(self.driver.get_window_size())
            print(center_x, center_y, coordinate)
            
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click()
            
            self.scrap_shop()
            
            time.sleep(2)
    
    def scrap_shop(self) -> CompanyModel:
        company = CompanyModel()
        company.title = self.driver.find_element(By.TAG_NAME, 'h1').text.strip()
        
    
    def towords_coordinates(self, location: LocationModel):
        try:
            if self.driver == None:
                self.driver = GoogleMapScraper.get_driver(False)
                
            self.driver.get(GoogleMapScraper.BASE_URL)
            time.sleep(2)
            
            search_box = self.driver.find_element(By.ID, "searchboxinput")
            ActionChains(self.driver).send_keys_to_element(search_box, f"{location.lat}, {location.lng}").perform()
            self.driver.find_element(By.ID, "searchbox-searchbutton").click()
            self.is_moved_to_coordinates = True
            
            print("moved to location")
            
            for _ in range(20):
                self.driver.find_element(By.ID, "widget-zoom-in").click()
                time.sleep(0.1)
            print("zoom successfull")
            
            time.sleep(3)
        except Exception as ex:
            print("An error accured while moving towords coordinates", ex)
            self.is_moved_to_coordinates = False
        
        
        
    
    @staticmethod
    def get_driver(headless = True) -> webdriver.Chrome:
        driver_options = webdriver.ChromeOptions()
        driver_options.add_argument("--disable-gpu")
        if headless: driver_options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=driver_options)
        driver.maximize_window()
        return driver