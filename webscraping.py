from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

import os
import requests
from watson import audioToText

filename = 'audio.mp3'

def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


def scrape_site(dni,dia_emisión,mes_emisión,año_emisión,dia_nacimiento,mes_nacimiento,año_nacimiento):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get('https://carnetvacunacion.minsa.gob.pe')
    wait = WebDriverWait(driver, 10)
    time.sleep(0.5)
    driver.delete_all_cookies()
    time.sleep(2)
    driver.refresh()
    time.sleep(2)
    
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-auth/div/div/app-login/div[1]/div/div[2]/div/div/form/div[2]/div/input"))).send_keys(dni)
    
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-auth/div/div/app-login/div[1]/div/div[2]/div/div/form/div[3]/div[1]/div/input-date/div/input[1]"))).send_keys(dia_emisión)
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-auth/div/div/app-login/div[1]/div/div[2]/div/div/form/div[3]/div[1]/div/input-date/div/input[2]"))).send_keys(mes_emisión)
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-auth/div/div/app-login/div[1]/div/div[2]/div/div/form/div[3]/div[1]/div/input-date/div/input[3]"))).send_keys(año_emisión)
    
    wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/app-auth/div/div/app-login/div[1]/div/div[2]/div/div/form/div[4]/div/div/input-date/div/input[1]"))).send_keys(dia_nacimiento)
    wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/app-auth/div/div/app-login/div[1]/div/div[2]/div/div/form/div[4]/div/div/input-date/div/input[2]"))).send_keys(mes_nacimiento)
    wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/app-auth/div/div/app-login/div[1]/div/div[2]/div/div/form/div[4]/div/div/input-date/div/input[3]"))).send_keys(año_nacimiento)
    time.sleep(0.5)
    iframe = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,"iframe")))[0]
    driver.switch_to.frame(iframe)
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.ID, "recaptcha-anchor-label"))).click()
    driver.switch_to.default_content()
    time.sleep(3)
    hola = driver.find_elements(By.TAG_NAME,'re-captcha')[0].get_attribute("class")
    time.sleep(0.5)
    if hola.find("-invalid") > 0 :
        iframe = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,"iframe")))[2]
        driver.switch_to.frame(iframe)
        time.sleep(2)
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,"button")))[1].click()
        time.sleep(2)
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,"button")))[0].click()
        time.sleep(2)
        src = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "audio")))[0].get_attribute("src")
        time.sleep(2.5)

        response = requests.get(src, stream=True)
        saveFile(response,filename)
        response = audioToText(os.getcwd() + '/' + filename)

        rty  = driver.find_elements(By.TAG_NAME,'input')[1]
        rty.send_keys(response)

        buttons2 = driver.find_elements(By.TAG_NAME,'button')[6]
        buttons2.click()
        driver.switch_to.default_content()
        time.sleep(3)
        No_soy_Robot =  wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-auth/div/div/app-login/div[1]/div/div[2]/div/div/form/div[8]/button")))
        No_soy_Robot.click()
        time.sleep(2)
    else:
        print('este 1')
        print(hola)
        driver.switch_to.default_content()
        time.sleep(3)
        No_soy_Robot =  wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-auth/div/div/app-login/div[1]/div/div[2]/div/div/form/div[8]/button")))
        No_soy_Robot.click()
        time.sleep(2)
    try:
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,"mat-dialog-container")))[0]
        time.sleep(1)
        return 500
    except:
        try:
            Terminos =  wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-auth/div/div/app-term/div/div/div/div/div/div[1]/div/div[1]/input")))
            Terminos.click()
            aceptoTerminos = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/app-root/app-auth/div/div/app-term/div/div/div/div/div/div[2]/button")))
            aceptoTerminos.click()
            time.sleep(3)
            Carlos = driver.execute_script("return sessionStorage.getItem('decode_token')")
            driver.close()
            return Carlos
        except:
            time.sleep(1)
            Carlos = driver.execute_script("return sessionStorage.getItem('decode_token')")
            driver.close()
            return Carlos