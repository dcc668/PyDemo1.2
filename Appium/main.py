from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

desired_caps = {}
desired_caps['platformName'] = "Android"         # 声明是ios还是Android系统
desired_caps['PLATFORMVERSION'] = '4.4.2'        # Android内核版本号，可以在夜神模拟器设置中查看
desired_caps['deviceName'] = '127.0.0.1:62001'   # 连接的设备名称
desired_caps['appPackage'] = 'com.amahua.ompimdrt'    # apk的包名
desired_caps['appActivity'] = 'com.mh.movie.core.mvp.ui.activity.SplashActivity'  # apk的launcherActivity

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)          # 建立 session

html=driver.page_source
driver.find_element_by_id("com.amahua.ompimdrt:id/button_enter").click()      # 点击元素
driver.find_element_by_id("com.amahua.ompimdrt:id/iv_notice_close").click()      # 点击元素
driver.find_element_by_id("com.amahua.ompimdrt:id/tv_dialog_cancel").click()      # 点击元素
driver.find_element_by_xpath("************").send_keys(u'123456')   # 发送键值
driver.quit()      # 退出 session
