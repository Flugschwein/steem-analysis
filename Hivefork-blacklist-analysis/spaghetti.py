from pprint import pprint
import matplotlib.pyplot as plt
from beem.steem import Steem
from beem.block import Block
from beem.amount import Amount
from beem.instance import set_shared_steem_instance

hive = Steem('https://api.hive.blog')
set_shared_steem_instance(hive)

blk = Block(41818752, steem_instance=hive, only_virtual_ops=True)

errors = [
    "akiroq",
    "balticbadger",
    "dailychina",
    "dailystats",
    "dftba",
    "double-u",
    "edgarare1",
    "electrodo",
    "fadetoblack",
    "freedompoint",
    "friendlystranger",
    "john371911",
    "juancar347",
    "kdtkaren",
    "lichtblick",
    "lifeskills-tv",
    "lotusfleur",
    "ricko66",
    "rynow",
    "scottcbusiness",
    "seo-boss",
    "sgbonus",
    "spoke",
    "steemchiller",
    "steemflower",
    "stimp1024",
    "travelnepal",
    "truce",
    "tuckerjtruman",
    "wisdomandjustice",
    "yanirauseche"
]

steemit = [
    "ben",
    "bitdev100",
    "geos",
    "goku1",
    "hkdev404",
    "imadev",
    "joe767676",
    "misterdelegation",
    "steem",
    "steemit",
    "steemit2",
    "steemitadmin",
    "timothy2020",
    "steemitblog",
    "goodguy24",  # puppets
    "aheadofslow",
    "night11pm",
    "hunger365",
    "waitforyou1",
    "cloudysun",
    "jumphigh",
    "coronashallgo",
    "paintingclub",
    "bostonawesome",
    "toke2049",
    "flyingfly1",
    "agirl10000",
    "eastooowest",
    "car2001",
    "nicetry001",
    "high46",
    "paintingclub",
    "respect888",
    "happylife123"
]

exchanges = [
    'poloniex'
]

vest_sum = None
hive_sum = None
hbd_sum = None
total_hive_sum = None
sums = {'Errors': {'vest sum': None,
                   'hive sum': None,
                   'hbd sum': None,
                   'total hive sum': None},
        'Steemit': {'vest sum': None,
                    'hive sum': None,
                    'hbd sum': None,
                    'total hive sum': None},
        'Exchanges': {'vest sum': None,
                      'hive sum': None,
                      'hbd sum': None,
                      'total hive sum': None},
        'Others': {'vest sum': None,
                   'hive sum': None,
                   'hbd sum': None,
                   'total hive sum': None},
        }

accounts = ()
vests = ()
hives = ()
hbd = ()
hive_converted = ()

for op in blk.operations:
    if op['op']['type'] != 'hardfork_hive_operation':
        continue
    if op['op']['value']['account'] in errors:
        mode = 'Errors'
    elif op['op']['value']['account'] in steemit:
        mode = 'Steemit'
    elif op['op']['value']['account'] in exchanges:
        mode = 'Exchanges'
    else:
        mode = 'Others'

    if mode == 'Errors':
        accounts += ('@' + op['op']['value']['account'],)
        vests += (Amount(op['op']['value']['vests_converted']).amount,)
        hives += (Amount(op['op']['value']['sbd_transferred']).amount,)
        hbd += (Amount(op['op']['value']['steem_transferred']).amount,)
        hive_converted += (Amount(op['op']['value']['total_steem_from_vests']).amount,)
        print(
            f"|@{op['op']['value']['account']}|{str(Amount(op['op']['value']['steem_transferred']).amount)}|{str(Amount(op['op']['value']['sbd_transferred']).amount)}|{str(Amount(op['op']['value']['vests_converted']).amount)}|{str(Amount(op['op']['value']['total_steem_from_vests']).amount)}|")

    if sums[mode]['vest sum'] is None:
        sums[mode]['vest sum'] = Amount(op['op']['value']['vests_converted'])
    else:
        sums[mode]['vest sum'] += Amount(op['op']['value']['vests_converted'])

    if sums[mode]['hive sum'] is None:
        sums[mode]['hive sum'] = Amount(op['op']['value']['sbd_transferred'])
    else:
        sums[mode]['hive sum'] += Amount(op['op']['value']['sbd_transferred'])

    if sums[mode]['hbd sum'] is None:
        sums[mode]['hbd sum'] = Amount(op['op']['value']['steem_transferred'])
    else:
        sums[mode]['hbd sum'] += Amount(op['op']['value']['steem_transferred'])

    if sums[mode]['total hive sum'] is None:
        sums[mode]['total hive sum'] = Amount(op['op']['value']['total_steem_from_vests'])
    else:
        sums[mode]['total hive sum'] += Amount(op['op']['value']['total_steem_from_vests'])

