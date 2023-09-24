import pandas as pd

# import raw data
print('Importing data...')
df_raw = pd.read_csv('../data/33100501.csv')

print('Cleaning data...')

# drop irrelevant columns
drop_columns = ['DGUID', 'UOM', 'UOM_ID', 'SCALAR_FACTOR', 'SCALAR_ID',
                'VECTOR', 'COORDINATE', 'STATUS', 'SYMBOL', 'TERMINATED',
                'DECIMALS']
df = df_raw.drop(columns=drop_columns)

# strip extra whitespace
cat_cols = df.select_dtypes(include='object').columns.tolist()
for col in cat_cols:
    df[col] = df[col].str.strip()

# remove rows of percentage data
df = df[df['Unit of measure'] == 'Number']
df.drop(columns=['Unit of measure'], inplace=True)

# filter out rows with totals
geo_total = df['GEO'] != 'Canada, total'
country_total = df['Country of control'] != 'Total all countries'
industry_total = df['Industry'] != 'Total all industries'
size_total = df['Size of enterprise'] != 'Total all sizes'
exec_total = df['Executive'] != 'All officers'
corp_total = df['Type of corporation'] != 'Total all corporations'

filters = [geo_total, country_total, industry_total, size_total, exec_total, corp_total]
for filter in filters:
    df = df[filter]

# drop nulls
df.dropna(inplace=True)

print(df.shape)

save_path = input("Enter path to save clean data (i.e. ../data/clean_data.csv): ")
df.to_csv(save_path, index=False)
print(f'File saved to {save_path}.')
