import os
import yaml
from selenium.common.exceptions import NoSuchElementException
from utils.path import SNAPSHOT_DIR, WEB_PAGES_DIR


class Page(object):
    def __init__(self, driver, yaml_file=None):
        self.driver = driver
        if yaml_file is not None:
            file_path = os.path.join(WEB_PAGES_DIR, yaml_file)
            with open(file_path, encoding='utf-8') as f:
                self.elements = yaml.safe_load(f)

    def __getattr__(self, item):
        element_loc = self.elements.get(item, None)
        if item is None:
            raise AttributeError(f'该属性:{item}未配置')

        try:
            element = self.driver.find_element(*element_loc)
        except NoSuchElementException:
            snapshot_file = os.path.join(SNAPSHOT_DIR, f'not_found_{item}.png')
            self.driver.save_screen_shot(snapshot_file)
            raise NoSuchElementException(f"定位不到元素: {item}[{element_loc}]")
        else:
            setattr(self, item, element)
            return element