pprint(sums)

plt.figure(figsize=[6.5, 15], dpi=150)
plt.subplot(2, 3, 1)
plt.barh(accounts, hives)
plt.gca().invert_yaxis()
plt.grid(True, 'both', 'x')
plt.xlabel('Steem')
plt.title('Steem removed')

plt.subplot(2, 3, 3)
plt.barh(accounts, hbd)
plt.gca().invert_yaxis()
plt.grid(True, 'both', 'x')
plt.xlabel('SBD')
plt.title('SBD removed')

plt.subplot(2, 3, 4)
plt.barh(accounts, vests)
plt.gca().invert_yaxis()
plt.grid(True, 'both', 'x')
plt.xlabel('Vests')
plt.title('Vests removed')

plt.subplot(2, 3, 6)
plt.barh(accounts, hive_converted)
plt.gca().invert_yaxis()
plt.grid(True, 'both', 'x')
plt.xlabel('Steem')
plt.title('Vests removed (in Steem)')
plt.show()

plt.figure(figsize=[7, 15], dpi=150)
plt.suptitle('Assets moved to @steem.dao (all in Steem)')

plt.subplot(1, 2, 1)
hbd_as_hive = sums['Errors']['hbd sum'] * hive.get_median_price().invert()
plt.title('Linear scale')
plt.bar('Assets', sums['Errors']['total hive sum'].amount, label='Vests')
plt.bar('Assets', sums['Errors']['hive sum'].amount, label='Steem')
plt.bar('Assets', hbd_as_hive.amount, label='SBD')

plt.subplot(1, 2, 2)
hbd_as_hive = sums['Errors']['hbd sum'] * hive.get_median_price().invert()
plt.title('Logarithmic scale')
plt.bar('Assets', sums['Errors']['total hive sum'].amount, label='Vests')
plt.bar('Assets', sums['Errors']['hive sum'].amount, label='Steem')
plt.bar('Assets', hbd_as_hive.amount, label='SBD', bottom=0)
plt.gca().set_yscale('log')
plt.legend()
plt.show()

plt.figure(figsize=[7, 15], dpi=200)
plt.suptitle('Total blacklisted funds')
plt.subplot(1, 2, 1)
labels = ["SBD", 'Steem', 'Vests']
plt.title('Linear scale')
for i in ['Steemit', 'Exchanges', 'Others', 'Errors']:
    values = [
        (sums[i]['hbd sum'] * hive.get_median_price().invert()).amount,
        sums[i]['hive sum'].amount,
        sums[i]['total hive sum'].amount,
    ]
    plt.bar(labels, values, label=i)
plt.legend()

plt.subplot(1, 2, 2)
labels = ["SBD", 'Steem', 'Vests']
plt.title('Logarithmic scale')
for i in ['Steemit', 'Exchanges', 'Others', 'Errors']:
    values = [
        (sums[i]['hbd sum'] * hive.get_median_price().invert()).amount,
        sums[i]['hive sum'].amount,
        sums[i]['total hive sum'].amount,
    ]
    plt.bar(labels, values, label=i)
plt.gca().set_yscale('log')

plt.show()

hbd_all = Amount(0, 'HBD')
hive_all = Amount(0, 'HIVE')
vest_all = Amount(0, 'VESTS')
total_hive_all = Amount(0, 'HIVE')

for m in ['Steemit', 'Errors', 'Others', 'Exchanges']:
    hbd_all += sums[m]['hbd sum']
    hive_all += sums[m]['hive sum']
    vest_all += sums[m]['vest sum']
    total_hive_all += sums[m]['total hive sum']

for i in [hbd_all, hive_all, vest_all, total_hive_all]:
    print(i)

complete_sum = hive_all + total_hive_all + hbd_all * hive.get_median_price().invert()
print(complete_sum)
