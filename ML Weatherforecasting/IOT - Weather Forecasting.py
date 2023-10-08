#!/usr/bin/env python
# coding: utf-8

# In[1]:


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



def regression_results(y_true, y_pred):

    # Regression metrics
    explained_variance=metrics.explained_variance_score(y_true, y_pred)
    mean_absolute_error=metrics.mean_absolute_error(y_true, y_pred) 
    mse=metrics.mean_squared_error(y_true, y_pred) 
    mean_squared_log_error=metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error=metrics.median_absolute_error(y_true, y_pred)
    r2=metrics.r2_score(y_true, y_pred)

    print('explained_variance: ', round(explained_variance,4))    
    print('mean_squared_log_error: ', round(mean_squared_log_error,4))
    print('r2: ', round(r2,4))
    print('MAE: ', round(mean_absolute_error,4))
    print('MSE: ', round(mse,4))
    print('RMSE: ', round(np.sqrt(mse),4))
    
    

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


# In[2]:


regression_results(y_test,reg.predict(x_test))


# In[3]:


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


# In[4]:


for i in range(len(predictions)):
    if i >= 1  and i <= 11:
        print('At:' , predictions[i][0],'AM', ' the Humdidty is' ,  round(predict[i][0][1],2),'%')
    elif i ==12:
        print('At:' , predictions[i][0],'PM', ' the Humdidty is' ,  round(predict[i][0][1],2),'%')
    elif i == 0:
        print('At:' ,'12','AM', ' the Humidity is' ,  round(predict[i][0][1],2),'%')
    else:
        print('At:' , predictions[i][0]-12,'PM', ' the Humdidty is' ,  round(predict[i][0][1],2),'%')
        


# In[5]:


