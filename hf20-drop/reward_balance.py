# Script by @flugschwein on GitHub and Steem
import requests
from matplotlib import pyplot as plt
from dateutil.parser import parse
import datetime

funds = requests.get('https://steemdb.com/api/funds').json()
for e in funds:
    e['last_update'] = parse(e['last_update'])

funds = sorted(funds, key=lambda x: x['last_update'])
now = datetime.datetime.now()
start = now - datetime.timedelta(days=7)
date = []
balance = []
recent_claims = []
for e in funds:
    if e['last_update'] < start:
        continue
    date.append(e['last_update'])
    balance.append(e['reward_balance'])
    recent_claims.append(e['recent_claims'])
plt.plot(date, balance, color='r')
plt.title('Recent Claims and Reward Balance - Last 450 days')
plt.xlabel('Date')
plt.ylabel('Reward Balance', color='r')
plt.yticks(color='r')
plt.twinx()
plt.plot(date, recent_claims, color='b')
plt.ylabel('Recent Claims', color='b')
plt.yticks(color='b')
plt.show()
