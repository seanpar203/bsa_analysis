
# coding: utf-8

# # *List of users.* 

# #### Imports.

import os

# Database(SQL) Modules.
from sqlalchemy import(
    Table,
    select,
    MetaData,
    create_engine,
) 


# #### DB Access Connection

# Build up path from private variables.
DB_CRED = os.environ['DB_CRED']
DB_PATH = os.environ['DB_PATH']
DB_FULL = 'postgres://{cred}@{path}'.format(cred=DB_CRED, path=DB_PATH)


# Create engine & MetaData 
db = create_engine(DB_FULL)
metadata = MetaData()


# #### List & Reflect tables.
print(db.table_names())


# Start table variables with capitals to prevent overwrite. 
Game = Table('game', metadata, autoload=True, autoload_with=db)
Coord = Table('coord', metadata, autoload=True, autoload_with=db)
Account = Table('account', metadata, autoload=True, autoload_with=db)


# #### Show table information

print('Game Columns   : {columns}'.format(columns=Game.columns))
print('Coord Columns  : {columns}'.format(columns=Coord.columns))
print('Account Columns: {columns}'.format(columns=Account.columns))


# #### Show a list of all users.

# Create temp connection.
conn = db.connect()

# Get user names.
stmt = select([Account.columns.user_name])
result = db.execute(stmt).fetchall()

# Close & remove connection.
conn.close()
db.dispose()

print(result)
