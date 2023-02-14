from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os


def main():
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_driver_path = r"E:\codes\auto_online_class\chromedriver.exe" # 这里修改浏览器驱动路径
    if not os.path.exists(chrome_driver_path):
        print(f"{chrome_driver_path} does not exist!!!")
        exit()
    browser = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
    url = r"https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
    browser.get(url)

    date = "2023-02-16" # 日期改这里
    citys = [           # 城市改这里
        "淮安",
        "南京",
        "无锡",
        "徐州",
        "常州",
        "苏州",
        "南通",
        "连云港",
        "扬州",
        "镇江",
        "盐城",
        "泰州",
        "宿迁",
        "杭州",
        "宁波",
        "温州",
        "嘉兴",
        "湖州",
        "绍兴",
        "金华",
        "衢州",
        "舟山",
        "台州",
        "丽水",
        "上海"
    ]

    if not os.path.exists(date):
        os.makedirs(date)
    for start_city in citys:
        if not os.path.exists(os.path.join(date, start_city)):
            os.makedirs(os.path.join(date, start_city))
        for end_city in citys:
            if start_city == end_city:
                continue
            print(f"exporting all trains from {start_city} to {end_city} ... ")
            fout = open(f"{os.path.join(date, start_city)}/{start_city}2{end_city}.txt", 'w', encoding='utf-8')
            fout.write('车次\t出发站\t发车时间\t到达站\t到达时间\t耗时\n')
            browser.get(url)
            sleep(1) # sleep是为了等待网页打开
            start_input = browser.find_elements(By.XPATH, '//*[@id="fromStationText"]')[0]
            end_input = browser.find_elements(By.XPATH, '//*[@id="toStationText"]')[0]
            date_input = browser.find_elements(By.XPATH, '//*[@id="train_date"]')[0]
            search_button = browser.find_elements(By.XPATH, '//*[@id="query_ticket"]')[0]
            start_input.click()
            start_input.send_keys(start_city, Keys.ENTER)
            sleep(1)
            end_input.click()
            end_input.send_keys(end_city, Keys.ENTER)
            date_input.clear()
            date_input.send_keys(date, Keys.ENTER)
            sleep(1)
            search_button.click()
            sleep(1)
            rows = browser.find_elements(By.XPATH, '/html/body/div[3]/div[7]/div[8]/table/tbody/tr')
            for i, r in enumerate(rows):
                try:
                    checi = r.find_element(By.XPATH, './td[1]/div/div[1]/div/a').text
                    start_station = r.find_element(By.XPATH, './td[1]/div/div[2]/strong[1]').text
                    start_time = r.find_element(By.XPATH, './td[1]/div/div[3]/strong[1]').text
                    end_station = r.find_element(By.XPATH, './td[1]/div/div[2]/strong[2]').text
                    end_time = r.find_element(By.XPATH, './td[1]/div/div[3]/strong[2]').text
                    cost_time = r.find_element(By.XPATH, './td[1]/div/div[4]/strong').text
                    info = [checi, start_station, start_time, end_station, end_time, cost_time]
                    fout.write('\t'.join(info) + '\n')
                except:
                    pass
            fout.close()
            sleep(10) # 频繁查询会被封ip！！！
    sleep(1000)

if __name__ == "__main__":
    main()