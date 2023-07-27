# -*- coding: utf-8 -*-
"""21MCI1249_EDA_COVID_19 _PROJECT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KHfNruNY-wshBF6qK0ZwXv-s-3Gdtcwg

# **EDA_COVID_19** **-By Deeksha Varshney**

**Importing the required libraries**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px
import seaborn as sns
import statsmodels.api as sm

"""**Importing and reading the dataset**"""

df = pd.read_csv("/content/drive/MyDrive/files/dataset/Covid_Data_Set.csv")
df.head()

print(df.shape)                 #From the output, we can see that the table contains 5111 rows and 39 columns.

print(df.columns)              #printing out column names using columns

"""**Exploring the DataSet**"""

print(df.info())      #info() method to output some general information about the dataframe:

"""We can observe there are total 38 columns where 8 columns are numerical, 19 columns are integer type and 12 are object type. In total, 5111 rows of data are available."""

df.describe()

"""**Examining the datatypes for each variable**"""

df.dtypes              #Examining the datatypes for each variable

"""**Data type conversions**"""

# Data type conversions
#df['survey_date'] = df['survey_date'].astype('Date')
df['region'] = df['region'].astype('string')
df['country'] = df['country'].astype('string')
df['sex'] = df['sex'].astype('string')
df['age'] = df['age'].astype('int')
df['blood_type'] = df['blood_type'].astype('string')
df['insurance'] = df['insurance'].astype('string')
df['income'] = df['income'].astype('string')
df['race'] = df['race'].astype('string')
df['immigrant'] = df['immigrant'].astype('string')
df['smoking'] = df['smoking'].astype('string')
df['working'] = df['working'].astype('string')


# Show new data types
df.dtypes

"""**Identifying the skewness present in the variables**"""

df.skew().sort_values(ascending=False)

"""**Question: What is the average BMI of a patient from the US who is COVID-19 positive?**

**Function to calculate average BMI of a patient from the US who is COVID-19 positive**
"""

df['bmi'] = df.apply(lambda row: row.weight/((row.height**2)/10000.0), axis=1)
df[(df['covid19_positive']==1) & (df['country']=="US")]['bmi'].mean()

grouped=df[["country","region","risk_mortality","covid19_positive"]]
grouped.head()

"""**Which country has the highest risk of mortality?**

According to the graph Country IT has the highest risk mortality ie 2,777.531


"""

# # Total number of positive cases by each county
cases = pd.DataFrame(grouped.groupby('country')['risk_mortality'].sum())
cases[:100]

"""**Plotting on Graph**"""

temp = grouped.groupby('country')['risk_mortality'].sum().reset_index()
temp = temp.melt(id_vars="country", value_vars=['risk_mortality'],
                 var_name='Case', value_name='Count')
temp.head()

fig = px.area(temp, x="country", y="Count", color='Case', height=600, width=700,
             title='country having highest risk of mortality')
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()

"""**Question: How many countries have reported at least 10 positive cases?**"""

# # Total number of positive cases by each county
cases = pd.DataFrame(grouped.groupby('country')['covid19_positive'].sum())
cases[:100]

"""**Ploting on graph**"""

def plot_daywise_line(col, hue):
    fig = px.line(day_wise, x="Date", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="country/region", yaxis_title="covid19_positive")
    fig.show()

temp = grouped.groupby('country')['covid19_positive'].sum().reset_index()
temp = temp.melt(id_vars="country", value_vars=['covid19_positive'],
                 var_name='Case', value_name='Count')
temp.head()

fig = px.area(temp, x="country", y="Count", color='Case', height=600, width=700,
             title='Highest Cases over time in different Countries')
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()

"""**Question: How many countries have reported at least 10 positive cases?**

According to the graph BE,BR,CL,ES,GB,IN,IT,MX,PK,ZA,US following countries have reported atleast 10 cases.

**Question: Which are the top-five contries according to the number of positive cases?**

US,BR,GB,CA,IT/MX are top 5 countries having a large number of positive cases.

**Understanding the distribution of variables**
"""

# Histogram
df.hist(figsize = (30,15), color='r')
plt.show()

"""**Using pandas to setup a data quality report**"""

data_types = pd.DataFrame(                      #Adding the data types of our data
    df.dtypes,
    columns=['Data Type']
)

missing_data = pd.DataFrame(                    #Checking for missing data
    df.isnull().sum(),
    columns=['Missing Values']
)
missing_data[0:10]

unique_values = pd.DataFrame(                   #Check if the values are unique:
    columns=['Unique Values']
)
for row in list(df.columns.values):
    unique_values.loc[row] = [df[row].nunique()]
unique_values[0:10]

maximum_values = pd.DataFrame(columns=['Maximum Value'])                                       #If the min or max values are relevant, we can add
for row in list(df.columns.values):
  maximum_values.loc[row] = [df[row].max()]
maximum_values[0:10]

dq_report = data_types.join(missing_data).join(unique_values).join(maximum_values)   #Now, generate the overview by df.join(other_df)

print("\nData Quality Report")
print("Total records :{}".format(len(df.index)))
dq_report

"""**Determining  if there is any relationship between the variables risk_infection and COVID-19 positive?**"""

df = df[['risk_infection','covid19_positive']]
sns.pairplot(df, kind="scatter")
plt.show()

"""**Correlation**"""

df.corr()          #corr() is used to find the pairwise correlation of all columns in the dataframe.

#Using Pearson Correlation
plt.figure(figsize=(20,20))
cor = df.corr()
sns.heatmap(cor, annot=True)
plt.show()

"""**Computing the VIF**"""

# load statmodels functions
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

# compute the vif for all given features
def compute_vif(considered_features):

    X = df[considered_features]
    # the calculation of variance inflation requires a constant
    X['intercept'] = 1

    # create dataframe to store vif values
    vif = pd.DataFrame()
    vif["Variable"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif = vif[vif['Variable']!='intercept']
    return vif

# features to consider removing
considered_features = ['covid19_positive', 'risk_infection']


# compute vif
compute_vif(considered_features).sort_values('VIF', ascending=False)

"""**Treating these variables**"""

# compute vif values after removing a feature
considered_features.remove('risk_infection')
compute_vif(considered_features)