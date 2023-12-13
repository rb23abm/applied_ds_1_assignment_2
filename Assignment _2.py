
#importing required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



def load_dataframe_transpose(filename):
    '''
    A function to read the dataframe and transpose the country and rows features and return two datframes.
    '''
    df_year_column = pd.read_excel(filename,engine="openpyxl")
    df_t = pd.melt(df_year_column, id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                    var_name='Year', value_name='Value')
    df_country_column = df_t.pivot_table(index=['Year', 'Country Code', 'Indicator Name', 'Indicator Code'], columns='Country Name', values='Value').reset_index()
    df_country_column = df_country_column.drop_duplicates().reset_index()
    return df_year_column,df_country_column



df_year,df_country = load_dataframe_transpose('world_bank_climate.xlsx')


def year_data_to_analyze(data,year_start,year_end,frequency_year):
    data_sample = data.copy()
    years_needed=[i for i in range(year_start,year_end,frequency_year)]
    req_col=['Country Name','Indicator Name']
    req_col.extend(years_needed)
    data_sample =  data_sample[req_col]
    data_sample = data_sample.dropna(axis=0, how="any") #removing all the null value rows
    return data_sample

#gathering the year data from 1980 to 2020 with 5 interval gap
df_year_col = year_data_to_analyze(df_year,1980,2020,5)

#taking 8 countires to analyze based on the feature occurances
countries_to_analyze = df_year_col['Country Name'].value_counts().index.tolist()[1:8]



print(df_year_col.describe())


def filter_field_data(data,feature_to_check,value_list_elements):
    '''
    function to filter dataframe based on feature value.
    '''
    data_sample = data.copy()
    data_req= data_sample[data_sample[feature_to_check].isin(value_list_elements)].reset_index(drop=True)
    return data_req



df_year_col_co2int = filter_field_data(df_year_col,'Indicator Name',['CO2 intensity (kg per kg of oil equivalent energy use)'])


print(df_year_col_co2int.describe())


df_year_col_co2_countries  = filter_field_data(df_year_col_co2int,'Country Name',countries_to_analyze)

print(df_year_col_co2_countries.describe())


def bar_plot_containing_country_xlabel(data,indicator_variable):
    df_sample = data.copy()
    df_sample.set_index('Country Name', inplace=True)
    numeric_columns_to_keep = df_sample.columns[df_sample.dtypes == 'float64']
    df_numeric_sample = df_sample[numeric_columns_to_keep]
    plt.figure(figsize=(50, 50))
    df_numeric_sample.plot(kind='bar')
    plt.title(indicator_variable)
    plt.xlabel('Country Name')    
    plt.legend(title='Year', bbox_to_anchor=(1.10, 1), loc='upper left')
    plt.show()


bar_plot_containing_country_xlabel(df_year_col_co2_countries,'CO2 intensity (kg per kg of oil equivalent energy use)')


df_year_col_mort = filter_field_data(df_year_col,'Indicator Name',['Mortality rate, under-5 (per 1,000 live births)'])
df_year_col_mort  = filter_field_data(df_year_col_mort,'Country Name',countries_to_analyze)


print(df_year_col_mort.describe())


bar_plot_containing_country_xlabel(df_year_col_mort,'Mortality rate, under-5 (per 1,000 live births)')



#taking finland country data to analyze
df_year_finland = filter_field_data(df_year_col,'Country Name',['Finland'])


def filter_indicator_data(data):
    df_s=data.copy()
    # Melt the DataFrame
    df_melted_sample = df_s.melt(id_vars='Indicator Name', var_name='Year', value_name='Value')

    # Pivot the DataFrame
    df_pivoted_sample = df_melted_sample.pivot(index='Year', columns='Indicator Name', values='Value')

    # Reset index
    df_pivoted_sample.reset_index(inplace=True)
    df_pivoted_sample = df_pivoted_sample.apply(pd.to_numeric, errors='coerce')
    del df_pivoted_sample['Year']
    df_pivoted_sample = df_pivoted_sample.rename_axis(None, axis=1)
    return df_pivoted_sample



