# coding:utf-8
from appium import webdriver
from time import sleep
from params import desired_caps
import logging
import traceback


class SignIn(object):
    logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

    def __init__(self):
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(6)

    def main(self):
        try:
            # 由于脚本采用的执行应用商店的签到后，再单击打开别的app的方法来进行其余app的签到
            # self.app_store_sign_in()必须第一个执行，其余app顺序随意
            self.app_store_sign_in()
            self.game_center_sign_in()
            self.community_sign_in()
        except:
            traceback.print_exc()
        finally:
            self.driver.quit()

    def app_store_sign_in(self):
        # 等待6s，跳过欢迎界面
        sleep(6)
        # 单击‘我’
        self.driver.find_element_by_xpath("//*[@resource-id='android:id/tabs']/*[5]").click()
        # 单击第一步的‘签到’
        self.driver.find_element_by_id('com.oppo.market:id/iv_sign_in').click()
        # 单击第二步的‘签到’
        sign_in = self.driver.find_element_by_id('com.oppo.market:id/activity_credit_main_sign_btn')
        sign_in.click()
        if sign_in.text == '已签到':
            logging.info('应用中心已签到')
        else:
            logging.info('应用中心未签到')
        # 当前应用置入后台
        self.driver.close_app()

    def game_center_sign_in(self):
        # 打开应用
        self.driver.find_element_by_accessibility_id('游戏中心').click()
        # 等待6s，跳过欢迎界面
        sleep(6)
        # 单击‘我’
        self.driver.find_element_by_xpath('//*[@resource-id="android:id/tabs"]/*[5]').click()
        # 单击‘赢取积分’
        self.driver.find_element_by_id('com.nearme.gamecenter:id/iv_earn_welfare').click()
        # 签到
        self.driver.find_element_by_id('com.nearme.gamecenter:id/sign_score').click()
        sign_in = self.driver.find_element_by_id('com.nearme.gamecenter:id/activity_credit_main_sign_btn')
        sign_in.click()
        if sign_in.text == '已签到':
            logging.info('游戏中心已签到')
        else:
            logging.info('游戏中心未签到')
        self.driver.back()
        # 安装游戏
        self.driver.find_element_by_id('com.nearme.gamecenter:id/download_score').click()
        # 找到体积小于50M的前三个游戏进行安装
        games = self.driver.find_element_by_xpath('//*[@class="android.widget.ListView"]//*[resource-id]')
        # 打开游戏


        # 置入后台,此处实现方法为单击Home键
        self.driver.press_keycode(3)

    def community_sign_in(self):
        # 打开应用
        self.driver.find_element_by_accessibility_id('OPPO社区').click()
        # 等待6s，跳过欢迎界面
        sleep(6)
        # 单击右上角头像
        self.driver.find_element_by_id('com.oppo.community:id/main_header_icon_img').click()
        # 单击第一步的‘签到’
        self.driver.find_element_by_id('com.oppo.community:id/my_homepage_item_view_label').click()
        # 单击第二步的‘签到’
        sign_in = self.driver.find_element_by_id('com.oppo.community:id/my_homepage_item_view_lay')
        sign_in.click()
        if sign_in.text == '已签到':
            logging.info('OPPO社区已签到')
        else:
            logging.info('OPPO社区未签到')
        # 置入后台,此处实现方法为单击Home键
        self.driver.press_keycode(3)


if __name__ == '__main__':
    SignIn().main()