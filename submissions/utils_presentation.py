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


def normalize_cols(data, col_names, coeff = 100):
    for col_name in col_names:
        data[f'{col_name}_Normalized'] = coeff * ((data[col_name] - data[col_name].min()) / (data[col_name].max() - data[col_name].min()))
    return data




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
    fig.update_layout(title='Correlation Coefficient of the Fatalities due to Alcohol Use Disorders and Chronic Liver Diseases per Country from 1990 to 2019', width=1200, height=700)
    # print('Correlation Coefficient of the Fatalities due to (Alcohol Use Disorders) and (Cirrhosis and Other Chronic Liver Diseases) per Country from 1990 to 2019]')
    fig.show()


def plot_hyp_1_2(df):
    df_corr = df[['Alcohol Use Disorders', 'Cirrhosis and Other Chronic Liver Diseases']].corr()
    fig = go.Figure()
    fig.add_trace(go.Heatmap(x = df_corr.columns, y = df_corr.index, z = np.array(df_corr), text=df_corr.values, texttemplate='%{text:.2f}'))
    # fig.update_layout(autosize=False, width=1000, height=500)
    # fig.update_layout(title='Overall Correlation Matrix of the Fatalities due to (Alcohol Use Disorders) and (Cirrhosis and Other Chronic Liver Diseases) Worldwide from 1990 to 2019]', , width=1200, height=700)
    fig.update_layout(title='Correlation Coefficient of the Fatalities due to Alcohol Use Disorders and Chronic Liver Diseases Worldwide from 1990 to 2019', width=1200, height=700)
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

    fig.update_layout(title='Comparison Between the Absolute Values and Relative Values of Total Road Injuries Fatalities worldwide from 1990 to 2019', barmode='group', autosize=False, width=1200, height=700)
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
    fig.update_layout(width=1200, height=700)
    fig.show()










# Hypothesis 3
def plot_hyp_3_1(df):
    candidates = df.groupby(by=['Country/Territory']).agg({"Conflict and Terrorism": "sum", "Continent": "max"})
    continents = df.groupby(by=['Continent']).agg({"Conflict and Terrorism": "sum"})

    candidates = candidates.fillna('NaN')

    labels = candidates.index.values.tolist()
    parents = candidates['Continent'].values.tolist()
    values = candidates['Conflict and Terrorism'].values.tolist()

    labels.extend(continents.index.values.tolist())
    parents.extend(["" for _ in range(len(continents))])
    values.extend([x/1000 for x in continents['Conflict and Terrorism'].values.tolist()])

    fig = go.Figure(go.Treemap(labels=labels, parents=parents, values=values, marker_colorscale='Blues',  textinfo="label+percent root"))
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), width=1200, height=700,
                      title="The Number of Fatalities due to Conflict & War by Country & Continent from 1990-2019")
    fig.show()


def plot_hyp_3_2(df):
    candidates = df.groupby(by=['Country/Territory']).agg({"Conflict and Terrorism": "sum"}).sort_values(by='Conflict and Terrorism', ascending=False).head(7).index.values.tolist()

    ds = df[df['Country/Territory'].isin(candidates)].groupby('Country/Territory')

    fig = make_subplots(rows=ds.ngroups, subplot_titles=(list(ds.groups.keys())), shared_xaxes=True, vertical_spacing=0.035,
                        specs=[[{"secondary_y": True}] for i in candidates])

    i = 1
    for cunt, data in ds:
        data = data.sort_values(by='Year')
        data = normalize_cols(data, ['Conflict and Terrorism', 'Alcohol Use Disorders','Drug Use Disorders', 'Self-harm'])

        sizes_normalized = data['Conflict and Terrorism_Normalized'].values.tolist()
        # fig.add_trace(go.Scatter(name=cunt, x=data['Year'], y=data['Conflict and Terrorism_Normalized'], mode='markers', marker=dict(size=[x/2 for x in sizes_normalized])), row=i, col=1)
        fig.add_trace(go.Scatter(name='Conflict and Terrorism', x=data['Year'], y=[0 for x in range(len(data))], mode='markers', marker=dict(size=[x/2 for x in sizes_normalized], color='darkgray'), showlegend=True if i == 1 else False), row=i, col=1, secondary_y=True, )

        fig.add_trace(go.Scatter(name='Alcohol Use Disorders', x=data['Year'], y=data['Alcohol Use Disorders_Normalized'], mode='lines', line=dict(color='red'), showlegend=True if i == 1 else False), row=i, col=1, secondary_y=False, )
        fig.add_trace(go.Scatter(name='Drug Use Disorders', x=data['Year'], y=data['Drug Use Disorders_Normalized'], mode='lines', line=dict(color='green'), showlegend=True if i == 1 else False), row=i, col=1, secondary_y=False, )
        fig.add_trace(go.Scatter(name='Self-harm', x=data['Year'], y=data['Self-harm_Normalized'], mode='lines', line=dict(color='blue'), showlegend=True if i == 1 else False), row=i, col=1, secondary_y=False, )
        i+=1
        # print(data)
    fig.update_yaxes(secondary_y=False, showgrid=False, rangemode='tozero', gridcolor='darkgray')
    fig.update_yaxes(secondary_y=True, showgrid=False, showticklabels=False, gridcolor='darkgray')
    fig.update_xaxes(gridcolor='darkgray')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.1)', width=1200, height=700,
                      title="The Trend of Fatalities due-to Alcohol-Use, Drug-Abuse and Self harm in comparison with Conflicts & War mortalities during 1990-2019.", title_x=0.5)
    fig.show()



