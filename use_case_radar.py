import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Use Case Radar")

df = pd.read_csv('2024-01-02_UseCase_maturity_map_for_FSI - use case master for radar.csv')
unit = df['unit'].unique()
unit_choice = st.sidebar.selectbox('Select your Business Unit:', unit)
sub_unit = df['sub_unit'].loc[df['unit'] == unit_choice].unique()
sub_unit_choice = st.sidebar.multiselect('Select your Use Case Category:', sub_unit, default=sub_unit[0])

df_filtered = df.loc[(df['unit'] == unit_choice) & (df['sub_unit'].isin(sub_unit_choice))]

# st.dataframe(df_filtered)

fig = px.scatter(df_filtered,
                 labels={
                     'x_innovation': 'Maturity Stage:',
                     'y_innovation': 'Maturity Stage:',
                     'use_case_family': 'Use Case group ',
                     'uc_id': 'Use Case ID ',
                     'maturity_stages': 'Effort to build '
                 },
                 x='x_innovation',
                 y='y_innovation',
                 color='use_case_family',
                 hover_name="use_case_name",
                 hover_data={'x_innovation': False,
                             'y_innovation': False,
                             'effort': False,
                             'uc_id': True,
                             'maturity_stages': True},
                 size='effort',
                 size_max=60,
                 height=700,
                 width=900,
                 )

fig.update_xaxes(ticktext=["Foundation", "Optimization", "Transformation"],
                 tickvals=["1", "10", "20"],
                 showgrid=True,
                 zeroline=False)

fig.update_yaxes(ticktext=["Foundation", "Optimization", "Transformation"],
                 tickvals=["1", "10", "20"],
                 tickangle=270,
                 showgrid=True,
                 zeroline=False)

fig_2 = px.scatter(df_filtered,
                   labels={
                       'effort': 'Effort to build:',
                       'impact': 'Impact to Business:',
                       'use_case_family': 'Use Case group',
                       'uc_id': 'Use Case ID',
                       'maturity_stages': 'Effort to build'
                   },
                   x='effort',
                   y='impact',
                   color='use_case_family',
                   hover_name="use_case_name",
                   hover_data={'x_innovation': False,
                               'y_innovation': False,
                               'effort': False,
                               'impact': False,
                               'uc_id': True,
                               'maturity_stages': True},
                   size='effort',
                   size_max=60,
                   height=700,
                   width=900,
                   )

# xaxes is the Effort
fig_2.update_xaxes(ticktext=["Simple", "Medium", "Complex"],
                   tickvals=["1", "10", "20"],
                   showgrid=True,
                   zeroline=False)

# yaxes is the Innovation
fig_2.update_yaxes(ticktext=["Low", "Medium", "Hight"],
                   tickvals=["1", "10", "20"],
                   tickangle=270,
                   showgrid=True,
                   zeroline=False)

tab1, tab2 = st.tabs(["Maturity Radar", "Long Hanging Fruit Radar"])
with tab1:
    st.plotly_chart(fig, theme="streamlit")
with tab2:
    st.plotly_chart(fig_2, theme="streamlit")
