from selenium.common.exceptions import NoSuchElementException
import logging, sys, io
from decimal import Decimal
from urllib.parse import urlparse
sys.path.append('../database')
import insertdata
class testlog:
        def __init__(self,driver,url,pagename):
                self.driver = driver
                o = urlparse(url)
                self.url = o.path
                self.pagename = pagename
                logging.basicConfig(filename="eptlog.log",                      
                        format='%(asctime)s %(message)s',level=logging.INFO,
                        filemode='w')
                self.debug = False
                
        def parseEpt(self): ##Pass in Webdriver instance ## Uses the EPT Sticker
                ##Alternate method for capturing EPT on a page.
                ept = None
                try:
                        eptstr = self.driver.find_element_by_css_selector('a.stamp-success').get_attribute('text')
                        ept = eptstr.split("\s")[0]
                        
                except (NoSuchElementException):
                        try:
                                eptstr = self.driver.find_element_by_css_selector('a.stamp-warning').get_attribute('text')
                                ept = eptstr.split("\s")[0]
                        except NoSuchElementException as err:
                                
                                #logging.error(',{},{},{},{},{},{}'.format('ERROR','threadId','null',self.url,404,err))
                                #self.insertTestData()
                                pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                finally:
                        pass
                if (ept != None):
                        msg = '{},{},{},{},{:f},{},{}'.format('P001','test001','AWS002','BT001',Decimal(ept.strip(" s")),self.url,200)

                        self.insertTestData('info',msg)
                        return ept
                else:
                        return None
                
        def logError(self,url,ErrorMessage):
                print('URL threw error '+ url + ' '+ ErrorMessage)
        
        def metricsService(self,):
                ### Calculate EPT using metricsservice.
                ##Standard way to capture EPT. Works with Communities
                dt1 = self.driver.execute_script("return aura.metricsService.getCurrentPageTransaction()")
                dt = dt1['config']['context']
                ept = dt['ept']
                cmps = dt['attributes']['defaultCmp']
                netrtt = dt['attributes']['network']['rtt']
                downlink = dt['attributes']['network']['downlink']
                cacherec = dt['cacheStats']['AuraRecordStore']
                numcmps = len(cmps)
                if len(cmps) < 1:
                        msg = '{},{},{},{},{},{},{}'.format('P001','test001','AWS002','BT001',self.url,404,"Page load error. No components loaded")
                        logging('error',msg)
                        return None
                else:
                        if (self.debug):
                                msg = '{},{},{},{},{},{:f},{},{},{},{},{},{}'.format(',P001','test001','AWS002','BT001',self.pagename,Decimal(ept),netrtt,downlink,cacherec['hits'],cmps,self.url,200)
                        else:
                                msg = '{},{},{},{},{},{:f},{},{}'.format(',P001','test001','AWS002','BT001',self.pagename,Decimal(ept),self.url,200)
                        logging.info(msg)
                        #self.insertTestData('info',msg)
                        return ept
                
        def navigationTime(self,driver, url): ##For future ##Using Performance API
                x = driver.execute_script("return performance.getEntriesByType('navigation')")
        def insertTestData(self,type,message):
                ### Create the logger
                logger = logging.getLogger('testrunner')
                ### Setup the console handler with a StringIO object
                sIO = io.StringIO()
                sh = logging.StreamHandler(sIO)
                sh.setLevel(logging.INFO)
                fh = logging.FileHandler('testrunner.log','w+')
                ### Optionally add a formatter
                formatter = logging.Formatter('%(asctime)s.%(msecs)03d,%(message)s','%Y-%m-%dT%H:%M:%S')
                sh.setFormatter(formatter)
                fh.setFormatter(formatter)
                ### Add the console handler to the logger
                logger.addHandler(sh)
                logger.addHandler(fh)
                if type == 'info':             
                        logger.info(message)
                        #log_contents = sIO.getvalue().strip()
                        #conn = insertdata.create_connection('../database/testrunner.db')
                        #insertdata.create_ept(conn,(log_contents.split(',')))
                else:
                        logger.error(message)
                        #og_contents = sIO.getvalue().strip()
                        #conn = insertdata.create_connection('../database/testrunner.db')
                        #insertdata.create_error(conn,log_contents)
                
                