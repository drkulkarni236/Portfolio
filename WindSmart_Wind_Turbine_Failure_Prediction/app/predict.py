import pandas as pd
import numpy as np
import joblib

#load model
pipeline = joblib.load('pipeline.pkl')

# load data
df = pd.read_csv('./data/df_clean.csv')

# model
x_cols = [
    'Gen_RPM_Avg','Gen_Bear_Temp_Avg','Gen_Phase1_Temp_Avg','Gen_Phase2_Temp_Avg','Gen_Phase3_Temp_Avg','Hyd_Oil_Temp_Avg','Gear_Oil_Temp_Avg','Gear_Bear_Temp_Avg','Nac_Temp_Avg',
    'HVTrafo_Phase1_Temp_Avg','HVTrafo_Phase2_Temp_Avg','HVTrafo_Phase3_Temp_Avg','Grd_InverterPhase1_Temp_Avg','Cont_Top_Temp_Avg','Cont_Hub_Temp_Avg','Cont_VCP_Temp_Avg',
    'Rtr_RPM_Avg','Amb_WindSpeed_Avg','Grd_Prod_Pwr_Avg']

df_x = df[['Timestamp','Turbine_ID'] + x_cols + ['status','logs_Remark','fail_Remark']].dropna(how='any', subset=x_cols)
x = df_x[x_cols].values

# predict
log_likelihood = pipeline.score_samples([x[1]])