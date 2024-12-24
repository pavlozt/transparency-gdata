import pandas as pd
import logging

def read_data(file_name, sheet_name='raw_data'):
    try:
        df =  pd.read_excel(file_name, sheet_name=sheet_name)
    except ValueError as e:
        logging.warning(e)
        return pd.DataFrame()
    except FileNotFoundError as e:
        logging.warning(e)
        logging.warning(f"Will create new file {file_name}")
        return pd.DataFrame()
    return df



def write_data(file_name, df, sheet_name='raw_data'):
    with pd.ExcelWriter(file_name, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

