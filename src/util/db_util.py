from typing import Any, Dict
import sqlalchemy as sa
import pymysql
import pandas as pd

def pandas_to_mysql(df: pd.DataFrame, schema: str,table_name: str) -> None:
    host="xxx"
    # port="3306"
    user="sra"
    pwd="xxx"
    sql_engine= sa.create_engine(f"mysql+pymysql://{user}:{pwd}@{host}:3306",pool_recycle=3600)
    db_connection = sql_engine.connect()
    try:
        df.to_sql(table_name, db_connection, if_exists="replace", index=False, schema=schema)        
    except Exception as ex:
        print(ex)
        raise
    else: 
        print("load Table ")
    finally:
        db_connection.close()



