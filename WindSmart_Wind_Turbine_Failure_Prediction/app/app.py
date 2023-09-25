from flask import Flask, render_template
import pandas as pd
import numpy as np
from sklearn import pipeline
import joblib

# load model
# pipeline = joblib.load('pipeline.pkl')

# # load data
# df = pd.read_csv('./data/df_clean.csv')
x_cols = [
    'Gen_RPM_Avg','Gen_Bear_Temp_Avg','Gen_Phase1_Temp_Avg','Gen_Phase2_Temp_Avg','Gen_Phase3_Temp_Avg','Hyd_Oil_Temp_Avg','Gear_Oil_Temp_Avg','Gear_Bear_Temp_Avg','Nac_Temp_Avg',
    'HVTrafo_Phase1_Temp_Avg','HVTrafo_Phase2_Temp_Avg','HVTrafo_Phase3_Temp_Avg','Grd_InverterPhase1_Temp_Avg','Cont_Top_Temp_Avg','Cont_Hub_Temp_Avg','Cont_VCP_Temp_Avg',
    'Rtr_RPM_Avg','Amb_WindSpeed_Avg','Grd_Prod_Pwr_Avg']

# df_x = df[['Timestamp','Turbine_ID'] + x_cols + ['status','logs_Remark','fail_Remark']].dropna(how='any', subset=x_cols)

# # predict 
# log_likelihood = pipeline.score_samples(df_x[x_cols].values)
# classes = pipeline.predict(df_x[x_cols].values)
# df_x['gmm_class'] = classes
# df_x['log_likelihood'] = log_likelihood
# df_x['anomaly'] = [log_likelihood < -21][0]
# df_x.anomaly = df_x.anomaly.astype(int)

# # calculate feature contribution
# gmm_model = pipeline.named_steps['gmm']
# scaler = pipeline.named_steps['normalization']
# means_dict = {}
# for c in df_x['gmm_class'].unique():
#     means_dict[c] = gmm_model.means_[c]

# def feature_contr(row):
#     means = means_dict[row['gmm_class']]
#     scaled_vector = scaler.transform([row[x_cols].tolist()])[0]
#     distances = np.abs(scaled_vector - means)
#     distances_sort = distances.copy()
#     distances_sort.sort()

#     highest_1 = x_cols[distances.tolist().index(distances_sort[-1])]
#     highest_2 = x_cols[distances.tolist().index(distances_sort[-2])]
#     highest_3 = x_cols[distances.tolist().index(distances_sort[-3])]

#     return [highest_1, highest_2, highest_3]

# df_x[['highest_1', 'highest_2', 'highest_3']] = df_x.apply(feature_contr, axis=1, result_type='expand')

# # evaluate anomaly as indicator for failures in future time window
# w = int(60*24*7/10)*3 # weeks window
# f = int(60*24*7/10)*4 # weeks ahead for window start
# df_x['fail'] = np.where(df_x.status.isin(['off','failure']), 1, 0)
# df_x['fut_fail'] = np.where(df_x.status.isin(['off','failure']), 1, 0)
# df_x.fut_fail = df_x.groupby('Turbine_ID')['fut_fail'].rolling(window=w, min_periods=1).max().reset_index(level=0, drop=True)
# df_x.fut_fail = df_x.groupby(['Turbine_ID'])['fut_fail'].shift(-f - w)

# # save to file
# df_x.to_csv('df_computed.csv', index=None)

# read from file
df_x = pd.read_csv('df_computed.csv')

#_____ app
app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/get_t01_data', methods=['POST'])
def get_t01_data():

    # generate the series
    df = df_x[df_x.Turbine_ID=='T01']
    series_data = df[['Timestamp','log_likelihood', 'anomaly','fut_fail', 'highest_1', 'highest_2', 'highest_3']].replace(np.nan, None).values.tolist()

    series_signal = {}
    for col in x_cols:
        series_signal[col] = df[['Timestamp', col]].replace(np.nan, None).values.tolist()
    
    
    # Gen_RPM_Avg_contr = df[['Timestamp','Gen_RPM_Avg_contr']].replace(np.nan, None).values.tolist()
    true_anom_data = df[(df.anomaly==1)&(df.fut_fail==1)][['Timestamp','log_likelihood']].replace(np.nan, None).values.tolist()
    false_anom_data = df[(df.anomaly==1)&(df.fut_fail!=1)][['Timestamp','log_likelihood']].replace(np.nan, None).values.tolist()
    series_dates = df.Timestamp.values.tolist()

    data = {
        'serieData': series_data, 
        'anomDataTrue': true_anom_data, 'anomDataFalse': false_anom_data, 
        'series_signal': series_signal,
        'dates': series_dates}
    return data

