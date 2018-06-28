from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait, Select
from functools import partial
from subprocess import Popen

CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'


class ChroSpider:
    def __init__(self, aguments='', taskkill=False, port=8090, chrome_path=CHROME_PATH):
        """
        :param taskkill: bool, kill chrome.exe
        :param aguments: str, Chromium Command Line Switches, exp:'--healess --blink-settings=imagesEnabled=false'
        :param port: int, debug port
        :param chrome_path: str, the path of chrome.exe
        """
        if taskkill:
            p = Popen('taskkill /f /im chrome.exe')
            p.wait()

        Popen(f'"{chrome_path}" --remote-debugging-port={port} {aguments}')

        options = ChromeOptions()
        options.debugger_address = f'127.0.0.1:{port}'
        self.driver = Chrome(chrome_options=options)
        self.wait = partial(WebDriverWait, self.driver)

    def click(self, value, by='link text'):
        element = self.driver.find_element(by, value)
        element.click()

    def select(self, locator, items, by='visible_text', deselect_all=False):
        """单选或多选菜单

        :param locator: by, value组成的元组，exp:('id', 'SelectID')
        :param items: 多选时传入list, 单选传单个值，如['opt1', 'opt2']或'opt1'
        :param by: 'visible_text'|'value'|'index'
        """
        s = Select(self.driver.find_element(*locator))
        if deselect_all: 
            s.deselect_all()

        select = getattr(s, f'select_by_{by}')
        items = [items] if not isinstance(items, list) else items
        for item in items:
            select(item)

    def checkbox(self, items, by='label', all_locator=None):
        # 如果有全选，通过全选取消所有选中
        if all_locator:
            all_locator.click()
            if all_locator.is_selceted():
                all_locator.click()

        box = self.__find_box(by)
        for item in items:
            box(by, item).click()

    def radio(self, item, by='label'):
        box = self.__find_box(by)
        box(item).click()

    def inputbox(self, text, value, by='id'):
        element = self.driver.find_element(by, value)
        element.send_keys(text)

    def __find_box(self, by):
        def by_label(x):
            return self.driver.find_element_by_xpath(f'//label[text()="{x}"]')

        def by_others(x):
            return self.driver.find_element(by, x)

        if by == 'label':
            func = by_label
        else:
            func = by_others

        return func
