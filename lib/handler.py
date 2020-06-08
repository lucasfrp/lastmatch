from abc import ABC
from datetime import datetime
import requests
import json


class BasicHandler(ABC):

    def __init__(self):
        self.config = json.load(open('lib/config.json'))
        self.champions = json.load(open('lib/champion.json', encoding="utf8"))
        self.headers = {'X-Riot-Token': self.config['X-Riot-Token']}
        self.api_url = self.config['api_url']

    def call_api(self, url):
        print(url)
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_champion(self, champion_id):
        for champion in self.champions['data'].values():
            if str(champion['key']) == str(champion_id):
                return champion

    def get_champion_name(self, champion_id):
        champion = self.get_champion(champion_id)
        return champion['name']


class PlayerHandler(BasicHandler):

    def __init__(self, name):
        super(PlayerHandler, self).__init__()
        self.player_by_name_url = self.api_url + self.config['player_by_name_url'] + name
        self.match_list_by_account_url = self.api_url + self.config['match_list_by_account'] + '%s'
        self.player_values = {}
        self.match_list_values = {}
        self.get_player_values()

    def get_player_values(self):
        self.player_values = self.call_api(self.player_by_name_url)

    @property
    def account_id(self):
        return self.player_values['accountId']

    @property
    def match_list(self):
        if not self.match_list_values:
            self.match_list_values = self.call_api(self.match_list_by_account_url % self.account_id)

        return self.match_list_values

    def get_last_match(self, win=None):

        for match in self.match_list['matches']:
            m = MatchHandler(match['gameId'])

            if not win:
                return m

            if m.get_player_status(self.account_id)['win'] == win:
                return m


class MatchHandler(BasicHandler):

    def __init__(self, match_id):
        super(MatchHandler, self).__init__()
        self.match_id = str(match_id)
        self.match_by_id_url = self.api_url + self.config['match_by_id'] + self.match_id
        self.match_values = self.get_match_values()
        self.winning_team_value = None
        self.participants_value = None

    @property
    def winning_team(self):
        if not self.winning_team_value:
            self.winning_team_value = self.get_winning_team()

        return self.winning_team_value

    @property
    def participants(self):
        if not self.participants_value:
            self.participants_value = self.get_team_participants()

        return self.participants_value

    def get_match_values(self):
        return self.call_api(self.match_by_id_url)

    def get_team_participants(self):
        participants = {}

        for player in self.match_values['participantIdentities']:
            player_id = player['participantId']
            participants[player_id] = {'gameCreation': self.match_values['gameCreation']}
            participants[player_id]['playerId'] = player_id
            participants[player_id]['accountId'] = player['player']['accountId']
            participants[player_id]['summonerName'] = player['player']['summonerName']
            participants[player_id]['summonerId'] = player['player']['summonerId']

        for player in self.match_values['participants']:
            player_id = player['participantId']
            participants[player_id]['teamId'] = player['teamId']
            participants[player_id]['championId'] = player['championId']
            participants[player_id]['championName'] = self.get_champion_name(player['championId'])
            participants[player_id]['kills'] = player['stats']['kills']
            participants[player_id]['deaths'] = player['stats']['deaths']
            participants[player_id]['assists'] = player['stats']['assists']
            participants[player_id]['win'] = 'Win' if player['teamId'] == self.winning_team else 'Fail'

        return participants

    def get_winning_team(self):
        for team in self.match_values['teams']:
            if team['win'] == 'Win':
                return team['teamId']

    def get_player_status(self, account_id):
        for player in self.participants:

            if self.participants[player]['accountId'] == account_id:
                return self.participants[player]

        return

    def __str__(self):
        return 'Mode: %s | Winning Team: %s' % (self.match_values['gameMode'], self.winning_team)