import logging
import os
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from Bet365Move import *
from Bet365GetData import *
from Bet365AMG import *
from Bet365CashOut import *
from Bet365Mongo import *


class Bet365Main(object):
    start_mode = 'd'

    def __init__(self):
        # Start Firefox
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.bet365.com/#/HO/')
        self.driver.set_window_size(1420, 1200)

        # Los settings
        formater = '%(asctime)s %(levelname)s：%(message)s'
        logging.basicConfig(level=logging.INFO, format=formater)

    def login(self):
        # Login function
        BET365_USERNAME = os.environ['BET365_USERNAME']
        BET365_PASSWORD = os.environ['BET365_PASSWORD']

        try:
            WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located((By.CLASS_NAME,
                'hm-MainHeaderRHSLoggedOutWide_Login'))).click()

            username = WebDriverWait(self.driver, 60).until(
                EC.visibility_of_element_located((By.CLASS_NAME,
                'lms-StandardLogin_Username')))
            password = self.driver.find_element_by_class_name(
                'lms-StandardLogin_Password')

            username.clear()
            password.clear()
            username.send_keys(BET365_USERNAME)
            password.send_keys(BET365_PASSWORD)

            self.driver.find_element_by_class_name(
                'lms-StandardLogin_LoginButtonText').click()
            logging.info('Login is successed!')
            return self.driver
        except:
            logging.error('Login is failed...')

    def bet_monitoringa(self):
        # Creating a module.
        bet365move = Bet365Move(driver)
        bet365getdata = Bet365GetData(driver)
        bet365cashout = Bet365CashOut(driver)

        # Automatic monitoring.
        while True:
            # Move to the "In-Play" screen.
            bet365move.in_play()
            bet365move.open_all_leagues()

            # Get all game data(time, scores).
            judg_data = bet365getdata.get_jude_data()

            # Determine the game to play.
            bet365agm = Bet365AMG(driver)
            bet365agm.find_game_bet(judg_data)

            # Determination of startup mode
            if (Bet365Main.start_mode == 'd'):
                break

            # Make sure you are betting.
            for _ in range(5):
                try:
                    self.driver.find_element_by_class_name(
                        'hm-HeaderMenuItemMyBets_MyBetsCount')
                    print('ok')
                    bet365cashout.main(bet365move, bet365getdata)
                except NoSuchElementException:
                    logging.info('No games have been bet.')
                    time.sleep(57)

    def save_page_html(self):
        # Save the html fo the currently displayed page to a file.
        path = '/Users/ryuya/work/03_project/Bet365/AutomationTools'
        filename = 'bet365.html'

        time.sleep(5)
        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser').prettify()
        with open(path + filename, 'w+') as f:
            f.write(soup)
        logging.info('save html file is successed!.')


if __name__ == '__main__':
    # Start Firefox and login bet365.
    bet365main = Bet365Main()
    driver = bet365main.login()

    # Get start mode.
    try:
        Bet365Main.start_mode = sys.argv[1]
    except IndexError:
        logging.info('start mode is Normal')

    bet365main.bet_monitoringa()