# Hypothesis 4
def plot_hyp_4_1(df):
    # Calculate Percentage of fatality based on Population
    # Group Data by Year, Continent
    # Aggregate the Variables by sum over years and continent
    df['Maternal Disorders_percent'] = 100 * df['Maternal Disorders'] / df['Population']
    df['Neonatal Disorders_percent'] = 100 * df['Neonatal Disorders'] / df['Population']
    df['Tuberculosis_percent'] = 100 * df['Tuberculosis'] / df['Population']
    df['Malaria_percent'] = 100 * df['Malaria'] / df['Population']

    grouped = df.groupby(by=['Year', 'Continent'], as_index=False).agg({"Maternal Disorders_percent": "sum", "Neonatal Disorders_percent": "sum", "Tuberculosis_percent": "sum",  "Malaria_percent": "sum"})

    # Create Figure wth Subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Create Color Maps [To Separate Continents]
    Maternal_colors = ['#468c22', '#3c771d', '#316318', '#274e13', '#1d390e', '#122509'] * len(df.Year.unique())
    Malaria_colors = ['#5A7E9B', '#738E87', '#194B74', '#003865', '#002C50', '#00213C'] * len(df.Year.unique())
    Tuberculosis_colors = ['#b28700', '#997300', '#7f6000', '#664d00', '#4c3900', '#332600'] * len(df.Year.unique())
    Neonatal_colors = ['#CF9374', '#C47952', '#B35320', '#AB4008', '#8F3607','#722B05'] * len(df.Year.unique())
    Continents = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

    # Add Graph Objects for each Cause of Death
    #   Assign an Offset Group for each and name them
    #   X -> Year   Y->Cause
    #   Assign Secondary and Primary Y-Axes
    fig.add_trace(go.Bar(offsetgroup=1, name='Maternal Disorders %', x=grouped['Year'], y=grouped['Maternal Disorders_percent'], marker_color=Maternal_colors), secondary_y=False)
    fig.add_trace(go.Bar(offsetgroup=2, name='Neonatal Disorders %', x=grouped['Year'], y=grouped['Neonatal Disorders_percent'], marker_color=Neonatal_colors), secondary_y=True)
    fig.add_trace(go.Bar(offsetgroup=3, name='Tuberculosis %', x=grouped['Year'], y=grouped['Tuberculosis_percent'], marker_color=Tuberculosis_colors), secondary_y=True)
    fig.add_trace(go.Bar(offsetgroup=4, name='Malaria %', x=grouped['Year'], y=grouped['Malaria_percent'], marker_color=Malaria_colors), secondary_y=True)

    # Update the Range and Scale for each Y_Axis -> To Overlap The Grid while maintinaing a reasonable value [Avoid Weird Scaling]
    fig.update_yaxes(title_text='Neonatal Disorders / Tuberculosis / Malaria', rangemode='tozero', scaleanchor='y', scaleratio=1, constraintoward='bottom', secondary_y=True)
    fig.update_yaxes(title_text='Maternal Disorders', rangemode='tozero', scaleanchor='y2', scaleratio=10, constraintoward='bottom', secondary_y=False)

    fig.update_xaxes(title_text="Year")
    fig.update_layout(barmode='group', bargroupgap=0, width=1200, height=700,
                      title="The Percentage Change of the fatalities due to Maternal Disorders, Tuberculosis, Malaria and Maternal Disorders from 1990-2019")

    fig.show()


def plot_white(df):
    ds = df.groupby(by=['Year']).agg({"Alzheimer's Disease and Other Dementias": "sum", "Nutritional Deficiencies": "sum"})
    # print(ds)
    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Nutritional Deficiencies', x=ds.index, y=ds['Nutritional Deficiencies'], mode='lines+markers'))
    fig.add_trace(go.Scatter(name="Alzheimer's Disease and Other Dementias", x=ds.index, y=ds["Alzheimer's Disease and Other Dementias"], mode='lines+markers'))
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Number of Deaths", rangemode='tozero')
    fig.update_layout(title="Fatalities of Nutrition Deficiencies vs Alzheimer's Disease 1990-2019", width=1200, height=700)
    fig.show()

def plot_black(df):
    ds = normalize_cols(df, ["Alzheimer's Disease and Other Dementias"], coeff=1)
    ds = normalize_cols(df, ["Nutritional Deficiencies"], coeff=-2)
    ds = df.groupby(by=['Year']).agg({"Alzheimer's Disease and Other Dementias_Normalized": "sum", "Nutritional Deficiencies_Normalized": "sum"})
    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Normalized Nutritional Deficiencies', x=ds.index, y=ds['Nutritional Deficiencies_Normalized'], mode='lines+markers'))
    fig.add_trace(go.Scatter(name="Normalized Alzheimer's Disease and Other Dementias * -2", x=ds.index, y=ds["Alzheimer's Disease and Other Dementias_Normalized"], mode='lines+markers'))
    fig.update_layout(template="plotly_dark", title="Relationship between Nutrition Deficiencies vs Alzheimer's Disease relays a correlation between them<br>Sponsored by Nastly", width=1200, height=700)
    fig.show()