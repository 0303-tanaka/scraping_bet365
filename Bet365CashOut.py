import logging
import time

from Bet365Mongo import *


class Bet365CashOut(object):
    def __init__(self, driver):
        self.driver = driver

    def main(self, bet365move, bet365getdata):

        # Get league name.
        league_name = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ipn-Fixture-selected")]/'
            'parent::div/parent::div/div/div/'
            'div[contains(@class, "ipn-CompetitionButton_Text")]').text

        # Move to the "My Bets" screen.
        bet365move.my_bets()

        # Cash out function.
        bet365cashout = Bet365CashOut(self.driver)

        time.sleep(20)
        # Get basic game data.
        imm_data = bet365getdata.get_game_imm_data(league_name)

        # Register data in MongoDB.
        # bet365mongo = Bet365Mongo()
        # bet365mongo.insert_game_data(imm_data)

        goal_count = int(imm_data['how_to_bet'][-3:-2])

        while True:
            # Determine if you are betting.
            try:
                self.driver.find_element_by_class_name(
                    'hm-HeaderMenuItemMyBets_MyBetsCount')
            except:
                break

            # Get Detailed game data.
            var_data = bet365getdata.get_game_var_data()

            # Give detailed game data and judge whether cash out.
            process_status = bet365cashout.game_judgement(goal_count, var_data)

            if process_status != 0:
                time.sleep(process_status)
            elif process_status == 0:
                bet365cashout.cash_out()
                break

    def game_judgement(self, goal_count, var_data):
        status = goal_count - (
                int(var_data['scores'][0]) + int(var_data['scores'][1]))
        logging.info('Now status is {}'.format(status))
        if status == 3:
            return 300
        elif status == 2:
            return 180
        elif status == 1:
            return 60
        elif status == 0:
            return 0

    def cash_out(self):
        # cash out.
        self.driver.find_element_by_xpath(
            '//div[contains(@class, "myb-CloseBetButtonWithSlider")]/div/span/'
            'div/div[1]').click()