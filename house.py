import pandas as pd

home_prices = pd.read_csv('data/CSUSHPISA.csv', parse_dates=['DATE'])
federal_funds_rate = pd.read_csv('data/DFF.csv', parse_dates=['DATE'])
disposable_income = pd.read_csv('data/DSPIC96.csv', parse_dates=['DATE'])
housing_starts = pd.read_csv('data/HOUST1F.csv', parse_dates=['DATE'])
mortgage_rate = pd.read_csv('data/MORTGAGE30US.csv', parse_dates=['DATE'])
housing_supply = pd.read_csv('data/MSACSR.csv', parse_dates=['DATE'])
residential_investment = pd.read_csv('data/PRRESCONS.csv', parse_dates=['DATE'])
unemployment_rate = pd.read_csv('data/UNRATE.csv', parse_dates=['DATE'])
personal_savings_rate = pd.read_csv('data/PSAVERT.csv', parse_dates=['DATE'])
real_disposable_personal_income = pd.read_csv('data/A229RX0.csv', parse_dates=['DATE'])


def preprocess_data(df, start_year=1990, end_year=2024, name=None):
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['YearMonth'] = df['DATE'].dt.to_period('M')
    df = df[(df['DATE'].dt.year >= start_year) & (df['DATE'].dt.year <= end_year)]
    if name:
        df = df.rename(columns={df.columns[1]: name})
    return df[['YearMonth', name]]


home_prices = preprocess_data(home_prices, name='Home_Price')
federal_funds_rate = preprocess_data(federal_funds_rate, name='Federal_Funds_Rate')
disposable_income = preprocess_data(disposable_income, name='Disposable_Income')
housing_starts = preprocess_data(housing_starts, name='Housing_Starts')
mortgage_rate = preprocess_data(mortgage_rate, name='Mortgage_Rate')
housing_supply = preprocess_data(housing_supply, name='Housing_Supply')
residential_investment = preprocess_data(residential_investment, name='Residential_Investment')
unemployment_rate = preprocess_data(unemployment_rate, name='Unemployment_Rate')
personal_savings_rate = preprocess_data(personal_savings_rate, name='Personal_Savings_Rate')


datasets = [federal_funds_rate, disposable_income, housing_starts, mortgage_rate, housing_supply, residential_investment, unemployment_rate,
            personal_savings_rate]


merged_data = home_prices
for dataset in datasets:
    merged_data = pd.merge(merged_data, dataset, on='YearMonth', how='left')


columns = [col for col in merged_data.columns if col != 'Home_Price']
columns.append('Home_Price')
merged_data = merged_data[columns]


print(merged_data.head())
print(merged_data.shape)


merged_data.to_csv('data/final_data/merged_data.csv', index=False)