@app.route('/get_t06_data', methods=['POST'])
def get_t06_data():

    # generate the series
    df = df_x[df_x.Turbine_ID=='T06']
    series_data = df[['Timestamp','log_likelihood', 'anomaly','fut_fail', 'highest_1', 'highest_2', 'highest_3']].replace(np.nan, None).values.tolist()

    series_signal = {}
    for col in x_cols:
        series_signal[col] = df[['Timestamp', col]].replace(np.nan, None).values.tolist()
    
    
    # Gen_RPM_Avg_contr = df[['Timestamp','Gen_RPM_Avg_contr']].replace(np.nan, None).values.tolist()
    true_anom_data = df[(df.anomaly==1)&(df.fut_fail==1)][['Timestamp','log_likelihood']].replace(np.nan, None).values.tolist()
    false_anom_data = df[(df.anomaly==1)&(df.fut_fail!=1)][['Timestamp','log_likelihood']].replace(np.nan, None).values.tolist()
    series_dates = df.Timestamp.values.tolist()

    data = {
        'serieData': series_data, 
        'anomDataTrue': true_anom_data, 'anomDataFalse': false_anom_data, 
        'series_signal': series_signal,
        'dates': series_dates}
    return data

@app.route('/get_t07_data', methods=['POST'])
def get_t07_data():

    # generate the series
    df = df_x[df_x.Turbine_ID=='T07']
    series_data = df[['Timestamp','log_likelihood', 'anomaly','fut_fail', 'highest_1', 'highest_2', 'highest_3']].replace(np.nan, None).values.tolist()

    series_signal = {}
    for col in x_cols:
        series_signal[col] = df[['Timestamp', col]].replace(np.nan, None).values.tolist()
    
    
    # Gen_RPM_Avg_contr = df[['Timestamp','Gen_RPM_Avg_contr']].replace(np.nan, None).values.tolist()
    true_anom_data = df[(df.anomaly==1)&(df.fut_fail==1)][['Timestamp','log_likelihood']].replace(np.nan, None).values.tolist()
    false_anom_data = df[(df.anomaly==1)&(df.fut_fail!=1)][['Timestamp','log_likelihood']].replace(np.nan, None).values.tolist()
    series_dates = df.Timestamp.values.tolist()

    data = {
        'serieData': series_data, 
        'anomDataTrue': true_anom_data, 'anomDataFalse': false_anom_data, 
        'series_signal': series_signal,
        'dates': series_dates}
    return data

@app.route('/get_t11_data', methods=['POST'])
def get_t11_data():

    # generate the series
    df = df_x[df_x.Turbine_ID=='T11']
    series_data = df[['Timestamp','log_likelihood', 'anomaly', 'fut_fail', 'highest_1', 'highest_2', 'highest_3']].replace(np.nan, None).values.tolist()

    series_signal = {}
    for col in x_cols:
        series_signal[col] = df[['Timestamp', col]].replace(np.nan, None).values.tolist()
    
    
    # Gen_RPM_Avg_contr = df[['Timestamp','Gen_RPM_Avg_contr']].replace(np.nan, None).values.tolist()
    true_anom_data = df[(df.anomaly==1)&(df.fut_fail==1)][['Timestamp','log_likelihood']].replace(np.nan, None).values.tolist()
    false_anom_data = df[(df.anomaly==1)&(df.fut_fail!=1)][['Timestamp','log_likelihood']].replace(np.nan, None).values.tolist()
    series_dates = df.Timestamp.values.tolist()

    data = {
        'serieData': series_data, 
        'anomDataTrue': true_anom_data, 'anomDataFalse': false_anom_data, 
        'series_signal': series_signal,
        'dates': series_dates}
    return data