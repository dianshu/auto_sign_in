# coding:utf-8
from appium import webdriver
from time import sleep
from params import desired_caps
import logging
import traceback
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction


class SignIn(object):
    logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

    def __init__(self):
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(6)

    def main(self):
        try:
            logging.info('签到开始')
            # 由于脚本采用的执行应用商店的签到后，再单击打开别的app的方法来进行其余app的签到
            # self.app_store_sign_in()必须第一个执行。
            self.app_store_sign_in()
            self.game_center_sign_in()
            self.community_sign_in()
            logging.info('签到结束')
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
            logging.info('应用中心 已签到')
        else:
            logging.info('应用中心 未签到')
        # 当前应用置入后台
        self.driver.close_app()

    def community_sign_in(self):
        # 打开应用
        self.driver.find_element_by_accessibility_id('OPPO社区').click()
        # 等待6s，跳过欢迎界面
        sleep(6)
        # 单击第一步的‘签到’
        self.driver.find_element_by_id('com.oppo.community:id/main_header_icon_img').click()
        # 单击第二步的‘签到’
        self.driver.find_element_by_id('com.oppo.community:id/my_homepage_item_view_label').click()
        # 单击第三步的‘签到’
        try:
            sign_in = self.driver.find_element_by_xpath('//*[@resource-id="com.oppo.community:id/browser_layout"]/*[1]/*[5]/*[1]')
            sign_in.click()
            if sign_in.text == '已签到':
                logging.info('OPPO社区 已签到')
            else:
                logging.info('OPPO社区 未签到')
        except NoSuchElementException:
            logging.info('OPPO社区 已签到')
        # 置入后台,此处实现方法为单击Home键
        self.driver.press_keycode(3)

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
            logging.info('游戏中心 已签到')
        else:
            logging.info('游戏中心 未签到')
        self.driver.back()
        # 安装游戏
        self.driver.find_element_by_id('com.nearme.gamecenter:id/download_score').click()
        # 获取屏幕中所列的游戏
        installed_game_count = 0
        while installed_game_count < 3:
            games = self.driver.find_elements_by_id('com.nearme.gamecenter:id/v_app_item')
            for game in games:
                try:
                    # 获取游戏的体积
                    volume = game.find_element_by_id('com.nearme.gamecenter:id/tv_size').text
                    # 如果游戏小于50M，单击安装
                    if installed_game_count < 3 and 'M' in volume and float(volume[:-1]) < 50:
                        # 下载
                        game.find_element_by_id('com.nearme.gamecenter:id/tv_hint').click()
                        # 安装
                        self.install_app_from_screen(installed_game_count + 1)
                        installed_game_count += 1
                except NoSuchElementException:
                    pass
            if installed_game_count >= 3:
                break
            else:
                self.next_screen()
        logging.info('游戏中心安装%d款游戏 已完成' % installed_game_count)
        self.driver.back()
        # 打开游戏
        self.driver.find_element_by_id('com.nearme.gamecenter:id/open_score').click()
        self.driver.find_element_by_id('com.nearme.gamecenter:id/close_beta_game_btn').click()
        logging.info('游戏中心打开游戏 已完成')
        # 置入后台,此处实现方法为单击Home键
        self.driver.press_keycode(3)
        self.remove_apps_from_screen()

    def next_screen(self, count=1):
        """
        滑动屏幕到下一屏
        :param count: 滑动的次数 int
        :return:
        """
        height = self.driver.get_window_size()['height']
        for _ in range(count):
            self.driver.swipe(0, int(height * 0.95), 0, int(height * 0.05), 1000)

    def install_app_from_screen(self, install_count):
        try:
            logging.info('开始安装第%d个游戏' % install_count)
            next_step_btn = WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.ID, 'com.android.packageinstaller:id/ok_button')))
            try:
                while next_step_btn:
                    next_step_btn.click()
            except:
                pass
            complete_btn = WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.ID, 'com.android.packageinstaller:id/done_button')))
            complete_btn.click()
            logging.info('安装成功')
        except:
            traceback.print_exc()
            logging.error('游戏安装失败')

    def remove_apps_from_screen(self):
        logging.info('开始卸载游戏')
        self.driver.press_keycode(3)
        games = self.driver.find_elements_by_xpath('//*[@resource-id="com.vphone.launcher:id/workspace"]/*[1]/*[1]/*')[::-1]
        action = TouchAction(self.driver)
        uninstall_pos = {'x': 190, 'y': 100}
        for game in games:
            game_name = game.text
            if game_name == '腾讯新闻':
                break
            action.long_press(el=game).move_to(**uninstall_pos).release().perform()
            self.driver.find_element_by_id('com.android.packageinstaller:id/ok_button').click()
            sleep(3)
            logging.info('%s 卸载成功' % game_name)


if __name__ == '__main__':
    SignIn().main()
