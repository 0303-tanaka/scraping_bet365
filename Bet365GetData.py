import datetime
import logging


class Bet365GetData(object):
    def __init__(self, driver):
        self.driver = driver

    def get_jude_data(self):
        # Get time and scores from all game.
        all_game_data = {
            'team_names1': [],
            'team_names2': [],
            'time': [],
            'scores1': [],
            'scores2': [],
        }
        all_game_data['team_names1'] = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "ipn-Fixture_TeamStack")]/div[1]')
        all_game_data['team_names2'] = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "ipn-Fixture_TeamStack")]/div[2]')
        all_game_data['time'] = self.driver.find_elements_by_class_name(
            'ipn-Fixture_TimerContainer')
        all_game_data['scores1'] = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "ipn-ScoresDefault_Score")]/div[1]')
        all_game_data['scores2'] = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "ipn-ScoresDefault_Score")]/div[2]')
        return all_game_data

    def get_game_imm_data(self, league_name):
        # For cash out.
        # Get the immutable data of the match.
        imm_data = {
            'league_name': '',
            'team_names': ['', ''],
            'how_to_bet': '',
            'stack': '',
            'to_return': '',
            'date': '',
        }
        imm_data['league_name'] = league_name
        imm_data['team_names'][0] = self.driver.find_element_by_class_name(
            'ml1-SoccerScoreHeaderLegacy_Team1Name').text
        imm_data['team_names'][1] = self.driver.find_element_by_class_name(
            'ml1-SoccerScoreHeaderLegacy_Team2Name').text
        imm_data['how_to_bet'] = self.driver.find_element_by_class_name(
            'myb-BetParticipant_ParticipantSpan').text
        imm_data['stack'] = self.driver.find_element_by_class_name(
            'myd-MyBetsModuleDefault_BetInformationText').text
        imm_data['to_return'] = self.driver.find_element_by_class_name(
            'myb-OpenBetItemInnerView_BetInformationText').text
        imm_data['date'] = datetime.datetime.now()

        print(imm_data)
        return imm_data

    def get_game_var_data(self):
        # Get variable data of the a game.
        var_data = {
            'time': '',
            'scores': ['', ''],
            'attacks': ['', ''],
            'd_attacks': ['', ''],
            'possession': ['', ''],
            'on_target': ['', ''],
            'off_target': ['', ''],
            'c_kick': ['', ''],
            'y_card': ['', ''],
            'r_card': ['', ''],
            'pk': ['', ''],
        }

        # Stats data
        self.driver.find_element_by_class_name(
            'ml-StatButtons_Button-stats').click()
        var_data['time'] = self.driver.find_element_by_class_name(
            'ml1-SoccerClock_Clock').text
        var_data['scores'][0] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-SoccerScoreHeaderLegacy_Team1Name")]/'
            'following-sibling::div[1]').text
        var_data['scores'][1] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-SoccerScoreHeaderLegacy_Team2Name")]/'
            'preceding-sibling::div').text

        # Attacks/Dangerous Attacks/Possession
        ADP1 = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "ml-WheelChart_Team1Text")]')
        ADP2 = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "ml-WheelChart_Team2Text")]')
        try:
            var_data['attacks'][0] = ADP1[0].text
            var_data['attacks'][1] = ADP2[0].text
            var_data['d_attacks'][0] = ADP1[1].text
            var_data['d_attacks'][1] = ADP2[1].text
            var_data['possession'][0] = ADP1[2].text
            var_data['possession'][1] = ADP2[2].text
        except IndexError:
            logging.warning(
                'This game is not data(Attacks/Dangerous Attacks/Possession)')

        # On Target/Off target
        onT = self.driver.find_elements_by_xpath(
            '//b[contains(@class, "ml-ProgressBar_MiniBarValue-1")]')
        offT = self.driver.find_elements_by_xpath(
            '//b[contains(@class, "ml-ProgressBar_MiniBarValue-2")]')
        var_data['on_target'][0] = onT[0].text
        var_data['off_target'][0] = offT[0].text
        var_data['on_target'][1] = onT[1].text
        var_data['off_target'][1] = offT[1].text

        # Summary data
        self.driver.find_element_by_class_name(
            'ml-StatButtons_Button-summary').click()
        var_data['c_kick'][0] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-StatBoardColumn_Icon-2")]/'
            'following-sibling::div[1]').text
        var_data['c_kick'][1] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-StatBoardColumn_Icon-2")]/'
            'following-sibling::div[2]').text
        var_data['y_card'][0] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-StatBoardColumn_Icon-3")]/'
            'following-sibling::div[1]').text
        var_data['y_card'][1] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-StatBoardColumn_Icon-3")]/'
            'following-sibling::div[2]').text
        var_data['r_card'][0] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-StatBoardColumn_Icon-4")]/'
            'following-sibling::div[1]').text
        var_data['r_card'][1] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-StatBoardColumn_Icon-4")]/'
            'following-sibling::div[2]').text
        var_data['pk'][0] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-StatBoardColumn_Icon-8")]/'
            'following-sibling::div[1]').text
        var_data['pk'][1] = self.driver.find_element_by_xpath(
            '//div[contains(@class, "ml1-StatBoardColumn_Icon-8")]/'
            'following-sibling::div[2]').text

        print(var_data)
        return var_data