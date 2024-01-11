import os
import Global_Setting_Var
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess


def KillIOS():
    output = os.popen("wmic process get description").read()
    if "chrome.exe" in output:
        os.system("taskkill /f /t /IM chrome.exe")
        # pathChromDriver = Global_Setting_Var.chromedriver
        # driver = webdriver.Chrome(pathChromDriver)
        # driver.quit()


def OpenSite(site):

    global driver

    options = Options()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.binary_location = Global_Setting_Var.chromepath

    pathChromDriver = Global_Setting_Var.chromedriver
    driver = webdriver.Chrome(executable_path=pathChromDriver, chrome_options=options)
    driver.maximize_window()
    driver.get(site)



