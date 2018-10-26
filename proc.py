
import numpy as np
import pandas as pd

from helper import *


periodscores = []
for period in range(maxperiod+1):
    periodscores.append(clean_teamgamelogs(
                        scrape_teamgamelogs(period),period))

data = join_periodscore(periodscores)

# results sanity check
assert data.shape[0] == 82* 30
assert np.array_equal((data['FUL'] * 2).values, data[list(periodname.values())].sum(axis = 1).values)


# output results to csv
data.to_csv('data/gamescores_2017_18.csv',index = False)

OT = [i for i in periodname.values() if 'OT' in i]

# due to nan ot and 2nd scores are float

data['1ST'] = data.QTR1 + data.QTR2
data['2ND'] = (data.QTR3 + data.QTR4 + data[OT].sum(axis = 1)).astype('int32')
data['REG'] = data.QTR1 + data.QTR2 + data.QTR3 + data.QTR4

data.to_csv('data/gamescores_2017_18_full.csv', index = False)

# generate avg score across nba per period.
period_avg = data[list(periodname.values()) + ['1ST','2ND','REG']].mean()
period_team = data.groupby(['TEAM_ID','TEAM_ABBREVIATION'])[list(periodname.values()) + ['1ST','2ND','REG']].mean()
factor = (period_team - period_avg).reset_index()
factor.to_csv('data/factor_2017_18.csv', index = False)
