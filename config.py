MODEL_PATH = "./models/"
MODEL_TO_USE = "random_forest_final.pkl"
DATA_PATH = './data/df_complete.csv'
HOST = 'http://127.0.0.1:8000'
HEROKU_HOST = 'https://scoring-credit-oc-48975.herokuapp.com'
EMPTY_RESPONSE = {
    'error': {'status' : None,
              'client_id_sample' : None,
              },
    'data': None,
    }
COLUMNS_ORDER = [
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",
    "DAYS_BIRTH",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "DAYS_EMPLOYED",
    "AMT_GOODS_PRICE",
    "DAYS_ID_PUBLISH",
    "OWN_CAR_AGE",
    "BUREAU_MAX_DAYS_CREDIT",
    "BUREAU_MAX_DAYS_CREDIT_ENDDATE",
    "BUREAU_MAX_DAYS_ENDDATE_FACT",
    "PREV_SUM_MIN_AMT_PAYMENT",
    "PREV_MEAN_MIN_AMT_PAYMENT",
]
