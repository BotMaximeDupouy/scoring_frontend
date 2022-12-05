import io
import json

import pandas as pd
import requests
import streamlit as st

from config import HOST, HEROKU_HOST
from utils import create_gauge_plot


# Change parameter if app is on heroku
IS_DEPLOY=True
if IS_DEPLOY==True:
    HOST=HEROKU_HOST

## Load desc
f = open('./data/columns_descriptions.json')
columns_descriptions = json.load(f)
f = open('./data/multiples_descriptions.json')
multiple_desc = json.load(f)


st.set_page_config(layout="wide")


########################################### TITLE ###########################################
title = '<b><p style="font-family:sans-serif; font-size: 45px;text-align: center;">🔮 Prêt-à-dépenser 🔮</b></p>'
st.markdown(title, unsafe_allow_html=True)
st.markdown(4 * "<br />", unsafe_allow_html=True)

########################################### SIDEBAR INPUTS ###########################################

client_id = st.sidebar.number_input('Insert client id',
                                    value=0)
payload = {
    "client_id": str(client_id)
    }

## GET DATA
response = requests.post(''.join([HOST,'/get_data/']),
                         json=payload
                         ).json()

## SITE DE BASE
if response["error"]["status"] and str(client_id) == "0":

    st.write(f'{multiple_desc["site_desc"]}')
    st.write(" ")
    st.write(multiple_desc["data_desc"])

## ID NOT FOUND
elif response["error"]["status"] and str(client_id) != "0":
    st.write('<p style="font-family:sans-serif; font-size: 25px;text-align: center;">⚠️ ERROR ⚠️</p>', unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.write('This ID does not match __any customer ID__ in the database 😱😱😱')
    st.write("Examples of known identifiers:")
    st.write(', '.join([str(i) for i in eval(response["error"]["client_id_sample"])]))


## LET THE MAGIE BEGGINS
else :

    # DATA_df FROM RESPONSE
    data = pd.DataFrame(eval(response["data"]))
    # CLIENT DATA
    client_value = data.loc[:, 'client_value']

    # INPUT HOWMANY FEATURE TO ANALYSED
    st.sidebar.write('______________________________')
    st.sidebar.write(' ')

    number_features_to_eval = int(st.sidebar.selectbox(
        'Features range you want to analyse',
        ["2", "3", "4"]))

    st.sidebar.write('______________________________')
    st.sidebar.write(' ')

    # SLIDER FOR MOST IMPACTFUL FEATURES
    st.sidebar.write(f'*Most {str(number_features_to_eval)} impactful features for selected client :*')

    # iterate over n MOST IMPACTFUL FEATURES
    for feature_name, data_feature in data.iloc[:number_features_to_eval,
                                                :].iterrows():

        # possibility to click for feature description
        if st.sidebar.button(f'Show {feature_name} description'):
            st.sidebar.write(columns_descriptions[feature_name])

        # instanciate sidebar to input new feature value
        values = st.sidebar.slider(
        f'Select value for {feature_name}',
        min_value=float(data.loc[feature_name, 'min_value']),
        max_value=float(data.loc[feature_name, 'max_value']),
        value=float(data.loc[feature_name, 'client_value']),
        step=(data.loc[feature_name, 'max_value']-data.loc[feature_name, 'min_value'])/1000
        )
        # replace client_data value by feature input
        data.loc[feature_name, 'client_value'] = values

    ########################################### PREDICTION ###########################################
    prediction = requests.post(''.join([HOST,'/predict/']),
                               json=client_value.to_dict()).json()
    prediction, probalitie = prediction["prediction"], float(prediction['probabilies'])

    col1, col2 = st.columns(2)

    with col1:
        to_display = multiple_desc[prediction]
        title = f'<p style="font-family:sans-serif; font-size: 28px;text-align: center;">{to_display}</p>'
        st.markdown(title, unsafe_allow_html=True)
    with col2:
        fig = create_gauge_plot(probalitie)
        st.plotly_chart(fig)

    ########################################### GRAPHS ###########################################
    graph_params = {
        "feature": None,
        "data_client": client_value.to_dict(),
        "client_id":client_id,
        "which_graph": None,
        "prediction": prediction if prediction else None
    }

    ######## FORCE PLOT
    with st.expander("See features empact on prediction"):
        st.write(f"Explanation for the {'credit acceptance' if prediction=='0' else 'refusal of credit'}.")
        st.write(multiple_desc["force_plot_desc"])
        graph_params['which_graph']='force_plot'
        force_plot_graph = requests.get(''.join([HOST, '/']),
                                                 json=graph_params)
        with io.BytesIO(force_plot_graph.content) as f:
            st.image(f, width=1000)

    ######## FEATURE IMPORTANCE GRAPH
    with st.expander("See models explanation"):
        st.write(multiple_desc['feature_desc'])
        # récupere le graph
        graph_params['which_graph']='features_importance_model'
        features_importance_model = requests.get(''.join([HOST, '/']),
                                                 json=graph_params)
        with io.BytesIO(features_importance_model.content) as f:
            st.image(f, width=850)


    ######## BOXPLOTS
    with st.expander("See features distribution"):
        st.write(multiple_desc["box_plot_desc"])

        graph_params['which_graph']='client_distribution'

        feature_to_boxplot = client_value.index[:number_features_to_eval]
        graph_to_display = []
        for ind, feature in enumerate(feature_to_boxplot):
            graph_params["feature"] = feature
            test = requests.get(''.join([HOST, '/']),
                                            json=graph_params)
            graph_to_display.append(test.content)

        # UGLY PART TO DISPLAY BOXPLOTS IN COLUMNS
        col1, col2 = st.columns(2)
        with col1:
            with io.BytesIO(graph_to_display[0]) as f:
                st.image(f, width=500)
            if len(graph_to_display) > 2:
                with io.BytesIO(graph_to_display[2]) as f:
                    st.image(f, width=500)
        with col2:
            with io.BytesIO(graph_to_display[1]) as f:
                st.image(f, width=500)
            if len(graph_to_display) == 4 :
                with io.BytesIO(graph_to_display[3]) as f:
                    st.image(f, width=500)



st.markdown(10 * "<br />", unsafe_allow_html=True)
st.write(multiple_desc["contact"])
