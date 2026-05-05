def from_df(*dfs, names=None):
    if not names or len(dfs) != len(names):
        print('Export failed: names argument does not match dfs argument')
        return
    for df, name in zip(dfs, names):
        path = 'csv/' + name + '.csv'
        df.to_csv(path, index=False)
