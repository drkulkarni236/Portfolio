import pandas as pd
import numpy as np
from sklearn import preprocessing, pipeline
from sklearn.mixture import GaussianMixture
from sklearn.metrics import confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

#_____ load data
df = pd.read_csv('./data/df_clean.csv')

x_cols = [
    'Gen_RPM_Avg','Gen_Bear_Temp_Avg','Gen_Bear2_Temp_Avg','Gen_Phase1_Temp_Avg','Gen_Phase2_Temp_Avg','Gen_Phase3_Temp_Avg','Hyd_Oil_Temp_Avg','Gear_Oil_Temp_Avg','Gear_Bear_Temp_Avg','Nac_Temp_Avg',
    'HVTrafo_Phase1_Temp_Avg','HVTrafo_Phase2_Temp_Avg','HVTrafo_Phase3_Temp_Avg','Grd_InverterPhase1_Temp_Avg','Cont_Top_Temp_Avg','Cont_Hub_Temp_Avg','Cont_VCP_Temp_Avg',
    'Gen_SlipRing_Temp_Avg','Spin_Temp_Avg',
    'Rtr_RPM_Avg','Grd_Prod_Pwr_Avg',
    'Amb_Temp_Avg','Amb_WindSpeed_Avg']
df_x = df[['Timestamp','Turbine_ID'] + x_cols + ['status','logs_Remark','fail_Remark']]

# data imputation
ffil_cols = [
    'Gen_Bear_Temp_Avg','Gen_Bear2_Temp_Avg','Gen_Phase1_Temp_Avg','Gen_Phase2_Temp_Avg','Gen_Phase3_Temp_Avg','Hyd_Oil_Temp_Avg','Gear_Oil_Temp_Avg','Gear_Bear_Temp_Avg','Nac_Temp_Avg',
    'HVTrafo_Phase1_Temp_Avg','HVTrafo_Phase2_Temp_Avg','HVTrafo_Phase3_Temp_Avg','Grd_InverterPhase1_Temp_Avg','Cont_Top_Temp_Avg','Cont_Hub_Temp_Avg','Cont_VCP_Temp_Avg',
    'Gen_SlipRing_Temp_Avg','Spin_Temp_Avg',
    'Amb_Temp_Avg','Amb_WindSpeed_Avg']
df_x[ffil_cols] = df_x.groupby(['Turbine_ID'])[ffil_cols].ffill()

zfil_cols = ['Gen_RPM_Avg', 'Rtr_RPM_Avg', 'Grd_Prod_Pwr_Avg']
df_x[zfil_cols] = df_x[zfil_cols].fillna(0)

#_____ normalize df
# df_x[x_cols] = (df_x[x_cols] - df_x[x_cols].mean()) / df_x[x_cols].std()
x = df_x[x_cols].values

#_____ pipeline
steps = [
    ('normalization', preprocessing.StandardScaler()),  # Normalization step
    ('gmm', GaussianMixture(n_components=8))  # GMM model step
]

# Create the pipeline
pipeline = pipeline.Pipeline(steps)

# Fit the pipeline to the data
pipeline.fit(x)

# save model
# joblib.dump(pipeline, 'pipeline.pkl')
# pipeline = joblib.load('pipeline.pkl')

# Use the pipeline for prediction
predictions = pipeline.predict(x)
log_likelihood = pipeline.score_samples(x)

#_____ threshold
best = -1
for th in np.arange(np.percentile(log_likelihood, 0.025), np.percentile(log_likelihood, 0.975), 0.5):
    df_x['anomaly'] = [log_likelihood < th][0]

    # evaluate anomaly as indicator for failures in future time window
    w = int(60*24*7/10)*3 # weeks window
    f = int(60*24*7/10)*4 # weeks ahead for window start

    df_x['fail'] = np.where(df_x.status.isin(['off','failure']), 1, 0)
    df_x['fut_fail'] = np.where(df_x.status.isin(['off','failure']), 1, 0)
    df_x.fut_fail = df_x.groupby('Turbine_ID')['fut_fail'].rolling(window=w, min_periods=1).max().reset_index(level=0, drop=True)
    df_x.fut_fail = df_x.groupby(['Turbine_ID'])['fut_fail'].shift(-f - w)

    precision = (df_x[df_x.anomaly==1].anomaly * df_x[df_x.anomaly==1].fut_fail).mean()
    perc_anom = df_x.anomaly.mean() * 100
    tot_anom = df_x.anomaly.sum()
    if precision > best:
        best = precision
        result = (th, precision, perc_anom, tot_anom)
print(result)

# select th
th = -32
df_x['anomaly'] = [log_likelihood < th][0]

# evaluate anomaly as indicator for failures in future time window
w = int(60*24*7/10)*3 # weeks window
f = int(60*24*7/10)*4 # weeks ahead for window start

df_x['fail'] = np.where(df_x.status.isin(['off','failure']), 1, 0)
df_x['fut_fail'] = np.where(df_x.status.isin(['off','failure']), 1, 0)
df_x.fut_fail = df_x.groupby('Turbine_ID')['fut_fail'].rolling(window=w, min_periods=1).max().reset_index(level=0, drop=True)
df_x.fut_fail = df_x.groupby(['Turbine_ID'])['fut_fail'].shift(-f - w)

precision = (df_x[df_x.anomaly==1].anomaly * df_x[df_x.anomaly==1].fut_fail).mean()
perc_anom = df_x.anomaly.mean() * 100
tot_anom = df_x.anomaly.sum()

print(th, precision, perc_anom, tot_anom)

for t in ['T01','T06','T07','T11']:
    dfp = df_x[df_x.Turbine_ID==t].dropna(subset=['fut_fail','anomaly'])
    cm = confusion_matrix(dfp.fut_fail, dfp.anomaly)

    precision = (dfp[dfp.anomaly==1].anomaly * dfp[dfp.anomaly==1].fut_fail).mean()

    labels = ['No Failure', 'Failure']
    plt.figure(figsize=(3, 1.6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.xlabel('Predicted Failures', fontsize=8)
    plt.ylabel('True Failures', fontsize=8)
    plt.title(f'Turbine {t}, prec={np.round(precision*100,1)}%', fontsize=10)
    plt.show()

for t in df_x.status.unique():
    dfp = df_x[df_x.status==t].dropna(subset=['fut_fail','anomaly'])
    cm = confusion_matrix(dfp.fut_fail, dfp.anomaly)

    precision = (dfp[dfp.anomaly==1].anomaly * dfp[dfp.anomaly==1].fut_fail).mean()

    labels = ['No Failure', 'Failure']
    plt.figure(figsize=(3, 1.6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.xlabel('Predicted Failures', fontsize=8)
    plt.ylabel('True Failures', fontsize=8)
    plt.title(f'Status {t}, prec={np.round(precision*100,1)}%', fontsize=10)
    plt.show()

# save model
joblib.dump(pipeline, 'pipeline.pkl')