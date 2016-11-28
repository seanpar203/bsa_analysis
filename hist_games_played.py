
# coding: utf-8

# # *Histogram on average games played.*

# #### Imports.

# In[17]:

import os

# Data Analysis Modules.
import pandas as pd
import seaborn as sns

# Database(SQL) Modules.
from sqlalchemy import(
    Table,
    select,
    MetaData,
    create_engine,
) 
from sqlalchemy.engine import Connection
from sqlalchemy.sql import func, desc, case, cast
from sqlalchemy.sql.expression import join


# #### DB Access Connection

# In[10]:

# Build up path from private variables.
DB_CRED = os.environ['DB_CRED']
DB_PATH = os.environ['DB_PATH']
DB_FULL = 'postgres://{cred}@{path}'.format(cred=DB_CRED, path=DB_PATH)


# In[11]:

# Create engine & MetaData 
db = create_engine(DB_FULL)
metadata = MetaData()


# #### Reflect tables.

# In[6]:

# Start table variables with capitals to prevent overwrite. 
Game = Table('game', metadata, autoload=True, autoload_with=db)
Coord = Table('coord', metadata, autoload=True, autoload_with=db)
Account = Table('account', metadata, autoload=True, autoload_with=db)


# #### Table information

# - Game Columns   : ['game.id', 'game.won', 'game.account_id']
# - Coord Columns  : ['coord.id', 'coord.cpu_coords', 'coord.acc_coords', 'coord.game_id']
# - Account Columns: ['account.id', 'account.user_name']

# #### Show a list of all users & related games.

# In[78]:

# Create temp connection.
conn = db.connect()

# Get user names.
account_game = join(
    Account, Game,
    Account.columns.id == Game.columns.account_id
)
user_name = Account.columns.user_name.label('User')
game_won = Game.columns.won.label('Played')

stmt = select([user_name, game_won]).select_from(account_game)
result = db.execute(stmt).fetchall()

# Close & remove connection.
conn.close()
db.dispose()


# #### Create DataFrame from result.

# In[79]:

df = pd.DataFrame(data=result, columns=result[0].keys())
print(df.head())


# #### Show User occurances.

# In[80]:

# Damn I played alot...
print(df['User'].value_counts())


# #### Histogram graph shows that most users played between 1-10 times.

# In[91]:

# Create Histogram.
ax = sns.distplot(df.groupby('User').count()['Played'])
ax.set_title('Numer of Games Played By Users.')

# Get & save figure.
fig = ax.get_figure()
fig.savefig('hist_games_played.png', dpi=200)


# In[ ]:



