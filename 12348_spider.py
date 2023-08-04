import os
import sys
import time 
import json


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = r"D:\workspace\tools\chromedriver_win32\chromedriver.exe" # 这里修改浏览器驱动路径
if not os.path.exists(chrome_driver_path):
    print(f"{chrome_driver_path} does not exist!!!")
    exit()
service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])

browser = webdriver.Chrome(service=service, options=options)
# url = "https://www.baidu.com/"
url = "http://www.12348.gov.cn/#/publicies/lawyerlist/consultList"
browser.get(url)
browser.maximize_window()

time.sleep(40)

# 手动设置好时间区间
# year = 2022
year = int(sys.argv[1])
start_page = 0
# fout = open(f"{year}_0101-0110_consults.txt", 'w', encoding="utf8")
fout = open(f"{year}_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_0101-0331_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_0401-0430_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_0501-0531_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_0601-0630_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_0701-0731_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_0801-0831_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_0901-0930_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_1001-1031_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_1101-1130_consults.txt", 'w', encoding="utf8")
# fout = open(f"{year}_1201-1231_consults.txt", 'w', encoding="utf8")
page_count = 0
browser.implicitly_wait(10)
wait = WebDriverWait(browser, 6000)
wait_qa = WebDriverWait(browser, 5)
while True:
    page_count += 1
    if page_count >= start_page:
        # 等待页面加载
        cur_page = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@page-data="{}"][@page-rel="itempage"]'.format(str(page_count)))))
        # 判断页数是否一致
        if cur_page.get_attribute("class") == "pageItemActive":
            pass
        else:
            print(f"page count: {page_count}, but cur page not active")

        # 获取咨询列表，遍历爬取内容
        # consultlist = browser.find_elements(By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/ul[2]/li/div[2]/a")
        consult = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/ul[2]/li/div[2]/a")))
        consult = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/ul[2]/li/div[2]/a")))
        i = 0
        while True:
            i+=1
            if i > 5:
                break
            try:
                consult.click()
                browser.switch_to.window(browser.window_handles[1])
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                break
            except:
                time.sleep(20)
                consult = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/ul[2]/li/div[2]/a")))
                consult = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/ul[2]/li/div[2]/a")))
        consultlist = wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/ul[2]/li/div[2]/a")))
        # 处理意外弹窗
        try:
            alert = Alert(browser)
            alert.accept()
        except:
            pass

        # 遍历咨询列表
        for consult in consultlist:
            try:
                consult.click()
            except:
                jdict = {
                    "source": "12348中国法律服务网",
                    "year": year,
                    "page": page_count,
                    "query": "",
                    "response": ""
                }
                fout.write(json.dumps(jdict, ensure_ascii=False)+'\n')
                continue
            browser.switch_to.window(browser.window_handles[1])
            # 处理意外弹窗
            try:
                alert = Alert(browser)
                alert.accept()
            except:
                pass

            # 获取query
            try:
                # query_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/p")))
                # query = query_element.text
                x = 0
                while True:
                    try:
                        query_element = wait_qa.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/p")))
                        # query_element = browser.find_elements(By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/p")
                        query = query_element.text
                    except:
                        query = ""
                    x += 1
                    if query != "" or x > 3:
                        break
                    else:
                        browser.refresh()
                        time.sleep(2)
            except:
                query = ""
            
            # 获取response
            try:
                x = 0
                while True:
                    # response_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[3]/ul/li/p[1]")))
                    try:
                        response_element = wait_qa.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[3]/ul/li/p[1]")))
                        # response_element = browser.find_elements(By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[3]/ul/li/p[1]")
                        response = response_element.text
                    except:
                        response = ""
                    x += 1
                    if response != "" or x > 3:
                        break
                    else:
                        browser.refresh()
                        time.sleep(2)
            except:
                response = ""
            # TODO 处理有追问的情况
            # print("="*100)
            # print(query)
            # print(response)
            jdict = {
                "source": "12348中国法律服务网",
                "year": year,
                "page": page_count,
                "query": query,
                "response": response
            }
            fout.write(json.dumps(jdict, ensure_ascii=False)+'\n')
            try:
                browser.close()
            except:
                pass
            browser.switch_to.window(browser.window_handles[0])

        print(f"page {page_count} done")
        fout.flush()
    else:
        print(f"start page {start_page} not current page {page_count}")
    pages = browser.find_element(By.XPATH, '//*[@id="page"]')
    next_page = pages.find_element(By.XPATH, '//*[@id="nextPage"]')

    if next_page.get_attribute("class") == "pageItemDisable":
        fout.close()
        print(f"all pages done")
        break
    else:
        next_page.click()
        time.sleep(20)


# time.sleep(10000)
