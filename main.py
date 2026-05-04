import build_df


if __name__ == "__main__":

    # To update raw_data from raw JSON files and current emails:
    intensives, events, gmail, messages = build_df.from_raw_data()

    # To load data from ready-made CSV files:
    # intensives, events, gmail, messages = build_df.from_csv()


