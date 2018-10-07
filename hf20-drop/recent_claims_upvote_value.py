# Script by @flugschwein on GitHub and Steem
import datetime
import matplotlib.pyplot as plt
import requests
from dateutil.parser import parse
from beem.amount import Amount
from beem.steem import Steem
from beem.instance import set_shared_steem_instance, shared_steem_instance
from beem.price import Price


def get_median_price(steem_price: int):
    """ Returns the current median history price as Price
    Also copied from beem and minor edits added
    """
    a = Price(
        None,
        base=Amount(steem_price, 'SBD'),
        quote=Amount(1, 'STEEM')
    )
    return a.as_base("SBD")


def get_sbd_per_rshares(reward_balance, recent_claims, date, not_broadcasted_vote_rshares=0):
    """ Returns the current rshares to SBD ratio
    Credit to beem. Nearly complete copy paste.
    """
    reward_balance = Amount(reward_balance, 'STEEM').amount
    recent_claims = float(recent_claims) + not_broadcasted_vote_rshares

    fund_per_share = reward_balance / (recent_claims)
    steem_price = requests.get(
        date.strftime('https://api.coingecko.com/api/v3/coins/steem/history?date=%d-%m-%Y')).json()
    global coingecko_count
    coingecko_count += 1
    median_price = get_median_price(steem_price['market_data']['current_price']['usd'])
    SBD_price = (median_price * Amount(1, "STEEM")).amount
    return (fund_per_share * SBD_price, steem_price['market_data']['current_price']['usd'])


funds = requests.get('https://steemdb.com/api/funds')
funds = funds.json()
stm = Steem()
set_shared_steem_instance(stm)
coingecko_count = 0

for e in funds:
    e['last_update'] = parse(e['last_update'])

funds = sorted(funds, key=lambda x: x['last_update'])

for count, d in enumerate([7, 14, 30, 90, 150, 450]):
    print(f'{d} days')
    date = []
    recent_claims = []
    upvote_value = []
    stm_price = []
    start = datetime.datetime.now() - datetime.timedelta(days=d)
    for e in funds:
        if e['last_update'] < start:
            continue
        else:
            date.append(e['last_update'])
            recent_claims.append(e['recent_claims'])

            rshares = stm.vests_to_rshares(stm.sp_to_vests(10000, e['last_update']))
            sbd_per_rshares, steem_price = get_sbd_per_rshares(e['reward_balance'], e['recent_claims'], e['last_update'])
            upvote_value.append(rshares * sbd_per_rshares)
            stm_price.append(steem_price)

    plt.subplot(3, 2, count + 1)
    plt.plot(date, recent_claims, 'b-', label='recent_claims')
    plt.title(f'Recent Claims and corresponding Upvote Value of the last {d} days')
    plt.ylabel('rshares', color='b')
    plt.tick_params('y', colors='b')
    plt.xlabel('Date')
    plt.legend(loc='center left')
    plt.twinx()
    plt.plot(date, upvote_value, 'r-', label='Upvote Value')
    plt.plot(date, stm_price, 'g-', label='Steem Price')
    plt.ylabel('STU/USD', color='r')
    plt.tick_params('y', colors='g')
    plt.legend(loc='center right')

plt.show()
