import time
import sys
import re
ScreenletPath = sys.path[0]
ScreenletPath = ScreenletPath.replace('/backend','')
from login import Login;
from selenium.webdriver.chrome import service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.opera import options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

def delete(temp):
    print temp;
    deleted = False;
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless");
    chrome_options.add_argument("--disable-gpu");
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(1120, 550);
    driver.get("https://keep.google.com")
    if "accounts" in driver.current_url.encode('utf-8'):
        Login(driver);
    try:
        time.sleep(6);
        to_write = [];#List to be written in file;
        if type(temp) != list:
            addNew(temp, driver);
            temp = [];
        note = driver.find_element_by_xpath("//*[@class='gkA7Yd-sKfxWe rymPhb-IZ65Hb-gkA7Yd']");
        items = note.find_elements_by_xpath("//*[@class='CmABtb RNfche']");
        for item in items:
            print item;
            for deleted_content in temp:
                if deleted_content in str(item.get_attribute('innerText')):
                    check_box = item.find_element_by_xpath(".//*[@class = 'Q0hgme-MPu53c IZ65Hb-MPu53c VIpgJd-MPu53c']");
                    # if "aria-checked='false'" in check_box.get_attribute("outerHTML").encode('utf-8'):
                    #     print "What"
                    driver.execute_script("arguments[0].click();", check_box);
                    break;
        for item in items:
            item = item.find_element_by_xpath(".//*[@class='notranslate IZ65Hb-YPqjbf CmABtb-YPqjbf']");
            print str(item.get_attribute('innerHTML').encode('utf-8'));
            for deleted_content in temp:
                if deleted_content in str(item.get_attribute('innerHTML').encode('utf-8')):
                    deleted = True;
            if deleted!=True:
                if str(item.get_attribute('innerHTML').encode('utf-8')) not in to_write:
                    to_write.append(item.get_attribute('innerHTML').encode('utf-8'));
            deleted=False;
        write_to_file(to_write);
        driver.quit();
        return []
    except:
        print("Box or Button not found in google.com");
        driver.quit();
        return temp;

def write_to_file(temp):
    print "Loading text to context.txt";
    filePath = ScreenletPath + '/files/contents.txt';
    thefile = open(filePath, 'w')
    for item in temp:
        thefile.write("%s\n" % item);

def addNew(text, driver):
    try:
        print "Adding Item";
        note = driver.find_element_by_xpath("//*[@class='notranslate IZ65Hb-YPqjbf CmABtb-YPqjbf']");
        driver.execute_script("arguments[0].click();",note);
        item = driver.find_element_by_xpath(".//*[@class='CmABtb aptq0d-ibnC6b RNfche']");
        item = item.find_element_by_xpath(".//*[@class='notranslate IZ65Hb-YPqjbf CmABtb-YPqjbf']");
        item.send_keys(text);
        time.sleep(2);
        closeModal = driver.find_element_by_xpath("//*[@class='VIpgJd-TUo6Hb-xJ5Hnf XKSfm-L9AdLc-AHe6Kc eo9XGd']");
        driver.execute_script("arguments[0].click();",closeModal);
        time.sleep(2);
        return;
    except:
        print("Box or Button not found in google.com");

if __name__ == "__main__":
     delete([]);
