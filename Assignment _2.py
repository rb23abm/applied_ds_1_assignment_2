import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

#setting views for dataframe
pd.options.display.max_rows = 40
pd.options.display.max_columns = 40


def load_dataframe(filename):
    '''
    Function to load the dataframe and manipulate the country and rows
    features and return two datframes(Raw Dataframe and Cleaned Dataframe).
    '''
    df_year_col = pd.read_excel(filename,engine="openpyxl")
    df_temp = pd.melt(
        df_year_col,
        id_vars=[
            'Country Name',
            'Country Code',
            'Indicator Name',
            'Indicator Code'],
        var_name='Year',
        value_name='Value')
    df_country_col = df_temp.pivot_table(
        index=['Year', 'Country Code', 'Indicator Name', 'Indicator Code'],
        columns='Country Name',
        values='Value').reset_index()
    df_country_col = df_country_col.drop_duplicates().reset_index()
    return df_year_col,df_country_col


def years_to_analyze_data(data,year1,year2,frequency = 5):
    '''
    function retrieve data from start year to end year based on interval.
    '''
    data_temp = data.copy()
    years_to_analyze=[i for i in range(year1,year2,frequency)]
    col_to_keep=['Country Name','Indicator Name']
    col_to_keep.extend(years_to_analyze)
    data_temp =  data_temp[col_to_keep]
    data_temp = data_temp.dropna(axis=0, how="any")
    return data_temp


def data_specific_field(data,feature,value_list):
    '''
    function to filter dataframe based on values of column.
    '''
    data_temp = data.copy()
    data_field = data_temp[
        data_temp[feature].isin(value_list)].reset_index(drop=True)
    return data_field


def bar_plot_country_year(data,indicator):
    # Filter numeric columns for plotting
    df = data.copy()
    df.set_index('Country Name', inplace=True)
    numeric_columns = df.columns[df.dtypes == 'float64']
    df_numeric = df[numeric_columns]


    # Plotting
    plt.figure(figsize=(50, 50))
    df_numeric.plot(kind='bar')
    plt.title(indicator)
    plt.xlabel('Country Name')
    plt.ylabel('Urban Population (% of Total Population)')
    plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()


def get_data_indicator(data):
    """
    function to give indicator names as columns for
    respective dataframe country
    """
    df=data.copy()
    df_melted = df.melt(
        id_vars='Indicator Name',
        var_name='Year', value_name='Value')
    df_pivoted = df_melted.pivot(
        index='Year', columns='Indicator Name', values='Value')
    df_pivoted.reset_index(inplace=True)
    df_pivoted = df_pivoted.apply(pd.to_numeric, errors='coerce')
    del df_pivoted['Year']
    df_pivoted = df_pivoted.rename_axis(None, axis=1)
    return df_pivoted


def time_series_plot(data,indicator):
    '''
    plot year wise data for respective countries
    '''
    df = data.copy()
    # Filter numeric columns for plotting
    df.set_index('Country Name', inplace=True)
    numeric_columns = df.columns[df.dtypes == 'float64']
    df_numeric = df[numeric_columns]

    # Plotting
    plt.figure(figsize=(12, 6))
    for country in df_numeric.index:
        plt.plot(
            df_numeric.columns,
            df_numeric.loc[country],
            label=country, linestyle='dashed', marker='o')

    plt.title(indicator)
    plt.xlabel('Year')
    #plt.ylabel('Urban Population (% of Total Population)')
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.show()


# Loading the dataset
df_year_col,df_country_col = load_dataframe('world_bank_climate.xlsx')

#taking data from 1990 to 2020 on 5 year gap.
df_year_col_temp = years_to_analyze_data(df_year_col,1990,2021,5)

countries = \
    df_year_col_temp['Country Name'].value_counts().index.tolist()[0:15]

# Looking at statistics of the data
print(df_year_col_temp.describe())

df_year_col_co2_emiss = data_specific_field(
    df_year_col_temp,
    'Indicator Name',
    ['CO2 emissions (metric tons per capita)'])

print(df_year_col_co2_emiss.describe())

df_year_col_co2_emiss_country = data_specific_field(
    df_year_col_co2_emiss,'Country Name',countries)

