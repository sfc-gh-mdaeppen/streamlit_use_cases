import pandas as pd
import plotly.graph_objs as go
import streamlit as st

pd.options.display.max_columns = None

st.set_page_config(layout="wide")
st.title("Use Case Dataflow")

df_dataflow = pd.read_excel('2024-01-02_UseCase_maturity_map_for_FSI.xlsx', header=1,
                            sheet_name='use_case_master_dataflow',
                            converters={'node_id': int,
                                        'source_1000': int,
                                        'target_1000': int,
                                        'source_1001': int,
                                        'target_1001': int,
                                        'source_1002': int,
                                        'target_1002': int,
                                        'source_1003': int,
                                        'target_1003': int,
                                        'source_1004': int,
                                        'target_1004': int,
                                        'source_1010': int,
                                        'target_1010': int,
                                        'source_1011': int,
                                        'target_1011': int,
                                        'source_1012': int,
                                        'target_1012': int,
                                        'source_1013': int,
                                        'target_1013': int
                                        })


print("df_dataflow")
print(df_dataflow)

# context selection
unit = df_dataflow['unit'].dropna().loc[lambda x: x != 'DataSource'].unique()
unit_choice = st.sidebar.selectbox('Select your Business Unit:', unit)

sub_unit = df_dataflow['sub_unit'].loc[df_dataflow['unit'] == unit_choice].unique()
sub_unit_choice = st.sidebar.multiselect('Select your Use Case Category:', sub_unit, default=sub_unit[0])

use_case = (df_dataflow['uc_id'].loc[(df_dataflow['unit'] == unit_choice) &
                              (df_dataflow['sub_unit'].isin(sub_unit_choice))].astype(int).unique())
use_case_choice = st.sidebar.multiselect('Select your Use Cases:', use_case, default=use_case[1])


df_dataflow = df_dataflow.loc[(df_dataflow['uc_id'].isin(use_case_choice))]


df_target = pd.concat([df_dataflow['target_1000'],
                       df_dataflow['target_1001'],
                       df_dataflow['target_1002'],
                       df_dataflow['target_1003'],
                       df_dataflow['target_1004'],
                       df_dataflow['target_1010'],
                       df_dataflow['target_1011'],
                       df_dataflow['target_1012'],
                       df_dataflow['target_1013']
                       ],
                      ignore_index=True)

# Create a DataFrame from the concatenated result
df_target_result = pd.DataFrame({'target': df_target}).dropna()

df_source = pd.concat([df_dataflow['source_1000'],
                       df_dataflow['source_1001'],
                       df_dataflow['source_1002'],
                       df_dataflow['source_1003'],
                       df_dataflow['source_1004'],
                       df_dataflow['source_1010'],
                       df_dataflow['source_1011'],
                       df_dataflow['source_1012'],
                       df_dataflow['source_1013']
                       ],
                      ignore_index=True)

df_source_result = pd.DataFrame({'source': df_source}).dropna()

df_color = pd.concat([df_dataflow['color_1000'],
                      df_dataflow['color_1001'],
                      df_dataflow['color_1002'],
                      df_dataflow['color_1003'],
                      df_dataflow['color_1004'],
                      df_dataflow['color_1010'],
                      df_dataflow['color_1011'],
                      df_dataflow['color_1012'],
                      df_dataflow['color_1013']
                      ],
                     ignore_index=True)

df_color_result = pd.DataFrame({'link_color': df_color}).dropna()

# merge final dataframe together
data_frames = [df_source_result, df_target_result, df_color_result]
df_final = pd.concat(data_frames, join='outer', axis=1).assign(value=1)

# df_final.to_csv('links.csv', index=False)

print("df_final: ")
print(df_final)

# ----PLOT SANKEY------#
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=15,
        line=dict(
            color='white',
            width=1
        ),
        label=df_dataflow['node_name'].dropna(axis=0, how='any'),
        color=df_dataflow['color'].dropna(axis=0, how='any')
    ),
    link=dict(
        target=df_final['source'].dropna(axis=0, how='any'),
        source=df_final['target'].dropna(axis=0, how='any'),
        value=df_final['value'].dropna(axis=0, how='any'),
        color=df_final['link_color'].dropna(axis=0, how='any')
    )
)])

fig.update_layout(height=700,
                  width=900,
                  hovermode='y', )

# ---DISPLAY SANKEY IN STREAMLIT-----#
st.plotly_chart(fig)