for i in range(len(predictions)):
    if i >= 1  and i <= 11:
        print('At:' , predictions[i][0],'AM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
    elif i ==12:
        print('At:' , predictions[i][0],'PM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
    elif i == 0:
        print('At:' ,'12','AM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
    else :
        print('At:' , predictions[i][0]-12,'PM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')


# In[6]:


def Weathre_forecasting():
    
    print('Hello User,How are You ..!\n')
    name = str(input('Enter your Name sir: '))
    print(f'\nHello {name}, I\'m Rawi, your Guide for Weather Forecast\n','Do you want to know my story?')    
    Answer = str(input('[Y] or [N] : '))
    flag = True
    while flag:       
        if Answer.lower() == 'y':   
            print('''\nmy brith place is 7-10-2023 created by a group of students at SIC-IOT course, 
            they used to call me predictor,')
            because, some times i forecast far values from the true ones, but i decided to develop my self,')
            so i trained well at Gym is called (XGboost), it cost me 4 seconds to make be Artificial BIG RAMY.')
            Let\'s Get Started:''')

        elif Answer.lower() == 'n':
            print('Sorry for Annoying you')
            print('Let\'s Go :')
            flag = False

        else:
            print('Invalid input. Please enter a valid Answer.')
            print('---------------------------------------')
            print(f'Do, You want to repeate the process {name}?\n')
            user_choice = str(input(f'Answer with Yes or No {name}\n'))
            if user_choice.lower() == 'yes':
                Weathre_forecasting()
            elif user_choice.lower() == 'no':
                flag = False
            else:
                print(f'Invalid input{name}. Please enter a valid Previewing Time.\n')
                print('-----------------------------------------------------')
                print(f'Do, You want to repeate last process {name}?\n')
                user_choice = str(input(f'Answer with Yes or No {name}\n'))
                if user_choice.lower() == 'yes':
                    Weathre_forecasting()
                else:
                    flag = False
                
            


        
        
        def Hour_Presentation():
            Flage = True
            
            while Flage:
                
                hour_system = int(input('\nYou want 12 o\'clock system or 24 o\'clock ?\n'))
                
                if hour_system == 12:
                    hour_forecast = int(input('Choose The preferred time please: '))
                    time_zone = str(input('AM or PM {ahmed}: '))
                    
                    if hour_forecast < 13 and time_zone.lower() =='am' :
                
                        if  hour_forecast >= 1  and hour_forecast <= 11:
                            print('\nAt:' , predictions[hour_forecast][0],'AM', ' the Temprature is' ,  int(predict[hour_forecast][0][0]),'°C')
                            print('At:' , predictions[hour_forecast][0],'AM', ' the Humdidty is' ,  round(predict[hour_forecast][0][1],2),'%')
                            Flage = False


                        elif hour_forecast == 0 or hour_forecast ==12:
                            print('\nAt:' ,'12','AM', ' the Temprature is' ,  int(predict[0][0][0]),'°C')
                            print('At:' ,'12','AM', ' the Humidity is' ,  round(predict[0][0][1],2),'%')
                            Flage = False

                        
                    
                    elif hour_forecast < 13 and time_zone.lower() =='pm' :
                        if hour_forecast == 12 :
                            print('\nAt:' ,'12','PM', ' the Temprature is' ,  int(predict[12][0][0]),'°C')
                            print('At:' ,'12','PM', ' the Humidity is' ,  round(predict[12][0][1],2),'%')
                            Flage = False
                        else:    
                            print('\nAt:' , predictions[hour_forecast][0],'PM', ' the Temprature is' ,  int(predict[hour_forecast + 12][0][0]),'°C')
                            print('At:' , predictions[hour_forecast][0],'PM', ' the Humdidty is' ,  round(predict[hour_forecast + 12][0][1],2),'%')
                            Flage = False
                    
                    
                    else:
                        print('Invalid input. Please enter a valid Previewing Time.\n')
                        print(f'Do, You want to repeate last process {name}?\n')
                        user_choice = str(input(f'Answer with Yes or No {name}\n'))
                        if user_choice.lower() == 'yes':
                            Hour_Presentation()
                        elif user_choice.lower() == 'no':
                            Flage = False
                        else:
                            print('Invalid input. Please enter a valid Hour or Time Zone for Time Prediction System.\n')
                            print('-----------------------------------------------------')
                            print(f'Do, You want to repeate last process {name}?\n')
                            user_choice = str(input(f'Answer with Yes or No {name}\n'))
                            if user_choice.lower() == 'yes':
                                Hour_Presentation()
                            else:
                                Flage = False
            
                            
                elif hour_system == 24:
                    hour_forecast = int(input('Choose The preferred time please: '))
                    if hour_forecast < 12:
                        print('\nAt:' , predictions[hour_forecast][0],'AM', ' the Temprature is' ,  int(predict[hour_forecast][0][0]),'°C')
                        print('\nAt:' , predictions[hour_forecast][0],'AM', ' the Humdidty is' ,  round(predict[hour_forecast][0][1],2),'%')
                        Flage = False
                    
                    elif hour_forecast >= 12 and hour_forecast <24:
                        print('\nAt:' , predictions[hour_forecast][0],'PM', ' the Temprature is' ,  int(predict[hour_forecast][0][0]),'°C')
                        print('\nAt:' , predictions[hour_forecast][0],'PM', ' the Humdidty is' ,  round(predict[hour_forecast][0][1],2),'%')
                        Flage = False
                        
                    else:
                        
                        print('Invalid input. Please enter a valid Previewing Time.\n')
                        print('-----------------------------------------------------')
                        print(f'Do, You want to repeate last process {name}?\n')
                        user_choice = str(input(f'Answer with Yes or No {name}\n'))
                        while True:
                            if user_choice.lower() == 'yes':
                                Hour_Presentation()
                            elif user_choice.lower() == 'no':
                                Flage = False
                            else:
                                print('Invalid input. Please enter a valid Previewing Time.\n')
                                print(f'Do, You want to repeate last process {name}?\n')
                                user_new_choice = str(input(f'Answer with Yes or No {name}\n'))
                                if user_new_choice.lower() == 'yes':
                                    Hour_Presentation()
                                else:
                                    Flage = False

                else:

                    print(f'Hey {name} ..., Do you kidding with me, there is error and it here: \n')
                    print('Invalid input. Please enter a valid Previewing Time.\n')
                    print('-----------------------------------------------------')
                    print(f'Do, You want to repeate last process {name}?\n')
                    user_choice = str(input(f'Answer with Yes or No {name}\n'))
                    if user_choice.lower() == 'yes':
                        Hour_Presentation()
            
                    elif user_choice.lower() == 'no':
                        Flage = False
                    else:
                        print('Invalid input. Please enter a valid Previewing Time.\n')
                        print('-----------------------------------------------------')
                        print(f'Do, You want to repeate last process {name}?\n')
                        user_choice = str(input(f'Answer with Yes or No {name}\n'))
                        if user_choice.lower() == 'yes':
                            Hour_Presentation()
                        else:
                            Flage = False
        
        Hour_Presentation()
        Flage = False


# In[7]:


import webbrowser

def url_implement():
# URL you want to open
    url = '''http://localhost:3000/d/bda08bba-9558-420e-90b7-69b3b09f52d0/
    temprature-data-sheet?orgId=1&from=1696507274244&to=1696852874246'''

# Open the URL in the default web browser
    webbrowser.open(url)


# In[8]:


url_implement()


# In[9]:



def preview_all_day_predictions():
   system_overview = int(input('\nYou want 12 o\'clock system or 24 o\'clock for previewing? :  \n'))
   
   if system_overview == 12:
       
       for i in range(len(predictions)):
           if  i >= 1  and i <= 11:
               print('\nAt:' , predictions[i][0],'AM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
               print('At:' , predictions[i][0],'AM', ' the Humdidty is' ,  round(predict[i][0][1],2),'%')

           elif i ==12:
               print('\nAt:' , predictions[i][0],'PM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
               print('At:' , predictions[i][0],'PM', ' the Humdidty is' ,  round(predict[i][0][1],2),'%')

           elif i == 0:
               print('\nAt:' ,'12','AM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
               print('At:' ,'12','AM', ' the Humidity is' ,  round(predict[i][0][1],2),'%')

           else :
               print('\nAt:' , predictions[i][0]-12,'PM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
               print('At:' , predictions[i][0]-12,'PM', ' the Humdidty is' ,  round(predict[i][0][1],2),'%')
       
   
   
   elif system_overview == 24:
       for i in range(len(predictions)):
           if i < 12 and i >= 1:
               print('\nAt:' , predictions[i][0],'AM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
               print('At:' , predictions[i][0],'AM', ' the Humdidty is' ,  round(predict[i][0][1],2),'%')
           elif i >= 12 and i <24:
               print('\nAt:' , predictions[i][0],'PM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
               print('At:' , predictions[i][0],'PM', ' the Humdidty is' ,  round(predict[i][0][1],2),'%')
           elif i == 0:
               print('\nAt:' , 12,'AM', ' the Temprature is' ,  int(predict[i][0][0]),'°C')
               print('At:' ,  12,'AM', ' the Humdidty is' ,  round(predict[i][0][1],2),'%')
       
                   

   
   else:
       print('Invalid input. Please enter a valid Previewing Time.\n')
       print(f'Do, You want to repeate last process {name}?\n')
       user_choice = str(input(f'Answer with Yes or No {name}\n'))
       while True:
           if user_choice == 'yes':
               preview_all_day_predictions()
               break
           elif user_choice == 'no':
               break
           else:
               print('Invalid input. Please enter a valid Previewing Time.\n')
               print(f'Do, You want to repeate last process {name}?\n')
               user_choice = str(input(f'Answer with Yes or No {name}\n'))
               preview_all_day_predictions()
               break
       


# In[12]:


print('''Hello sir, i\'m a program to preview the weather forecast \n,
do you want to see our last Analysis of weather, or preview the whole day temprature forecasting\n
or choose a specifiy time ''')
system = str(input('press 1 to preview Analysis\npress 2 to preview the whole day temprature forecasting\npress 3 to choosing a specifiy time\n'))
             
if system == '1':
    url_implement() 
elif system == '2':
    preview_all_day_predictions()
else:
    Weathre_forecasting()    


# In[ ]:




