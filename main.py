from lib.handler import PlayerHandler, MatchHandler
from datetime import datetime


def clean_date(timestamp):
    timestamp = int(str(timestamp)[0:10])
    date_time = datetime.fromtimestamp(timestamp)
    return date_time.strftime("%d/%m/%y, %H:%M")


def main():
    p = PlayerHandler('kucasp')
    last_match = p.get_last_match('Fail')

    print(last_match)
    print(last_match.get_player_status(p.account_id))

    # print('Últimos 10 jogos\n')
    # for match in p.match_list['matches'][0:4]:
    #     print('Data: %s' % clean_date(match['timestamp']))
    #     m = MatchHandler(match['gameId'])
    #     print(m.get_player_status(p.account_id))
    #     print('\n')


if __name__ == "__main__":
    main()