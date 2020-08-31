from time import sleep
import os
from appium import webdriver
import yaml
from selenium.webdriver.common.by import By


class TestDemo:

    def setup(self):

        with open('phone.yml')as f:
            desired_caps = yaml.safe_load(f)['mumu_xueqiu']
            # desired_caps['app']=f'{os.path.abspath(os.pardir)}{os.sep}app{os.sep}xueqiu.apk'
            # print(desired_caps['app'])
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(10)

    def teardown(self):
        self.driver.quit()

    def test_search_price(self):
        self.driver.find_element_by_id("com.xueqiu.android:id/home_search").click()
        self.driver.find_element_by_id("com.xueqiu.android:id/search_input_text").send_keys('阿里巴巴')
        self.driver.find_element_by_xpath('//*[@resource-id="com.xueqiu.android:id/name"][@text="阿里巴巴"]').click()
        current_price = self.driver.find_element_by_xpath(
            "//*[@resource-id='com.xueqiu.android:id/current_price']").text
        print('当前的股价为:',current_price)
        assert float(current_price) > 200



    def test_xpath_father_son_element_locate(self):
        self.driver.find_element_by_id("com.xueqiu.android:id/home_search").click()
        self.driver.find_element_by_id("com.xueqiu.android:id/search_input_text").send_keys('阿里巴巴')
        self.driver.find_element_by_xpath('//*[@resource-id="com.xueqiu.android:id/name"][@text="阿里巴巴"]').click()
        self.driver.find_element_by_xpath('//*[@resource-id="com.xueqiu.android:id/title_container"]'
                                          '//android.widget.TextView[3]').click()
        no_user_text = self.driver.find_element_by_xpath("//*[@text='阿里巴巴官方账号']").text
        print("查找的账号：",no_user_text)
        assert no_user_text == '阿里巴巴官方账号'

    def test_uiautomator_use(self):
        # 通过父类的tab的id查找子类当中带有【行情】关键字的tab文案
        self.driver.find_element_by_android_uiautomator(
            'resourceId("android:id/tabs").childSelector(text("行情"))').click()
        # 定位到tab的icon的id，然后通过兄弟元素的文案【交易】定位到这个icon
        self.driver.find_element_by_android_uiautomator(
            'resourceId("com.xueqiu.android:id/tab_icon").fromParent(text("交易"))').click()
        print('跳转到交易页成功')
        assert  '交易' in self.driver.page_source

