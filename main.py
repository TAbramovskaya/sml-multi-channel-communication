import build_df
import pandas as pd


if __name__ == "__main__":

    # To update data from raw JSON files and current emails:
    # messages = build_df.from_raw_data()

    # To load data from ready-made CSV files:
    messages = build_df.from_csv()
    messages['day'] = pd.to_datetime(messages['date']).dt.floor('D')


