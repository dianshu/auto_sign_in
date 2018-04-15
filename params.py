# driver 设置
desired_caps = {
        'deviceName': '127.0.0.1:62001',
        'platformName': 'Android',
        'platformVersion': '4.4.2',
        'appPackage': 'com.oppo.market',
        'appActivity': '.activity.MainActivity',
        'noReset': True
    }

# 要启动的应用, appium保持在列表最后
exe_files = [
             r'C:\Program Files\Nox\bin\Nox.exe',
             r'C:\Users\bai\AppData\Local\appium-desktop\Appium.exe'
             ]
