"""
This is the demo code that uses hydra to access the parameters in under the directory config.

Author: Krisorn Chunhapongpipat
"""

import hydra
from omegaconf import DictConfig

from extractor.excel_extractor import extract_excel
from util.db_util import pandas_to_mysql


@hydra.main(config_path="../config", config_name="main", version_base=None)
def process_data(config: DictConfig):
    """Function to process the data"""

    print(f"Process data using {config.data.raw}")
    print(f"{config.process.sheet_name = }")
    columns = {
        "ID": "id",
        "ID Link": "id_link",
        "Member Status": "new_status",
        "เลขที่สมาชิก": "member_number",
        "ประเภทสมาชิก": "member_type",
        "คำนำหน้า": "pre_name",
        "ชื่อ - นามสกุล": "first_last_name",
        "Tel": "tel_raw",
        "ที่อยู่": "address",
        "แขวง/ตำบล เขต/อำเภอ": "subdistrict",
        "จังหวัด": "province",
        "รหัสไปรษณีย์": "postal",
        "Zone": "zone",
        "Tel 2": "tel_2",
        "Magazine Type": "magazine_type",
        "จำนวนเล่ม": "amount_of_book",
        "Email": "email",
        "FB": "facebook",
        "รูปแบบจัดส่ง": "delivery_method",
        "ช่องทางสมัตร": "register_method",
        "Start MM/YY": "start_date",
        "End MM/YY": "end_date",
        "ฉบับแรก": "first_book_number",
        "ฉบับสุดท้าย": "last_book_number",
        "จำนวนเงิน": "amount_payment",
        "Ref Payment": "ref_payment",
        "วันที่โอน": "payment_date",
        "เวลาโอน": "payment_at",
        "หมายเหตุการชำระเงิน": "note",
        "PRO": "pro",
        "Pro Done": "pro_done",
        "Remark": "remark",
        "วันที่บันทึก": "save_at",
    }
    df = extract_excel(
        file_name=config.data.raw,
        sheet_name=config.process.sheet_name[0],
        columns=columns,
    )
    # arrange columns
    print(f"{df.columns = }")

    required_cols = [
        "id",
        "new_status",
        "member_number",
        "member_type",        
        "pre_name",
        "first_last_name",
        "tel_raw",
        "tel_1",
        "tel_2",
        "address",
        "subdistrict",
        "district",
        "province",
        "postal",
        "zone",
        "magazine_type",
        "amount_of_book",
        "email",
        "facebook",
        "delivery_method",
        "regiestry_method",
        "start_date",
        "end_date",
        "first_book_number",
        "last_book_number",
        "ref_payment",
        "amount_payment",
        "payment_date",
        "payment_at",
        "datetime_payment",
        "note",
        "pro",
        "pro_done",
        "remark",
        "save_at",
        "create_at",
        "updated_at",
        "deleted_at",
        "tel_1_search",
        "tel_2_search",
        "line_id",
        "id_link",
    ]
    df_set = set(df.columns)
    required_set = set(required_cols)
    diff=required_set.difference(df_set)
    print(diff)
    df[list(diff)]=None
    print(df.columns)
    
    ingesting_df = df[required_cols]
    ingesting_df["tel_1"]=ingesting_df["tel_raw"].apply(lambda x: str(x).split(",")[0] if len(str(x).split(","))>0 else None)
    ingesting_df["tel_2"]=ingesting_df["tel_raw"].apply(lambda x: str(x).split(",")[1] if len(str(x).split(","))==2 else None)
    replace_dash_fnc  = lambda x: str(x).replace("-","") if "-" in str(x) else None
    ingesting_df["tel_1_search"]=ingesting_df["tel_1"].apply(replace_dash_fnc)
    ingesting_df["tel_2_search"]=ingesting_df["tel_2"].apply(replace_dash_fnc)
    print(ingesting_df.columns)
    assert len(required_set.symmetric_difference(set(ingesting_df.columns)))==0, "schema is not the same as destination"
    pandas_to_mysql(df=ingesting_df, schema="5000s",table_name="members")


if __name__ == "__main__":
    process_data()
