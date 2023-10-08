import numpy as np
import pandas as pd
import matplotlib_inline as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics
import xgboost as xgb


data = pd.read_csv('Forecasting.csv' ,encoding = 'unicode_escape')
data[['Day', 'Month','Year']] = data['Date'].str.split('-', expand=True)
data.drop('Date',axis = 1,inplace = True)


from sklearn.preprocessing import OrdinalEncoder
ordinal_encoder = OrdinalEncoder()
data['Time'] = ordinal_encoder.fit_transform(data[['Time']])
for column in data.columns:
    if data[column].dtypes == 'object':
        data[column] = data[column].astype(int)
        
        
x = data.drop(['Temperature (°C)', 'Humidity (%)'],axis=1).values
y = data[['Temperature (°C)', 'Humidity (%)']].values
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.25, random_state=365)



# def regression_results(y_true, y_pred):

#     # Regression metrics
#     explained_variance=metrics.explained_variance_score(y_true, y_pred)
#     mean_absolute_error=metrics.mean_absolute_error(y_true, y_pred) 
#     mse=metrics.mean_squared_error(y_true, y_pred) 
#     mean_squared_log_error=metrics.mean_squared_log_error(y_true, y_pred)
#     median_absolute_error=metrics.median_absolute_error(y_true, y_pred)
#     r2=metrics.r2_score(y_true, y_pred)

#     print('explained_variance: ', round(explained_variance,4))    
#     print('mean_squared_log_error: ', round(mean_squared_log_error,4))
#     print('r2: ', round(r2,4))
#     print('MAE: ', round(mean_absolute_error,4))
#     print('MSE: ', round(mse,4))
#     print('RMSE: ', round(np.sqrt(mse),4))
    
    

reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
        n_estimators=1000,
        early_stopping_rounds=50,
        objective='reg:linear',
        max_depth=3,
        learning_rate=0.01,
    )

reg.fit(x_train, y_train,
        eval_set=[(x_train, y_train), (x_test, y_test)],
        verbose=100)


import random
predictions = []

for hour in range(24):
    if hour > 0 and hour < 10:
        air_moisture = random.uniform(55, 80)
        dew_point = random.uniform(13, 21)
        predictions.append([hour,air_moisture,dew_point])

    elif hour >= 10 and hour < 18:
        air_moisture = random.uniform(30, 40)
        dew_point = random.uniform(14, 23)
        predictions.append([hour,air_moisture,dew_point])

    elif hour >= 18 and hour < 21:
        air_moisture = random.uniform(40, 55)
        dew_point = random.uniform(16, 25)
        predictions.append([hour,air_moisture,dew_point])

    else :
        air_moisture = random.uniform(55, 60)
        dew_point = random.uniform(13, 18)
        predictions.append([hour,air_moisture,dew_point])
        
    
predict = []
for i in predictions:
    predict.append(reg.predict([i]))
    
    
new_data = []
for i in range(len(predictions)):
    new_data.append([predictions[i][0],round(predict[i][0][1],2),int(predict[i][0][0])])