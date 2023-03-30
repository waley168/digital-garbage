import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# 第1步，例項化object，建立視窗window
window = tk.Tk()

# 第2步，給視窗的視覺化起名字
window.title('數位學習 快樂學習')

# 第3步，設定視窗的大小(長 * 寬)
window.geometry('600x500')  # 這裡的乘是小x

text = tk.Label(window, text=f'一鍵學習').pack()
var1 = tk.StringVar() #宣告字串變數
var1.set('帳號')
var2 = tk.StringVar() #宣告字串變數
var2.set('密碼')
# 第4步，在圖形介面上設定輸入框控制元件entry框並放置
e1 = tk.Entry(window, textvariable=var1, width=20, font=('Arial', 14))  # 顯示成明文形式
e1.pack()
e2 = tk.Entry(window, textvariable=var2, width=20, font=('Arial', 14))  # 顯示成明文形式
e2.pack()

def insert_point():
    acc = var1.get()
    pas = var2.get()

    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://id.taipei/tpcd/login/oauth")
    print(driver.title)
    search_bar = driver.find_element(By.ID, 'account')
    search_bar.clear()
    search_bar.send_keys(acc)
    search_bar = driver.find_element(By.ID, 'pass')
    search_bar.clear()
    search_bar.send_keys(pas)
    search_bar = driver.find_element(By.CLASS_NAME, 'login_btn')
    search_bar.send_keys(Keys.RETURN)
    time.sleep(3)
    driver.get("https://elearning.taipei/AuthorizationGrant_tpcd.php")
    time.sleep(3)
    driver.get("https://id.taipei/isso/taipeipass")
    time.sleep(3)

    class_list = [
        '3649', '493', '298', '702', '225', '1517', '3759', '3560', '2651', '2939', '2925', '2655', '1586', '1819', '221', '1775'
    ]

    for class_item in class_list:
        url = "http://elearning.taipei/elearn/courseinfo/index.php?courseid=" + class_item
        driver.get(url)
        search_bar = driver.find_element(By.TAG_NAME, 'button')
        search_bar.send_keys(Keys.RETURN)
        time.sleep(3)
    driver.close()
    totaltext = 'test'+acc+pas
    t.insert('end', totaltext)

# 第6步，建立並放置按鈕分別觸發兩種情況
b1 = tk.Button(window, text='一鍵學習', width=20, height=3, command=insert_point)
b1.pack()

# 第7步，建立並放置一個多行文字框text用以顯示，指定height=3為文字框是三個字元高度
t = tk.Text(window, height=30)
t.pack()
# 第8步，主視窗迴圈顯示
window.mainloop()
# pip install pyinstaller
# pyinstaller -F -w --icon=linkmall_ico_final.ico main.py