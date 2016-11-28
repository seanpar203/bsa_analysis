
# coding: utf-8

"""  List of users.

Notes:
	This script shows the steps taken to access
	a remote AWS EC2 instance Postgres database
	and run a simple query to get all users.
"""

# Imports
import os

# Database(SQL) Modules
from sqlalchemy import(
    Table,
    select,
    MetaData,
    create_engine,
) 


# DB Access Connection

# Build up path from private variables.
DB_CRED = os.environ['DB_CRED']
DB_PATH = os.environ['DB_PATH']
DB_FULL = 'postgres://{cred}@{path}'.format(cred=DB_CRED, path=DB_PATH)


# Create engine & MetaData 
db = create_engine(DB_FULL)
metadata = MetaData()


# List & Reflect tables

# ['account', 'game', 'coord']

# Start table variables with capitals to prevent overwrite. 
Game = Table('game', metadata, autoload=True, autoload_with=db)
Coord = Table('coord', metadata, autoload=True, autoload_with=db)
Account = Table('account', metadata, autoload=True, autoload_with=db)


# Table information

""" 
- Game Columns   : ['game.id', 'game.won', 'game.account_id']
- Coord Columns  : ['coord.id', 'coord.cpu_coords', 'coord.acc_coords', 'coord.game_id']
- Account Columns: ['account.id', 'account.user_name']
"""


# Show a list of all users

""" Raw SQL Query.

SELECT account.user_name 
from account; 
"""

# Create tmp connection.
conn = db.connect()

# Get user names.
stmt = select([Account.columns.user_name])
result = db.execute(stmt).fetchall()

# Close & remove connection
conn.close()
db.dispose()

print(result)
