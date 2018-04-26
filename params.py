# 模拟器监听的端口号
port = '6555'

# driver 设置
desired_caps = {
        'deviceName': '127.0.0.1:%s' % port,
        'platformName': 'Android',
        'platformVersion': '6.0.1',
        'appPackage': 'com.oppo.market',
        'appActivity': '.activity.MainActivity',
        'noReset': True
    }

# 要启动的应用, appium保持在列表最后
exe_files = [
             r'C:\ttmnq\TianTian.exe',
             r'C:\Users\bai\AppData\Local\appium-desktop\Appium.exe'
             ]
