#Salesforce Login test with HomePage and EPT 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import json,time
from testlogger import testlog


class TestRunner:
    def __init__(self,DataQueue):
        self.homepageurl = "https://scalegrail--sgdev.lightning.force.com/lightning/page/home?eptVisible=1"
        self.objectPageUrl = "https://scalegrail--sgdev.lightning.force.com/lightning/o/Account/list?filterName=00B6g000009FQ8AEAW"
        self.q = DataQueue
    
    def setup(self):
        chrome_options = Options()  
        #chrome_options.add_argument("--headless")  
        self.driver = webdriver.Chrome(executable_path="/home/axjacob/workspace/projects/ScaleTest/scripts/chromedriver",options=chrome_options)
        driver = self.driver
        return driver

    def __call__(self): ##For multithreading/load tests
       self.start()
    
    def start(self): ## For single user tests
        driver = self.setup()
        ObjectPageEpt = None
        homepageEpt = self.doLogin(driver)
        for x in range(0,20):
            if (homepageEpt != None):
                ObjectPageEpt = self.AccountListPage(driver)
            else:
                pass
            if (ObjectPageEpt != None):
                self.AccountDetailPage(driver)
            else:
                pass
            self.HomePage(driver)
        self.tearDown()

    def doLogin(self,driver):
        try:
            driver.get("https://test.salesforce.com")
        except WebDriverException as err:
            logError(driver.current_url, err)
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys('USERNAME')
        #self.driver.implicitly_wait(6)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("PASSWORD")
        driver.find_element_by_id("Login").click()
        driver.get(self.homepageurl)
        time.sleep(6)
        val = driver.find_element_by_xpath("//span[@class = 'slds-truncate']").get_attribute('title')
        pageName = "homepage"
        return testlog(driver,driver.current_url,pageName).metricsService()
        #return testlog(driver,driver.current_url).parseEpt()
        
    def AccountListPage(self, driver):
        #Get Account List and Detail
        driver.get(self.objectPageUrl)
        time.sleep(5)
        pageName = "Account Home"
        return testlog(driver,driver.current_url,pageName).metricsService()
        #return testlog(driver,driver.current_url).parseEpt()
        
        #print(x[0].duration)
    def AccountDetailPage(self,driver):
        accountId = self.q.getItem()
        self.objectDetailUrl = "https://scalegrail--sgdev.lightning.force.com/lightning/r/Account/{}/view".format(accountId) ##0011k00000eZ30uAAC
        print(self.objectDetailUrl)
        driver.get(self.objectDetailUrl)
        time.sleep(7)
        pageName = "Account Detail"
        return testlog(driver,driver.current_url,pageName).metricsService()
        #return testlog(driver,driver.current_url).parseEpt()
    def HomePage(self,driver):
        self.url = "https://scalegrail--sgdev.lightning.force.com/lightning/page/home"
        driver.get(self.url)
        time.sleep(7)
        pageName = "HomePage"
        return testlog(driver,driver.current_url,pageName).metricsService()
    
    def WaitForElement(self,currentdriver, locator):
        wait = WebDriverWait(currentdriver,10,3)
        wait.until()

    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__": 
    t = TestRunner()
    t.start()