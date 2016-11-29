#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

# Data Analysis Modules.

import pandas as pd
import seaborn as sns

# Database(SQL) Modules.

from sqlalchemy import Table, select, MetaData, create_engine

from sqlalchemy.engine import Connection
from sqlalchemy.sql import func, desc, case, cast
from sqlalchemy.sql.expression import join

# In[11]:

# Build up path from private variables.

DB_CRED = os.environ['DB_CRED']
DB_PATH = os.environ['DB_PATH']
DB_FULL = 'postgres://{cred}@{path}'.format(cred=DB_CRED, path=DB_PATH)

# Create engine & MetaData

db = create_engine(DB_FULL)
metadata = MetaData()

# Start table variables with capitals to prevent overwrite.

Game = Table('game', metadata, autoload=True, autoload_with=db)
Coord = Table('coord', metadata, autoload=True, autoload_with=db)
Account = Table('account', metadata, autoload=True, autoload_with=db)

# - Game Columns   : ['game.id', 'game.won', 'game.account_id']
# - Coord Columns  : ['coord.id', 'coord.cpu_coords', 'coord.acc_coords', 'coord.game_id']
# - Account Columns: ['account.id', 'account.user_name']

# Create common variables.

# Informative Columns.

Game_won = Game.columns.won.label('Won')
Account_un = Account.columns.user_name.label('User')

# Unique Identifiers.

Account_id = Account.columns.id
Game_account_id = Game.columns.account_id

# Joins

Account_game = join(Account, Game, Account_id == Game_Account_id)

# Create temp connection.

conn = db.connect()

# SELECT account.user_name as "User",
# SUM(CASE WHEN game.won = 't' THEN 1 ELSE 0 END) as "Won",
# SUM(CASE WHEN game.won = 'f' THEN 1 ELSE 0 END) as "Lost"
# FROM account
#   INNER JOIN game on account.id = game.account_id
#   GROUP BY account.user_name;

# Get user names.

stmt = select([
    Account_un, 
    func.sum(case([(Game_won == True, 1)], else_=0)).label('Won'), 
    func.sum(case([(Game_won == False, 1)], else_=0)).label('Lost'),
    func.count(Game_won).label('Played')
    ]).select_from(Account_game).group_by(Account_un)

# Run Query.

results = db.execute(stmt).fetchall()

# Close & remove connection.

conn.close()
db.dispose()

# Create DataFrame.

df = pd.DataFrame(data=results, columns=results[0].keys())
print(df.head())


# Organize Data

df.set_index('User', inplace=True)
df.sort_values('Won', ascending=False, inplace=True)


# Print top 5 winners.

print(df['Won'].head(5))


# Print top 5 losers.

print(df.sort_values('Lost', ascending=False)['Lost'].head(5))


# Create bargraph.

# Init matplotlib subplot.
fig, ax = plt.subplots(figsize=(8, 8))

# Plot total uer plays.
sns.set_color_codes('muted')
sns.barplot(x='Played', y=df.index.tolist(), data=df, label='Played.', color='b')

# Plot total user wins.

sns.set_color_codes('pastel')
sns.barplot(x='Won', y=df.index.tolist(), data=df, label='Won.', color='b')

# Set Informative.

ax.legend(ncol=2, loc=0, frameon=True)
ax.set_xlabel('Games')
ax.set_title('Wins And Games Played Per Person.')

sns.despine(left=True, bottom=True)

fig.savefig('user_wins.png', dpi=200)