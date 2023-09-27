# Country/Territory,Code,Year,
# Meningitis,Alzheimer's Disease and Other Dementias,Parkinson's Disease,
# Nutritional Deficiencies,Malaria,Drowning,Interpersonal Violence,Maternal Disorders,HIV/AIDS,Drug Use Disorders,
# Tuberculosis,Cardiovascular Diseases,Lower Respiratory Infections,Neonatal Disorders,Alcohol Use Disorders,Self-harm,
# Exposure to Forces of Nature,Diarrheal Diseases,Environmental Heat and Cold Exposure,Neoplasms,
# Conflict and Terrorism,Diabetes Mellitus,Chronic Kidney Disease,Poisonings,Protein-Energy Malnutrition,Road Injuries,
# Chronic Respiratory Diseases,Cirrhosis and Other Chronic Liver Diseases,Digestive Diseases,"Fire, Heat, and Hot Substances",Acute Hepatitis

import numpy as np
import pandas as pd

import pycountry

import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import matplotlib.pyplot as plt

pd.options.plotting.backend = "plotly"


def map_contries_to_continents(df, cont_df):
    # Get List of Countries
    list_of_countries = df['Country/Territory'].unique()
    df['Continent'] = None
    # Map Countries to Continents
    for country in list_of_countries:
        cont = cont_df.loc[cont_df['Country'] == country, 'Continent'].values.tolist()
        if cont:
            df.loc[df['Country/Territory'] == country, 'Continent'] = cont[0]
        else:
            print(country)
    # Color Code
    # df.Continent = pd.Categorical(df.Continent)
    # df['Continent_Code'] = df.Continent.cat.codes
    # Save DF [For Further Use]
    df.to_csv('cause_of_deaths_cont.csv')
    return df


def add_population_by_country(df, pop_df):
    # Get List of Countries
    list_of_countries = df['Country/Territory'].unique()
    list_of_years = df['Year'].unique()
    df['Population'] = None
    # Map Population to Countries
    for country in list_of_countries:
        for year in list_of_years:
            population = pop_df.loc[(pop_df['Country'] == country) & (pop_df['Year'] == year), 'Total'].values.tolist()
            if population:
                df.loc[(df['Country/Territory'] == country) & (df['Year'] == year), 'Population'] = int(population[0].replace(' ', '')) * 1000
            else:
                print(country)
    # Save DF [For Further Use]
    df.to_csv('cause_of_deaths_cont_pop.csv')
    return df




# Hypothesis 1
def plot_hyp_1_1(df):
    df['Alcohol Use Disorders_percent'] = df['Alcohol Use Disorders'] / df['Population']
    df['Cirrhosis and Other Chronic Liver Diseases_percent'] = 100 * df['Cirrhosis and Other Chronic Liver Diseases'] / df['Population']

    grouped = df.groupby(by=['Year', 'Country/Territory'], as_index=False).agg({"Alcohol Use Disorders_percent": "sum", "Cirrhosis and Other Chronic Liver Diseases_percent": "sum"}).groupby(by=['Country/Territory'], as_index=False)
    Continents = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

    data = []
    for country in grouped.groups:
        g = grouped.get_group(country)

        df_corr = g[['Alcohol Use Disorders_percent', 'Cirrhosis and Other Chronic Liver Diseases_percent']].corr()
        try:
            data.append({'Country': country, 'code': pycountry.countries.search_fuzzy(country)[0].alpha_3 ,'Corr': df_corr.values[1,0]})
        except:
            data.append({'Country': country, 'code': None ,'Corr': df_corr.values[1,0]})
    df_corr = pd.DataFrame.from_records(data)

    fig = go.Figure(data=go.Choropleth(locations = df_corr['code'], z = df_corr['Corr'], text = df_corr['Country'], colorscale = 'RdBu', autocolorscale=False, reversescale=False, marker_line_color='darkgray', marker_line_width=0.5, colorbar_ticksuffix = '%', colorbar_title = '[-1,1]'))
    # fig.update_layout(autosize=False, width=1000, height=800)
    # fig.update_layout(title='Correlation Coefficient of the Fatalities due to (Alcohol Use Disorders) and (Cirrhosis and Other Chronic Liver Diseases) per Country from 1990 to 2019]', autosize=False, width=1000, height=800)
    # print('Correlation Coefficient of the Fatalities due to (Alcohol Use Disorders) and (Cirrhosis and Other Chronic Liver Diseases) per Country from 1990 to 2019]')
    fig.show()


