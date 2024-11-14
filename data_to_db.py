import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text


engine = create_engine("postgresql:#################")

df = pd.read_csv("route/players_data.csv")
df.to_sql('player_data', engine, if_exists='replace', index=False)

print("Initial CSV data successfully loaded into the database.")

def update_stats():
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE player_data RESTART IDENTITY;"))
        
    new_df = pd.read_csv("route/players_data.csv")
    new_df.to_sql('player_data', engine, if_exists='append', index=False)
    
    print("Table player_data updated with the latest CSV data.")

update_stats()
