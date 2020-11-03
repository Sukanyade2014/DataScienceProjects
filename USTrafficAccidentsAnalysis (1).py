#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Kaggle link: https://www.kaggle.com/sobhanmoosavi/us-accidents
Backup Dataset: https://www.kaggle.com/usdot/flight-delays

Research topic: Analyze US traffic data  from 2016-2020 to predict the risk of an accident at a certain time of the day for a certain zipcode
in a given day under a specific weather condition

Questions to be answered:
1. Are factors like Crossing, Junction , No-Exit etc related to occurance of accidents
2. Find out the number of accidents per state per year
3. Find the average number of accidents per state per year
4. Find out the states with increasing numbers of accidents each year
5. Determine the State with highest number of accidents for 2016
6. Plot a bar graph to show the number of  high Severity accidents occurring at Day vs at Night
7. Plot a graph to depict the number of Accidents per severity for Oregon
8. For the State of Oregon, check the number of Accidents per severity for each of the zipcodes 
9. From the above data, filter the records with zipcodes between '97202' and '97341'
10. Find if certain days of the week has more accidents than others
'''
import pandas as pd


# In[2]:


df_accidents = pd.read_csv('/Users/sukanyade/PycharmProjects/untitled/US_Accidents_June20.csv' )


# In[3]:


#Find if factors like No_Exit, Railway are related to  number of accidents
accident_cause = {}
accident_cause_keys = ['Amenity', 'Bump', 'Crossing',
       'Give_Way', 'Junction', 'No_Exit', 'Railway', 'Roundabout', 'Station',
       'Stop', 'Traffic_Calming', 'Traffic_Signal', 'Turning_Loop' ]
for key in accident_cause_keys:
    count = df_accidents[df_accidents[key] == True]['ID'].count()
    if count > 10000: # taking into consideration high number of accidents related to the listed clauses
        accident_cause[key]  = count
sorted_acc_cause = sorted(accident_cause.items(), key = lambda x:x[1] , reverse = True)
keys = []
values = []
for items in sorted_acc_cause:
    keys.append(items[0]) 
    values.append(items[1])
import matplotlib.pyplot as plt
plt.bar(range(len(keys)), values, align='center')
plt.xticks(range(len(keys)), keys ,rotation = 45)
plt.show()


# In[4]:


df_accidents_by_state_temp = df_accidents[['ID','State', 'Start_Time']]
df_accidents_by_state = df_accidents_by_state_temp.copy()
df_accidents_by_state[ 'year'] = df_accidents_by_state_temp['Start_Time'].apply(lambda x:x.split('-')[0])


# In[5]:


#Number of accidents per state per year
df_acc_state_year = df_accidents_by_state.groupby(['State', 'year'])['ID'].count()
print("Number of accidents per state per year:" , df_acc_state_year)
#Average number of accidents per state per year
df_mean_accidents = df_acc_state_year.mean(level=['State'])
print("Average number of accidents per state per year:" , df_mean_accidents)


# In[6]:


#Find out the states with increasing numbers of accidents each year
df_acc_state_year = df_acc_state_year.unstack()
df_acc_state_year = df_acc_state_year.reset_index('State')
states = df_accidents_by_state['State'].unique()
years = df_accidents_by_state['year'].unique()
years = sorted(years)
increasing_acc_state = []
years = years[:len(years)-1]

for state in states:
    count_year_prev = 0
    increasing = 0
    for year in years:
        count_year = df_acc_state_year.loc[ df_acc_state_year['State'] == state,[year]][year]
        if count_year.iloc[0] < count_year_prev:
            increasing = 1
            break
        else:
            count_year_prev = count_year.iloc[0]
    if increasing ==0:
        increasing_acc_state.append(state)
print("States with increasing number of accidents:" , increasing_acc_state)
      


# In[7]:


#State with highest number of accidents for 2016
df_acc_state_year = df_accidents_by_state.groupby(['State', 'year'])['ID'].count()
df_acc_state_year = df_acc_state_year.unstack()
state = df_acc_state_year.loc[df_acc_state_year['2016'] == df_acc_state_year['2016'].max()].index
print("State with highest accidents in 2016:" , state[0])


# In[8]:


#Plot a bar graph to show the number of  high Severity accidents occurring at Day vs at Night
df_visibility = df_accidents[['ID', 'Severity'  , 'Nautical_Twilight']]
df_visibility = df_visibility.groupby('Nautical_Twilight')['ID'].count()
df_visibility = df_visibility.sort_values(ascending=False)
ax = df_visibility.plot.bar(x='Nautical_Twilight', y='val', rot=0)


# In[9]:


# Plotting number of Accidents per severity for Oregon

df_accidents_OR = df_accidents.loc[df_accidents.State == 'OR', ['ID' , 'Severity' , 'Zipcode' , 'Start_Time' , 'End_Time']]
total_OR_Accidents = df_accidents_OR['ID'].count()

total_OR_Accidents_Severity = df_accidents_OR.groupby('Severity')['ID'].count()/total_OR_Accidents
ax = total_OR_Accidents_Severity.plot.bar(x='Severity', y='val', rot=0)


# In[10]:


#For the State of Oregon, check the number of Accidents per severity for each of the zipcodes 
df_accidents_OR = df_accidents.loc[df_accidents.State == 'OR', ['ID' ,'Severity' , 'Zipcode' , 'Start_Time' , 'End_Time']]
df_accidents_OR['Zipcode'] = df_accidents_OR['Zipcode'].apply(lambda x: str(x).split('-')[0])
df_accidents_OR.pivot_table('ID' , index ='Zipcode' , columns='Severity', aggfunc='count', dropna=True).plot()


# In[11]:


#Filter zipcodes between 97202 and 97341
df_accidents_OR = df_accidents.loc[df_accidents.State == 'OR', ['ID' ,'Severity' , 'Zipcode' , 'Start_Time' , 'End_Time']]
df_accidents_OR['Zipcode'] = df_accidents_OR['Zipcode'].apply(lambda x: str(x).split('-')[0])
df_accidents_OR = df_accidents_OR[df_accidents_OR.Zipcode.between('97202','97341',  inclusive=False)].pivot_table('ID' , index ='Zipcode' , columns='Severity', aggfunc='count', dropna=True).plot()


# In[12]:


# Find if certain days of the week has more accidents than others
df_accidents_by_day_temp = df_accidents[['ID', 'Start_Time']]
df_accidents_by_day = df_accidents_by_day_temp.copy()
df_accidents_by_day['Start_Time'] = pd.to_datetime(df_accidents_by_day_temp['Start_Time'])
df_accidents_by_day.loc[:,'day'] = pd.DatetimeIndex(df_accidents_by_state.loc[:,'Start_Time']).dayofweek
df_accidents_by_day =  df_accidents_by_day.groupby('day')['ID'].count()
df_accidents_by_day.plot(kind='bar').set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])

