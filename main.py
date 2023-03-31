import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import threading

window = tk.Tk()
window.title('數位學習 快樂學習')
window.geometry('600x500')

label = tk.Label(window, text='一鍵學習')
label.pack()

username_var = tk.StringVar()
username_var.set('帳號')
password_var = tk.StringVar()
password_var.set('密碼')

username_entry = tk.Entry(window, textvariable=username_var, width=20, font=('Arial', 14))
username_entry.pack()
password_entry = tk.Entry(window, textvariable=password_var, width=20, font=('Arial', 14))
password_entry.pack()

data = []

def pickClass():
    username = username_var.get()
    password = password_var.get()

    driver = webdriver.Chrome()
    driver.get('https://id.taipei/tpcd/login/oauth')

    search_bar = driver.find_element(By.ID, 'account')
    search_bar.clear()
    search_bar.send_keys(username)

    search_bar = driver.find_element(By.ID, 'pass')
    search_bar.clear()
    search_bar.send_keys(password)

    search_bar = driver.find_element(By.CLASS_NAME, 'login_btn')
    search_bar.send_keys(Keys.RETURN)

    time.sleep(3)

    driver.get('https://elearning.taipei/AuthorizationGrant_tpcd.php')

    time.sleep(3)

    driver.get('https://id.taipei/isso/taipeipass')

    time.sleep(3)

    class_list = ['3649', '493', '298', '702', '225', '1517', '3759', '3560', '2651', '2939', '2925', '2655', '1586', '1819', '221', '1775']

    for class_id in class_list:
        url = f'https://elearning.taipei/elearn/courseinfo/index.php?courseid={class_id}'
        driver.get(url)

        search_bar = driver.find_element(By.TAG_NAME, 'button')
        search_bar.send_keys(Keys.RETURN)

        time.sleep(3)

    driver.close()

    result_text = f'{username} 選課完成'
    textArea.insert('end', result_text)

def open_and_wait(driver, url):
    driver.execute_script(f"window.open('{url}');")
    # 等待新分頁完全載入
    new_tab = driver.window_handles[-1]
    driver.switch_to.window(new_tab)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.modtype_scorm .instancename')))
    driver.find_element(By.CSS_SELECTOR, '.modtype_scorm .instancename').click()
    driver.close()

def learnClass():
    username = username_var.get()
    password = password_var.get()

    driver = webdriver.Chrome()
    driver.get('https://id.taipei/tpcd/login/oauth')

    search_bar = driver.find_element(By.ID, 'account')
    search_bar.clear()
    search_bar.send_keys(username)

    search_bar = driver.find_element(By.ID, 'pass')
    search_bar.clear()
    search_bar.send_keys(password)

    search_bar = driver.find_element(By.CLASS_NAME, 'login_btn')
    search_bar.send_keys(Keys.RETURN)

    time.sleep(3)

    driver.get('https://elearning.taipei/AuthorizationGrant_tpcd.php')
    time.sleep(3)

    driver.get('https://id.taipei/isso/taipeipass')
    time.sleep(3)

    driver.get('http://elearning.taipei/elearn/courserecord/index.php?cstatus=2&ssearch=&mode=0&list=50')
    time.sleep(3)

    table = driver.find_element(By.CLASS_NAME, 'generaltable')

    # 取得table中所有row
    rows = table.find_elements(By.TAG_NAME, "tr")
    # 將每個row中的cell取出，並存入一個二維list中

    for i in range(1, len(rows)):
        row = rows[i]
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = []
        # 取得第一欄和第六欄的資料
        link = cells[0].find_element(By.TAG_NAME, "a")
        url = link.get_attribute("href")
        text = link.text
        row_data.append({"text": text, "url": url})
        row_data.append(cells[5].text)
        data.append(row_data)

    result_text = '待補課程: \n'
    for row in data:
        result_text += f'{row[0]["text"]}\n'
    textArea.insert('end', result_text)

    threads = []
    for row in data:
        t = threading.Timer(int(row[1])*1800, open_and_wait, args=(driver, row[0]['url']))
        t.start()
        threads.append(t)

        if len(threads) >= 2:  # 同時開三個視窗
            for t in threads:
                t.join()
            threads = []

    # 等待剩下的線程完成
    for t in threads:
        t.join()

    driver.close()

button1 = tk.Button(window, text='一鍵選課', width=20, height=3, command=pickClass)
button1.pack()

button2 = tk.Button(window, text='一鍵學習', width=20, height=3, command=learnClass)
button2.pack()

textArea = tk.Text(window, height=30)
textArea.pack()

window.mainloop()
