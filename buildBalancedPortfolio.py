import Trading_Bot.allCompanies as ac
import yfinance as yf
from datetime import date, timedelta

equity_allocation = 80
debt_allocation = 100 - equity_allocation

industries = {1: 'Basic Materials',
              2: 'Financial Services',
              3: 'Industrials',
              4: 'Technology',
              5: 'Energy',
              6: 'Healthcare',
              7: 'Consumer Cyclical',
              8: 'Utilities',
              9: 'Consumer Defensive',
              10: 'Communication Services',
              11: 'Real Estate'}

industry_choice = {7: 40,
                   5: 35,
                   8: 15,
                   2: 10
                   }

industry_driver = False

# ... Large, Mid, Small

if industry_driver:
    cap_choice = {
        1: 100,
    }
else:
    cap_choice = {
        1: 55,
        2: 20,
        3: 25
    }

portfolio_value = 1000000
portfolio_raw = {
    'equity': {},
    'debt': {}
}

debt_amount = portfolio_value * (debt_allocation / 100)

tot = 0

for i in range(4):
    tot += ac.rank[ac.rank_2[i]]

for j in range(4):
    df = yf.download(ac.rank_2[j] + '.NS', start=date.today() + timedelta(-30), end=date.today())

    share = ac.rank[ac.rank_2[j]] / tot
    amt = debt_amount * share
    units = int(amt / df.iloc[len(df) - 1]['Close'])
    debt_amount -= amt
    portfolio_raw['debt'][ac.rank_2[j]] = units

equity_amount = portfolio_value * (equity_allocation / 100)

# ind_wise_amt_alloc = {}

for i in industry_choice:
    portfolio_raw['equity'][i] = {}
    amt = equity_amount * (industry_choice[i] / 100)

    for j in cap_choice:

        amt_cap = amt * (cap_choice[j] / 100)

        sc = 0  # Used to parse stocks.
        totl = {}
        totm = {}
        tots = {}
        totlr = 0
        totmr = 0
        totsr = 0
        for k in range(5):
            if j == 1:
                if sc >= len(ac.mc_bysec[industries[i]]):
                    print(
                        f'One of more companies of industry {industries[i]} and cap category {j} did not satisfy our conditions. We move ahead. Funds will be divided among other caps.')
                    continue
                df = yf.download(ac.lc_bysec[industries[i]][sc] + '.NS', start=date.today() + timedelta(-30),
                                 end=date.today())
                ratio = df.iloc[len(df) - 1]['Close'] / df.iloc[0]['Close']
                if ratio > 1.03:
                    totl[ac.lc_bysec[industries[i]][sc]] = ratio
                    totlr += ratio
                    sc += 1
                else:
                    sc += 1
                    k -= 1
            elif j == 2:
                if sc >= len(ac.mc_bysec[industries[i]]):
                    print(
                        f'One of more companies of industry {industries[i]} and cap category {j} did not satisfy our conditions. We move ahead. Funds will be divided among other caps.')
                    continue
                df = yf.download(ac.mc_bysec[industries[i]][sc] + '.NS', start=date.today() + timedelta(-30),
                                 end=date.today())
                ratio = df.iloc[len(df) - 1]['Close'] / df.iloc[0]['Close']
                if ratio > 1.03:
                    totm[ac.mc_bysec[industries[i]][sc]] = ratio
                    totmr += ratio
                    sc += 1

                else:
                    sc += 1
                    k -= 1
            elif j == 3:
                if sc >= len(ac.mc_bysec[industries[i]]):
                    print(
                        f'One of more companies of industry {industries[i]} and cap category {j} did not satisfy our conditions. We move ahead. Funds will be divided among other caps.')
                    continue
                df = yf.download(ac.sc_bysec[industries[i]][sc] + '.NS', start=date.today() + timedelta(-30),
                                 end=date.today())
                ratio = df.iloc[len(df) - 1]['Close'] / df.iloc[0]['Close']
                if ratio > 1.05:
                    tots[ac.sc_bysec[industries[i]][sc]] = ratio
                    totsr += ratio
                    sc += 1
                else:
                    sc += 1
                    k -= 1

        if j == 1:
            portfolio_raw['equity'][i]['LCAP'] = {}
            for k in totl:
                checker = False
                amt_sh = amt_cap * (totl[k] / totlr)
                df = yf.download(k + '.NS', start=date.today(), end=date.today())
                if df.isnull:
                    df = yf.download(k + '.NS', start=date.today() + timedelta(-1), end=date.today())

                if checker:
                    units = int(amt_sh / df.iloc[0]['Close'])
                else:
                    units = int(amt_sh / df['Close'])

                portfolio_raw['equity'][i]['LCAP'][k] = units
                amt_cap -= amt_sh

        if j == 2:
            portfolio_raw['equity'][i]['MCAP'] = {}
            for k in totm:
                checker = False
                amt_sh = amt_cap * (totm[k] / totmr)
                df = yf.download(k + '.NS', start=date.today(), end=date.today())
                if df.isnull:
                    checker = True
                    df = yf.download(k + '.NS', start=date.today() + timedelta(-1), end=date.today())

                if checker:
                    units = int(amt_sh / df.iloc[0]['Close'])
                else:
                    units = int(amt_sh / df['Close'])

                portfolio_raw['equity'][i]['MCAP'][k] = units
                amt_cap -= amt_sh

        if j == 3:
            portfolio_raw['equity'][i]['SCAP'] = {}
            for k in tots:
                checker = False
                amt_sh = amt_cap * (tots[k] / totsr)
                df = yf.download(k + '.NS', start=date.today(), end=date.today())
                if df.isnull:
                    checker = True
                    df = yf.download(k + '.NS', start=date.today() + timedelta(-1), end=date.today())
                if checker:
                    units = int(amt_sh / df.iloc[0]['Close'])
                else:
                    units = int(amt_sh / df['Close'])
                portfolio_raw['equity'][i]['SCAP'][k] = units
                amt_cap -= amt_sh


def get_port_return(port):
    port_val_s = 0
    port_val_e = 0

    for i in port:

        if i == 'debt':
            for m in port[i]:
                df = yf.download(m + '.NS', start=date.today() + timedelta(-60),
                                 end=date.today())
                port_val_s += port[i][m] * df.iloc[0]['Close']
                port_val_e += port[i][m] * df.iloc[len(df) - 1]['Close']
            break

        for j in port[i]:

            for k in port[i][j]:

                for l in port[i][j][k]:
                    df = yf.download(l + '.NS', start=date.today() + timedelta(-60),
                                     end=date.today())
                    port_val_s += port[i][j][k][l] * df.iloc[0]['Close']
                    port_val_e += port[i][j][k][l] * df.iloc[len(df) - 1]['Close']

    print(f'Portfolio grew by {(((port_val_e / port_val_s) - 1) * 100):.2f}%')


for i in portfolio_raw:
    print(f'{i} : {portfolio_raw[i]}')

get_port_return(portfolio_raw)