def plot_hyp_1_2(df):
    df_corr = df[['Alcohol Use Disorders', 'Cirrhosis and Other Chronic Liver Diseases']].corr()
    fig = go.Figure()
    fig.add_trace(go.Heatmap(x = df_corr.columns, y = df_corr.index, z = np.array(df_corr), text=df_corr.values, texttemplate='%{text:.2f}'))
    # fig.update_layout(autosize=False, width=1000, height=500)
    # fig.update_layout(title='Overall Correlation Matrix of the Fatalities due to (Alcohol Use Disorders) and (Cirrhosis and Other Chronic Liver Diseases) Worldwide from 1990 to 2019]', autosize=False, width=1000, height=500)
    fig.show()









# Hypothesis 2
def plot_hyp_2_1(df):
    df['Road Injuries_percent'] = 100 * df['Road Injuries'] / df['Population']
    grouped = df.groupby(by=['Year', 'Continent'], as_index=False).agg({"Road Injuries_percent": "sum", "Road Injuries": "sum"}).groupby(by=['Continent'], as_index=False)
    grouped_2 = df.groupby(by=['Year', 'Continent'], as_index=False).agg({"Road Injuries_percent": "sum", "Road Injuries": "sum"})
    Continents = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

    fig = make_subplots(specs=[[{"secondary_y": True}]])


    for cont in Continents:
        g = grouped.get_group(cont)
        fig.add_trace(go.Scatter(name=cont, x=g['Year'], y=g['Road Injuries_percent'], mode='lines+markers'), secondary_y=True)

    fig.add_trace(go.Bar(name='Worldwide', x=grouped_2['Year'], y=grouped_2['Road Injuries'], marker_color='darkgray'), secondary_y=False)

    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text='Percentage of Road Injuries Fatalities / Continent', rangemode='tozero', scaleanchor='y', scaleratio=1, constraintoward='bottom', secondary_y=True)
    fig.update_yaxes(title_text='Total Road Injuries Fatalities Worldwide', rangemode='tozero', scaleanchor='y2', scaleratio=1/1000000, constraintoward='bottom', secondary_y=False)

    fig.update_layout(barmode='group', autosize=False, width=1000, height=600)
    fig.show()



def plot_hyp_2_2(df):
    df['Road Injuries_percent'] = 100 * df['Road Injuries'] / df['Population']

    grouped = df.groupby(by=['Year', 'Country/Territory'], as_index=False).agg({"Road Injuries_percent":"sum"}).groupby(by=['Country/Territory'], as_index=False)

    data = []
    for country in grouped.groups:
        g = grouped.get_group(country)
        g_ = g['Road Injuries_percent'].pct_change() * 100
        try:
            data.append({'Country': country, 'code': pycountry.countries.search_fuzzy(country)[0].alpha_3 ,'Corr': g_.mean()})
        except:
            data.append({'Country': country, 'code': None ,'Corr': g_.mean()})

    df_pct = pd.DataFrame.from_records(data)

    fig = go.Figure(data=go.Choropleth(locations = df_pct['code'], z = df_pct['Corr'], text = df_pct['Country'], colorscale = 'RdBu', autocolorscale=False, reversescale=True, marker_line_color='darkgray', marker_line_width=0.5, colorbar_title = '%'))
    # fig.update_layout(autosize=False, width=1000, height=800)
    fig.show()



# df = pd.read_csv('../data/cause_of_deaths_cont_pop.csv')
#
# plot_hyp_1_1(df)
# plot_hyp_1_2(df)
#
#
# plot_hyp_2_2(df)
# plot_hyp_2_3(df)
