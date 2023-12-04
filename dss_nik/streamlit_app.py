import pandas as pd
import plotly.express as px
import streamlit as st
import os 
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(layout='wide')

# IMPORT AND READ DATA
employ_merge = pd.read_pickle(base_dir + '/data/employ_clean.pkl')
coord = pd.read_csv(base_dir + '/data/coordinate.csv')

# TITLE & DESCRIPTION
st.title('Employee Demography Dashboard: Leveraging NIK Data Enrichment for Comprehensive Workforce Analysis')
st.write("""Dive into the future of workforce analytics with the interactive "Employee Demography Dashboard." 
            Leveraging Indonesia's National ID Number (NIK) data, we bring a new dimension to understanding employee dynamics.""")
st.write('**Dashboard Created by: Putu Sanisa Pascaline**')

# Creating two columns for the additional sections
col1, col2 = st.columns(2)

# Why Data Enrichment and NIK: A Treasure Trove of Demographics
with col1:
    st.markdown('### Why Data Enrichment?')
    st.write('Transform raw data into a goldmine of insights. From geographical mapping to behavioral patterns, '
             'enriching data means enhanced accuracy and deeper, actionable insights.')
    st.markdown('### NIK: A Treasure Trove of Demographics')
    st.write("NIK is not just a number—it's a key to unlock rich demographic details for every Indonesian citizen. "
             "Ethical, comprehensive, and insightful, it's the backbone of data strategy.")

# Empowering Decisions Across Sectors and Our Dashboard: Your Insight Engine
with col2:
    st.markdown('### Empowering Decisions Across Sectors')
    st.write("Whether it's banking, education, or government planning, enriched data paves the way for smarter "
             "decisions and strategies.")
    st.markdown('### This Dashboard: Your Insight Engine')
    st.write("Visualize hiring trends, map employee distribution, and discover generational and gender insights. "
             "This dashboard isn't just about data; it's about stories hidden within numbers, ready to be explored and acted upon.")

# Divider
st.divider()

# --- ROW 1 ---
col1, col2 = st.columns(2)

## --- LINE PLOT ---

# data: line plot
df_join = pd.crosstab(index=employ_merge['join_year'],
                       columns='join_count', 
                       colnames=[None])
df_join = df_join.reset_index()

# plot: line plot
plot_join = px.line(df_join, x='join_year', y='join_count', markers=True,
                     labels = {
                         'join_year' : 'Year',
                         'join_count' : 'Employee Joining'})

col1.write('### Joining Frequency over Time')
## --- Explanation ---
col1.write("Track hiring trends with a line chart showing employee joinings over time. Gain insights into growth, recruitment effectiveness, and identify hiring spikes.")
col1.plotly_chart(plot_join, use_container_width=True)


## --- MAP PLOT ---
# data: map
prov_gender = pd.crosstab(index=employ_merge['province'],
                        columns=employ_merge['gender'], colnames=[None])
prov_gender['Total'] = prov_gender['Female'] + prov_gender['Male']
df_map = prov_gender.merge(coord, on='province')

# plot: map
plot_map = px.scatter_mapbox(data_frame=df_map, lat='latitude', lon='longitude',
                             mapbox_style='carto-positron', zoom=3,
                             size='Total',
                             hover_name='province',
                             hover_data={'Male': True,
                                         'Female': True,
                                         'latitude': False,
                                         'longitude': False})

col2.write('### Employee Count across Indonesia')
## --- Explanation ---
col2.write("A map chart visualizes employee distribution across Indonesia's provinces, highlighting regional workforce diversity and aiding strategic regional decisions.")
col2.plotly_chart(plot_map, use_container_width=True)


# --- ROW 2 ---
st.divider()
col3, col4 = st.columns(2)

## --- INPUT SELECT ---
input_select = col3.selectbox(
    label='Select Department',
    options=employ_merge['department_name'].unique().sort_values()
)

## --- INPUT SLIDER ---
input_slider = col4.slider(
    label='Select age range',
    min_value=employ_merge['age'].min(),
    max_value=employ_merge['age'].max(),
    value=[20,50]
)

min_slider = input_slider[0]
max_slider = input_slider[1]


# --- ROW 3 ---
col5, col6 = st.columns(2)


## --- BARPLOT ---
# data: barplot
employ_cs = employ_merge[employ_merge['department_name'] == input_select]
df_gen = pd.crosstab(index=employ_cs['generation'], columns='num_people', colnames=[None])
df_gen = df_gen.reset_index()

# plot: barplot
plot_gen = px.bar(df_gen, x='generation', y='num_people', 
                   labels = {'generation' : 'Generation',
                             'num_people' : 'Employee Count'})

