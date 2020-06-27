import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class Bet365Move(object):
    def __init__(self, driver):
        self.driver = driver

    def in_play(self):
        # Go to the In-Play screen
        WebDriverWait(self.driver, 50).until(
            EC.visibility_of_element_located((By.XPATH,
            '//div[contains(@class, "MainHeaderCentreWide_Link")]/'
            'div[contains(text(), "My Bets")]')))
        try:
            self.driver.find_element_by_xpath(
                '//div[contains(@class, "MainHeaderCentreWide_Link")]/'
                'div[contains(text(), "In-Play")]').click()
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH,
                '//div[contains(text(), "Event View")]'))).click()

            logging.info('move to the In-Play is successed!')
        except:
            logging.error('move to the In-Play is failed...')

    def my_bets(self):
        # Go to the My  Bets screen
        try:
            WebDriverWait(self.driver, 50).until(
                EC.visibility_of_element_located((By.XPATH,
                '//div[contains(@class, "MainHeaderCentreWide_Link")]/'
                'div[contains(text(), "My Bets")]'))).click()

            logging.info('move to the "My Bets" is successed!')
        except:
            logging.error('move to the "My Bets" is failed...')

    def open_all_leagues(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME,
                'ipn-Classification-open')))
        except NoSuchElementException:
            # Press the soccer icon.
            WebDriverWait(self.driver, 40).until(
                EC.visibility_of_element_located((By.CLASS_NAME,
                'cis-ClassificationIconSmall-1'))).click()

        # Open all leagues pages.
        closed_leagues = self.driver.find_elements_by_class_name(
            'ipn-Competition-closed')

        for i in range(len(closed_leagues)):
            closed_leagues[i].click()