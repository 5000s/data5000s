from typing import Any, Dict
import pandas as pd
from tabulate import tabulate
import os


def extract_excel(
    file_name: str, sheet_name: str, columns: Dict[str, Any]
) -> pd.DataFrame:
    print(f"{file_name = } {sheet_name = }")
    if not os.path.exists(file_name):
        raise FileNotFoundError
    excel_df = pd.read_excel(file_name, sheet_name=sheet_name)

    renamed_df = excel_df.rename(columns=columns)

    print(renamed_df.columns)
    df_info = tabulate(renamed_df.head(), headers="keys", tablefmt="psql")
    print(df_info)
    return renamed_df