print(df_year_col_co2_emiss_country.describe())

bar_plot_country_year(
    df_year_col_co2_emiss_country,
    'CO2 emissions (metric tons per capita)')


df_year_col_fresh_water = data_specific_field(
    df_year_col_temp,
    'Indicator Name',
    ['Annual freshwater withdrawals, total (% of internal resources)'])
df_year_col_fresh_water  = data_specific_field(
    df_year_col_fresh_water,'Country Name',countries)

print(df_year_col_fresh_water.describe())

bar_plot_country_year(
    df_year_col_fresh_water,
    'Annual freshwater withdrawals, total (% of internal resources)')


df_year_col_korea = data_specific_field(
    df_year_col_temp,'Country Name',['Korea, Rep.'])

data_heat_map_korea = get_data_indicator(df_year_col_korea)

features_check = [
    "CO2 emissions (metric tons per capita)",
    "Annual freshwater withdrawals, total (% of internal resources)",
    "Urban population (% of total population)",
    "Total greenhouse gas emissions (kt of CO2 equivalent)",
    "Agricultural land (% of land area)",
    "Arable land (% of land area)",
    "Renewable energy consumption (% of total final energy consumption)",
    "Average precipitation in depth (mm per year)"]

data_heat_map_korea_sub = data_heat_map_korea[features_check]

print(data_heat_map_korea_sub.corr())

sns.heatmap(
    data_heat_map_korea_sub.corr(),
    annot=True, cmap='YlGnBu', linewidths=.5, fmt='.3g')



df_year_col_ghg = data_specific_field(
    df_year_col_temp,
    'Indicator Name',
    ['Total greenhouse gas emissions (kt of CO2 equivalent)'])
df_year_col_ghg = data_specific_field(
    df_year_col_ghg,'Country Name',countries)


print(df_year_col_ghg.describe())



df_year_col_ub_pop = data_specific_field(
    df_year_col_temp,
    'Indicator Name',
    ['Urban population (% of total population)'])
df_year_col_ub_pop = data_specific_field(
    df_year_col_ub_pop,'Country Name',countries)



time_series_plot(
    df_year_col_ghg,'Total greenhouse gas emissions (kt of CO2 equivalent)')



df_year_col_ag_land = data_specific_field(
    df_year_col_temp,'Indicator Name',['Agricultural land (% of land area)'])
df_year_col_ag_land = data_specific_field(
    df_year_col_ag_land,'Country Name',countries)



print(df_year_col_ag_land.describe())


time_series_plot(df_year_col_ag_land,'Agricultural land (% of land area)')



df_year_col_islam = data_specific_field(
    df_year_col_temp,'Country Name',['Iran, Islamic Rep.'])
data_heat_map_islam = get_data_indicator(df_year_col_islam)
data_heat_map_islam_sub = data_heat_map_islam[
    ["CO2 emissions (metric tons per capita)",
     "Annual freshwater withdrawals, total (% of internal resources)",
     "Urban population (% of total population)",
     "Total greenhouse gas emissions (kt of CO2 equivalent)",
     "Agricultural land (% of land area)",
     "Arable land (% of land area)",
     "Renewable energy consumption (% of total final energy consumption)",
     "Average precipitation in depth (mm per year)"]]
sns.heatmap(
    data_heat_map_islam_sub.corr(),
    annot=True, cmap='YlGnBu', linewidths=.5, fmt='.3g')



df_year_col_uk = data_specific_field(
    df_year_col_temp,'Country Name',['United Kingdom'])
data_heat_map_uk = get_data_indicator(df_year_col_islam)
data_heat_map_uk_sub = data_heat_map_uk[
    ["CO2 emissions (metric tons per capita)",
     "Annual freshwater withdrawals, total (% of internal resources)",
     "Urban population (% of total population)",
     "Total greenhouse gas emissions (kt of CO2 equivalent)",
     "Agricultural land (% of land area)",
     "Arable land (% of land area)",
     "Renewable energy consumption (% of total final energy consumption)",
     "Average precipitation in depth (mm per year)"]]
sns.heatmap(data_heat_map_uk_sub.corr(), annot=True,linewidths=.5, fmt='.3g')




