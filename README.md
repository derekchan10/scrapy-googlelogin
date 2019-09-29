# scrapy-googlel

## 安裝方法

使用 pip 安裝

    $ pip install scrapy-googlelogin

或者使用 pipenv 安装

    $ pipenv install scrapy-googlelogin

## 配置

1. 此中间件依赖 Selenium 模拟登录谷歌，采用的是 Chrome Driver，首先在 settings.py 配置Selenium相关参数

        # Chrome headless config
        CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'
        
        SELENIUM_DRIVER_NAME = 'chrome'
        SELENIUM_DRIVER_EXECUTABLE_PATH = CHROME_DRIVER_PATH
        # SELENIUM_DRIVER_ARGUMENTS=['--no-sandbox','--headless']
        SELENIUM_DRIVER_ARGUMENTS=['user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"']  # '--headless' if using chrome instead of firefox

    注意事项：

    - 使用此中间件之前请先安装 Chrome Driver，然后配置对应路径
    - —headless 可实现无UI界面抓取数据
    - 上线到Linux服务器需配置—no-sandbox

2. 在 Scrapy 中的 settings.py 配置 Google 模拟登入相关参数：

        GOOGLE_ACCOUNT = 'YOUR_GOOGLE_ACCOUNT' # 邮箱账号
        GOOGLE_PWD = 'YOUR_GOOGLE_PASSWORD' # 密码
        GOOGLE_NAME = 'YOUR_GOOGLE_NAME' # 你的谷歌账号名，用来检测是否正确登入

    可能会遇到需要填写验证码的情况，这里使用 Google 二次验证来避免这次情况，需在谷歌账号开启二次验证，使用谷歌验证码验证，然后在 settings.py 加入以下配置：

        GOOGLE_OTPKEY = 'YOUR_OTPKEY'

3. 在 Scrapy 中的 settings.py 配置中间件：

        DOWNLOADER_MIDDLEWARES = {
            'googlelogin.selenium.SeleniumDownloaderMiddleware': 800,
            'googlelogin.googlelogin.GoogleLoginDownloaderMiddleware': 801
        }

    或者在 Spider 的 custom_settings 中配置：

        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'googlelogin.selenium.SeleniumDownloaderMiddleware': 800,
                'googlelogin.googlelogin.GoogleLoginDownloaderMiddleware': 801
            }
        }

4. 在 Spider 中使用 SeleniumRequest 抓取数据：

        from googlelogin.selenium import SeleniumRequest
        ...
        ...
        
        class Googleplay(scrapy.Spider):
            def start_requests(self):
                url = 'https://...'
                yield SeleniumRequest(url=url, callback=self.parse)
        ...
        ...

5. 为了判断最终页面有没准确，需在 Spider 配置 css_selector 属性：

    css_selector = 'table h3'

## 其他配置

- 如果需要抓取 iframe 里面的内容，可以在 Spider 增加属性：

        iframe_selector = '#iframe'

## 备注

selenium：[https://github.com/SeleniumHQ/selenium/](https://github.com/SeleniumHQ/selenium/)