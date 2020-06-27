import json
import logging
import os
import time

from Bet365Mongo import *

UNDER_TIME = 58
ABOVE_TIME = 70
# UNDER_TIME = 0
# ABOVE_TIME = 90


class Bet365AMG(object):
    favorite_flag = '0'

    def __init__(self, driver):
        self.driver = driver

    def find_game_bet(self, judg_data):
        # Find a game to bet and notify.
        bet_count = 0
        bet_games = []
        for i in range(len(judg_data['time'])):
            game_data = {
                'how_to_bet': '',
                'team_names': [],
                'time': '',
                'scores': [],
            }
            select_box = judg_data['time'][i]
            time = int(judg_data['time'][i].text[:2])
            score1 = int(judg_data['scores1'][i].text)
            score2 = int(judg_data['scores2'][i].text)

            if (UNDER_TIME <= time <= ABOVE_TIME):
                if ((score1 + score2 <= 3) and
                    (score1 != 3 or score2 != 3) and
                    self.find_alternative(select_box)):
                    # Alternative Match Goals
                    game_data['how_to_bet'] = 'AMG'
                    game_data['team_names'] =\
                        judg_data['team_names1'][i].text,\
                        judg_data['team_names2'][i].text
                    game_data['time'] = judg_data['time'][i].text
                    game_data['scores'] = score1, score2
                    bet_count += 1
                    bet_games.append(game_data)
                elif (abs(score1 - score2) >= 2):
                    # Fulltime Result
                    game_data['how_to_bet'] = 'FR'
                    game_data['team_names'] =\
                        judg_data['team_names1'][i].text,\
                        judg_data['team_names2'][i].text
                    game_data['time'] = judg_data['time'][i].text
                    game_data['scores'] = score1, score2
                    bet_count += 1
                    bet_games.append(game_data)

        if bet_count > 0:
            print(json.dumps(bet_games, indent=4))
            os.system('play -n synth 1 sin 3500')
            logging.info('bet game is {}'.format(bet_count))
        else:
            logging.info('No games can be bet.')

    def find_alternative(self, select_box):
        select_box.click()
        time.sleep(2)
        try:
            self.driver.find_element_by_xpath(
                '//div[contains(text(), "Alternative Match Goals")]')
            if (Bet365AMG.favorite_flag == '0'):
                self.driver.find_element_by_xpath(
                    '//div[contains(text(), "Alternative Match Goals")]/'
                    'following-sibling::div[1]').click()
                logging.info('Selected your favorite button.')
                Bet365AMG.favorite_flag = '1'
            return True
        except:
            return False