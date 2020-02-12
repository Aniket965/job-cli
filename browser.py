
from selenium import webdriver as wd
import selenium

class Browser:
    __instance = None
    chrome = None
    def __init__(self,driver_path):
        if Browser.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.driver_path = driver_path
            chrome_options = wd.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('log-level=3')
            self.chrome = wd.Chrome(self.driver_path,options=chrome_options)
            Browser.__instance = self
        
    @staticmethod
    def get(driver_path):
        if Browser.__instance == None:
            return Browser(driver_path)
        else:
            return Browser.__instance
            
