import pandas as pd


def to_csv(df, name, prefix='csv/'):
    path = prefix + name + '.csv'
    df.to_csv(path, index=False)


def to_many_csv(*dfs, names=None):
    if not names or len(dfs) != len(names):
        print('Export failed: names argument does not match dfs argument')
        return
    for df, name in zip(dfs, names):
        path = 'csv/' + name + '.csv'
        df.to_csv(path, index=False)


def to_csv_cropped(dfs_dict, day_start="2026-01-01", day_end="2026-04-30", no_content=True):
    cropped = {}

    for name, df in dfs_dict.items():
        if no_content:
            drop_columns = ['content', 'content_structured', 'content_1', 'content_2', 'content_a', 'content_b']
        else:
            drop_columns = []

        new_df = df.copy()
        col = 'day' if 'day' in new_df.columns else 'date'

        start = pd.to_datetime(day_start, utc=True)
        end = pd.to_datetime(day_end, utc=True)

        if col == 'date':
            end = end + pd.Timedelta(days=1)

        new_df = new_df[(new_df[col] >= start) & (new_df[col] < end)]

        if drop_columns:
            new_df = new_df.drop(columns=drop_columns, errors="ignore")

        cropped[name] = new_df
        to_csv(new_df, name, prefix='csv/cropped/cropped_')

    return cropped