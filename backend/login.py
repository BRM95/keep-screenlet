import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException


def Login(driver):
    try:
        wait = WebDriverWait(driver, 10)
        element = driver.find_element_by_xpath("//*[@type='email']");
        element.send_keys("brmusani@gmail.com");
        try:
            driver.find_element_by_id("identifierNext");
            button =  wait.until(EC.element_to_be_clickable((By.ID, "identifierNext")))
            driver.execute_script("arguments[0].click();", button);
            #driver.save_screenshot('/home/bm95/Downloads/Atom Files/Keep Application/login_failed.png');
            button =  wait.until(EC.element_to_be_clickable((By.ID, "passwordNext")));
        except:
            button = wait.until(EC.element_to_be_clickable((By.ID,"next")));
            driver.execute_script("arguments[0].click();", button);
            button = wait.until(EC.element_to_be_clickable((By.ID,"signIn")));
        finally:
            time.sleep(2);
            element = driver.find_element_by_xpath("//*[@type='password']");
            element.send_keys("bilalmusani81495");
            driver.execute_script("arguments[0].click();", button);
            return driver;
    except TimeoutException:
        return driver;