data_heat_map_finland = filter_indicator_data(df_year_finland)



data_heat_map_finland_map = data_heat_map_finland[["Urban population growth (annual %)","Mortality rate, under-5 (per 1,000 live births)","CO2 intensity (kg per kg of oil equivalent energy use)","Energy use (kg of oil equivalent per capita)","Electricity production from coal sources (% of total)","School enrollment, primary and secondary (gross), gender parity index (GPI)"]]


print(data_heat_map_finland_map.corr())


sns.heatmap(data_heat_map_finland_map.corr(), annot=True, cmap='YlGnBu', linewidths=.5, fmt='.3g')


df_year_col_energy= filter_field_data(df_year_col,'Indicator Name',['Energy use (kg of oil equivalent per capita)'])
df_year_col_energy  = filter_field_data(df_year_col_energy,'Country Name',countries_to_analyze)


print(df_year_col_energy.describe())


df_year_col_urban= filter_field_data(df_year_col,'Indicator Name',['Urban population (% of total population)'])
df_year_col_urban  = filter_field_data(df_year_col_urban,'Country Name',countries_to_analyze)




def plotting_time_series(data,indicator_label):
    '''
    plot time series graph for indicators.
    '''
    df_sample = data.copy()
    df_sample.set_index('Country Name', inplace=True)
    numeric_columns_need = df_sample.columns[df_sample.dtypes == 'float64']
    df_numeric_need = df_sample[numeric_columns_need]

    plt.figure(figsize=(12, 6))
    for count in df_numeric_need.index:
        plt.plot(df_numeric_need.columns, df_numeric_need.loc[count], label=count, linestyle='dashed', marker='o')

    plt.title(indicator_label)
    plt.xlabel('Year')
    plt.legend(title='Country', bbox_to_anchor=(1.15, 1), loc='upper left')

    plt.show()



plotting_time_series(df_year_col_energy,'Energy use (kg of oil equivalent per capita)')



df_year_col_school= filter_field_data(df_year_col,'Indicator Name',['School enrollment, primary and secondary (gross), gender parity index (GPI)'])
df_year_col_school  = filter_field_data(df_year_col_school,'Country Name',countries_to_analyze)


df_year_col_school.describe()



plotting_time_series(df_year_col_school,'School enrollment, primary and secondary (gross), gender parity index (GPI)')



df_year_col_new = filter_field_data(df_year_col,'Country Name',['New Zealand'])
data_heat_map_new = filter_indicator_data(df_year_col_new)
data_heat_map_new_sub = data_heat_map_new[["Urban population growth (annual %)","Mortality rate, under-5 (per 1,000 live births)","CO2 intensity (kg per kg of oil equivalent energy use)","Energy use (kg of oil equivalent per capita)","Electricity production from coal sources (% of total)","School enrollment, primary and secondary (gross), gender parity index (GPI)"]]
sns.heatmap(data_heat_map_new_sub.corr(), annot=True, cmap='YlGnBu', linewidths=.5, fmt='.3g')



df_year_col_swe= filter_field_data(df_year_col,'Country Name',['Sweden'])
data_heat_map_swe = filter_indicator_data(df_year_col_swe)
data_heat_map_swe_sub = data_heat_map_swe[["Urban population growth (annual %)","Mortality rate, under-5 (per 1,000 live births)","CO2 intensity (kg per kg of oil equivalent energy use)","Energy use (kg of oil equivalent per capita)","Electricity production from coal sources (% of total)","School enrollment, primary and secondary (gross), gender parity index (GPI)"]]
sns.heatmap(data_heat_map_swe_sub.corr(), annot=True, cmap='YlGnBu', linewidths=.5, fmt='.3g')