col5.write(f'### Employee Count per Generation in {input_select} Dept.') # f-string
## --- Explanation ---
col5.write("Analyze generational diversity within departments using a bar chart. Understand demographic composition for tailored management and succession planning.")
col5.plotly_chart(plot_gen, use_container_width=True)


## --- MULTIVARIATE ---
# data: multivariate
employ_age = employ_merge[employ_merge['age'].between(left=min_slider, right=max_slider)]
dept_gender = pd.crosstab(index=employ_age['department_name'],
                          columns=employ_age['gender'],
                          colnames=[None])
dept_gender_melt = dept_gender.melt(ignore_index=False, var_name='gender', value_name='num_people')
dept_gender_melt = dept_gender_melt.reset_index()

# plot: multivariate
plot_dept = px.bar(dept_gender_melt.sort_values(by='num_people'), 
                   x="num_people", y="department_name", 
                   color="gender", 
                   barmode='group',
                   labels = {'num_people' : 'Employee Count',
                             'department_name' : 'Department',
                             'gender': 'Gender'}
                             )

col6.write(f'### Gender per Department, Age {min_slider} to {max_slider}')
## --- Explanation ---
col6.write("Interactive slider chart to explore gender representation across age groups in various departments, supporting equitable HR practices and diversity.")
col6.plotly_chart(plot_dept, use_container_width=True)

# Divider
st.divider()

# --- NEW VISUALIZATION: Geographical Distribution of Departments ---
st.markdown('### Geographical Distribution of Departments')
## --- Explanation ---
st.write("Map chart showing departments' spread across provinces, useful for strategic planning, departmental expansions, and understanding regional talents.")

# Merging data for the new plot
dept_distribution = pd.crosstab(index=employ_merge['province'], columns=employ_merge['department_name'])
dept_distribution = dept_distribution.merge(coord, on='province')

# Creating the map plot
fig_dept_distribution = px.scatter_mapbox(dept_distribution, lat='latitude', lon='longitude',
                                          size=dept_distribution.max(axis=1),
                                          hover_name='province',
                                          hover_data=dept_distribution.columns[:-2],
                                          mapbox_style='carto-positron', zoom=3)

st.plotly_chart(fig_dept_distribution, use_container_width=True)

# Divider
st.divider()

# Creating two columns for the visualizations
col1, col2 = st.columns(2)

# --- NEW VISUALIZATION: Average Age per Province ---
with col1:
    st.markdown('### Average Age per Province')
    ## --- Explanation ---
    st.write("Bar chart depicting average age or experience of employees in provinces, aiding in HR strategy and understanding workforce maturity regionally.")
    # Calculating average age per province
    avg_age_per_province = employ_merge.groupby('province')['age'].mean()
    avg_age_df = avg_age_per_province.reset_index()

    # Dropdown for selecting provinces to compare
    selected_provinces = st.multiselect('Select Provinces for Comparison', avg_age_df['province'].unique())

    # Filtering the data based on the selected provinces
    filtered_avg_age_df = avg_age_df[avg_age_df['province'].isin(selected_provinces)]

    # Creating the bar plot for the selected provinces
    if not filtered_avg_age_df.empty:
        fig_avg_age = px.bar(filtered_avg_age_df, x='province', y='age',
                             labels={'age': 'Average Age', 'province': 'Selected Province'},
                             color='age')
        st.plotly_chart(fig_avg_age, use_container_width=True)
    else:
        st.write("Please select at least one province for comparison.")


# --- NEW VISUALIZATION: Gender Ratio per Province ---
with col2:
    st.markdown('### Gender Ratio per Province')
    ## --- Explanation --
    st.write("Pie charts showcase gender ratio in each province, offering insights into diversity and informing gender-balanced recruitment and inclusivity efforts.")
    # Calculating gender ratio per province
    gender_ratio = employ_merge.groupby('province')['gender'].value_counts(normalize=True).unstack()
    gender_ratio_df = gender_ratio.reset_index()

    # Dropdown for selecting a province
    selected_province = st.selectbox('Select a Province', gender_ratio_df['province'].unique())

    # Displaying the pie chart for the selected province
    st.markdown(f'#### Gender Ratio in {selected_province}')
    fig_gender_ratio = px.pie(gender_ratio_df[gender_ratio_df['province'] == selected_province],
                              names=gender_ratio_df.columns[1:],  # Assuming these are 'Female' and 'Male'
                              values=gender_ratio_df.loc[gender_ratio_df['province'] == selected_province, gender_ratio_df.columns[1:]].values[0])
    st.plotly_chart(fig_gender_ratio, use_container_width=True)
