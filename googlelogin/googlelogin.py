from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyotp

class GoogleLoginDownloaderMiddleware(object):
    cookies = None
    login_url = 'https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        driver = request.meta.get('driver')
        if self.cookies == None:

            driver.get(self.login_url)
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'headingText'))
            )

            print('start login...')
            driver.find_element(By.ID, 'identifierId').send_keys(spider.settings.get('GOOGLE_ACCOUNT'))
            driver.find_element(By.CSS_SELECTOR, '#identifierNext > div > button').click()

            print('account next...')
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#passwordNext > div > button"))
            )

            driver.find_element(By.CSS_SELECTOR, '#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input').send_keys(spider.settings.get('GOOGLE_PWD'))
            driver.execute_script('document.querySelector("#passwordNext > div > button").click()')
            print('pwd next...')

            try:
                if(spider.settings.get('GOOGLE_OTPKEY')):
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "totpPin"))
                    )
                    driver.implicitly_wait(1)
                    totp = pyotp.TOTP(spider.settings.get('GOOGLE_OTPKEY'))
                    print('totp', totp.now())
                    driver.find_element(By.ID, 'totpPin').send_keys(totp.now())
                    driver.execute_script('document.querySelector("#totpNext > div > button").click()')
            except:
                pass

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "figure"))
            )

            WebDriverWait(driver, 20).until(
                element_has_content(driver.find_element(By.TAG_NAME, 'h1').text, spider.settings.get('GOOGLE_NAME'))
            )

            print('login success...')

            print('record cookies...')

            request.cookies = self.cookies = driver.get_cookies()

        driver.get(request.url)
        if (hasattr(spider, 'iframe_selector')):
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, getattr(spider, 'iframe_selector')))
            )

            iframe = driver.find_element(By.CSS_SELECTOR, getattr(spider, 'iframe_selector'))
            driver.switch_to.frame(iframe)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, spider.css_selector))
        )

        body = str.encode(driver.find_element(By.TAG_NAME, 'html').get_attribute('outerHTML'))


        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': driver})
        return HtmlResponse(
            request.url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class element_has_content(object):
    def __init__(self, locator, content):
        self.locator = locator
        self.content = content

    def __call__(self, driver):
        result = self.locator.find(self.content)
        if (result != -1):
            return True
        else:
            return False
