import streamlit as st
import pandas as pd
import altair as alt
import des_lib as lib

import streamlit.components.v1 as components

# if you dont know how to read the go to this site https://docs.streamlit.io/

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.write("""
APP 372
# DOUBLE EXPONENTIAL SMOOTHING
""")

alpha = st.number_input('Input Alpha', min_value=0.00, max_value=1.00, step=0.10,format='%2f', key='alpha')

beta = st.number_input('Input Beta', min_value=0.00, max_value=1.00, step=0.10,format='%2f', key='beta')

option = st.selectbox('How would you like to be contacted?',('---- Select ----','caspea', 'baby breath', 'silver dollar'))



if option != '---- Select ----' :
    df = lib.calculate(alpha, beta, option)

    st.success(f"RSME : {df['rsme']}")
    st.markdown("<h2 style='text-align: center; color: black;'>Chart Forecast</h2>", unsafe_allow_html=True)
    
    source = pd.DataFrame(df['chart'],
                    columns=['flower', 'forecast'], index=pd.RangeIndex(44, name='x'))
    source = source.reset_index().melt('x', var_name='category', value_name='y')

    line_chart = alt.Chart(source).mark_line(interpolate='basis').encode(
        alt.X('x', title='Week'),
        alt.Y('y', title='Selling and Forecast'),
        color='category:N'
    ).properties(
        title='Sales and Forecast of flower'
    )

    st.altair_chart(line_chart, use_container_width=True)

    # st.dataframe(source)

    st.markdown("<h3 style='text-align: center; color: black;'>Table Forecast</h3>", unsafe_allow_html=True)
    st.table(df['table'])
    st.markdown("<h3 style='text-align: center; color: black;'>4 Week Forecast</h3>", unsafe_allow_html=True)
    st.table(df['forecast'])