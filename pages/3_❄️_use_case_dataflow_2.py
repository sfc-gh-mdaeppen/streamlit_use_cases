import graphviz
import pandas as pd
import streamlit as st

pd.options.display.max_columns = None

st.set_page_config(layout="wide")

df_raw = pd.read_excel('2024-01-02_UseCase_maturity_map_for_FSI.xlsx', header=1,
                       sheet_name='use_case_master_dataflow',
                       converters={'uc_id': int,
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

# context selection
unit = df_raw['unit'].dropna().loc[lambda x: x != 'DataSource'].unique()
unit_choice = st.sidebar.selectbox('Select your Business Unit:', unit)

sub_unit = df_raw['sub_unit'].loc[df_raw['unit'] == unit_choice].unique()
sub_unit_choice = st.sidebar.multiselect('Select your Use Case Category:', sub_unit, default=sub_unit[0])

use_case = ((df_raw['node_name']).loc[(df_raw['unit'] == unit_choice) &
                                      (df_raw['sub_unit'].isin(
                                          sub_unit_choice))].unique())

use_case_choice = st.sidebar.multiselect('Select your Use Cases:', use_case, default=use_case[1])

df_filtered = df_raw.loc[(df_raw['node_name'].isin(use_case_choice))]

df_target = pd.concat([df_filtered['target_1000'],
                       df_filtered['target_1001'],
                       df_filtered['target_1002'],
                       df_filtered['target_1003'],
                       df_filtered['target_1004'],
                       df_filtered['target_1010'],
                       df_filtered['target_1011'],
                       df_filtered['target_1012'],
                       df_filtered['target_1013']
                       ],
                      ignore_index=True)

# Create a DataFrame from the concatenated result
df_target_result = pd.DataFrame({'target': df_target}).dropna()

df_source = pd.concat([df_filtered['source_1000'],
                       df_filtered['source_1001'],
                       df_filtered['source_1002'],
                       df_filtered['source_1003'],
                       df_filtered['source_1004'],
                       df_filtered['source_1010'],
                       df_filtered['source_1011'],
                       df_filtered['source_1012'],
                       df_filtered['source_1013']
                       ],
                      ignore_index=True)

df_source_result = pd.DataFrame({'source': df_source}).dropna()

df_color = pd.concat([df_filtered['color_1000'],
                      df_filtered['color_1001'],
                      df_filtered['color_1002'],
                      df_filtered['color_1003'],
                      df_filtered['color_1004'],
                      df_filtered['color_1010'],
                      df_filtered['color_1011'],
                      df_filtered['color_1012'],
                      df_filtered['color_1013']
                      ],
                     ignore_index=True)

df_color_result = pd.DataFrame({'link_color': df_color}).dropna()

# merge final dataframe together
agg_data_frames = [df_source_result, df_target_result, df_color_result]
df_final = pd.concat(agg_data_frames, join='outer', axis=1)

df_final_enhanced = df_final.merge(df_raw[['uc_id', 'node_name']], how='inner', left_on='target', right_on='uc_id',
                                   validate="many_to_many")

df_final_enhanced = df_final_enhanced.merge(df_raw[['uc_id', 'node_name']], how='inner', left_on='source',
                                            right_on='uc_id', validate="many_to_many")

df_final_enhanced.to_csv('links.csv', index=False)

# Create Graph Nodes and interconnecting Edges
graph = graphviz.Graph("jupyter_moons", comment="Jupyter moons")

for index, row in df_final_enhanced.iterrows():
    graph.node(name=str(row["source"]),
               label=str(row["node_name_y"]),
               href="http://localhost:8501/use_case_details/?uc_id=" + str(row["uc_id_y"]))

    graph.edge(str(row["source"]), str(row["target"]), str(row["node_name_x"]))

#  add href to link URL="http://localhost:8501/test_3/?uc_id=" + str(row["uc_id_x"])

st.graphviz_chart(graph)
