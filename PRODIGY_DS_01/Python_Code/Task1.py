import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

csv_file_path = '/content/API_SP.POP.TOTL_DS2_en_csv_v2_406129.csv'
df = pd.read_csv(csv_file_path, skiprows=4, sep=',')

df_cleaned = df.drop(columns=['2025', 'Unnamed: 70', 'Indicator Name', 'Indicator Code'])

year_cols = [col for col in df_cleaned.columns if col.isdigit()]
id_vars = ['Country Name', 'Country Code']
df_long = df_cleaned.melt(id_vars=id_vars, value_vars=year_cols, var_name='Year', value_name='Population')
df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce').astype(int)
df_long['Population'] = pd.to_numeric(df_long['Population'], errors='coerce')

df_filled = df_long.copy()
df_filled['Population'] = df_filled.groupby('Country Code')['Population'].transform(lambda x: x.ffill().bfill())
df_filled.drop_duplicates(inplace=True)

aggregate_codes = ['WLD', 'IBT', 'LMY', 'MIC', 'IBD', 'EMU', 'LMC', 'UMC', 'EAS', 'LTE', 'EAR', 'EAP', 'IDA', 'IDX', 'LAC', 'MNA', 'NAC', 'SAS', 'SSA', 'SST', 'SXY', 'XZN', 'XKX', 'TLA', 'TSA', 'TEA', 'TEC', 'TSS', 'HIC', 'PRP', 'OEC']
df_countries = df_filled[~df_filled['Country Code'].isin(aggregate_codes)].copy()

latest_year = df_countries['Year'].max()
top_10 = df_countries[df_countries['Year'] == latest_year].sort_values(by='Population', ascending=False).head(10)

plt.figure(figsize=(12, 7))
sns.barplot(x='Country Name', y='Population', data=top_10, hue='Country Name', palette='viridis', legend=False)
plt.title(f'Top 10 Countries by Population in {latest_year}')
plt.xticks(rotation=45)
plt.show()

global_pop = df_countries.groupby('Year')['Population'].sum().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Population', data=global_pop, marker='o')
plt.title('Global Population Trend')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df_countries[df_countries['Year'] == latest_year]['Population'].dropna(), bins=30, kde=True)
plt.title('Population Distribution')
plt.show()