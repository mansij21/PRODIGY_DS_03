# -*- coding: utf-8 -*-
"""Task - 03.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d2WbYmxErcBVpH2U-kp0aSIlNTM24oR4

**PRODIGY INFOTECH**

**Author: Mansi Jadhav**

**Data Science Intern**

Task - 03: Build a decision tree classifier to predict whether a customer will purchase a product or service based on their demographic and behavioural data. Use a dataset such as Bank Marketing dataset from the UCI Machine Learning Repository.
"""

from google.colab import files
upload=files.upload()

import pandas as pd
url='/content/IBM.csv'
data=pd.read_csv(url,encoding='latin1')

data.columns

#checking data type & non-null count
data.info()

#SHAPE OF DATASET
print("Rows:", data.shape[0])
print("Columns:", data.shape[1])

#CHECKING FOR UNIQUE VALUES IN THE DATASET
data.nunique()

#Generate summary statistics and transpose the result
data.describe().T

"""Understanding distribution of target variable"""

data['Attrition'].value_counts()

import seaborn as sns
import matplotlib.pyplot as plt
sns.countplot(data=data, x='Attrition')
plt.title('Attrition Count')
plt.show()

"""Understanding Categorical variables"""

categorical = [var for var in data.columns if data[var].dtype=='O']

print('There are {} categorical variables\n'.format(len(categorical)))

print('The categorical variables are :', categorical)

#all the categorical columns with their values -
cols=data.describe(include="O").columns
for i in cols:
    print("Distinct_values :\n 'column_name' =",i)
    print(data[i].unique())
    print("")

#checking number of categorical data as per their columns
for var in categorical:

    print(data[var].value_counts())

"""Understanding numerical variable"""

numerical = [var for var in data.columns if data[var].dtype!='O']

print('There are {} numerical variables\n'.format(len(numerical)))

print('The numerical variables are :', numerical)

data[numerical].head()

"""Missing Value Detection for all columns"""

data.isnull()

data.isnull().sum()

"""Since, all the values are 0, so there is no need to perform the step of feeding missing values"""

#Checking relationship among attributes
data.corr()

plt.figure(figsize=(20,8))
sns.heatmap(data.corr(),cmap='BuPu',annot=True)

"""Segregating Numerical and Categorical Attributes"""

data_cat = data.select_dtypes('object')
data_num = data.select_dtypes(exclude='object')

data_cat.head()

data_num.head()

#Using Boxplot to detect the outliers-
plt.figure(figsize=(15,12))

for i ,col in enumerate(list(data_num.columns)):
    plt.subplot(9,2,i+1)
    data_num.boxplot(col)
    plt.grid()
    plt.tight_layout()

"""The box plot here indicates the interquartile range, that is, the top line of the box is the third quartile and the bottom line of the box is the second quartile. The line separating the second and third quartiles indicates the median. The lines outside of the box indicate the outer-quartiles

From the above box plots we can see that the Age & Monthly Income columns have outliers whereas other columns do not.
"""

#Treating outliers using IQR
q1 = data.quantile(0.25)
q3 = data.quantile(0.75)
IQR = q3 - q1
lower_limit,upper_limit=q1-(1.5*IQR),q3+(1.5*IQR)
data = data[~((data<lower_limit)|(data>upper_limit)).any(axis=1)]
data.shape

data.plot(kind='kde', subplots=True, sharex=False, layout=(4,3), legend = True, figsize=(10,10))
plt.show()

# checking the skewness coefficient to determine the transformation
for i in data_num.columns:
    sk = data_num[i].skew()
    print(i,"  has the skewness coeff of :",sk)

# skew coeff should lie between [-1,1]

"""EDA

1) Univariate Analysis
"""

sns.histplot(data_num.DistanceFromHome)
plt.show()

sns.histplot(data_num.MonthlyIncome)
plt.show()

sns.countplot(data=data_cat, x='Department')
plt.show()

"""2) Bivariate Analysis"""

sns.boxplot(x='Attrition',y = 'DistanceFromHome',data = data)
plt.show()

sns.boxplot(x='Attrition',y = 'MonthlyIncome',data = data)
plt.show()

pd.crosstab(data_cat.Attrition,data_cat.MaritalStatus)

#Age based attrition of employees
plt.figure(figsize=(20,10))
sns.countplot(x='Age',hue='Attrition',data=data)

#Monthly income of the employees acc to age
import numpy as np
plt.figure(figsize=(20,10))
sns.barplot(x='Age',y='MonthlyIncome',data=data,estimator=np.mean)
plt.title('Monthly income of employees according to their Age')

# Departmental Attrition of Employees
plt.figure(figsize=(10,6))
sns.countplot(data=data,x=data['Department'],order=data['Department'].value_counts().sort_values(ascending=True).index, palette='ocean')
plt.title('Departments of employess')

#Attrition based on gender of the employee
plt.figure(figsize=(8,5))
sns.countplot(x='EducationField',hue='Attrition',data=data, palette= 'seismic')
plt.title("Attrition based on education field of the employee")

#Distribution of employees by the education field
plt.figure(figsize=(8,5))
sns.countplot(data=data,x=data['EducationField'], order=data['EducationField'].value_counts().sort_values(ascending=True).index, palette = 'cubehelix')
plt.title('Attrition by EducationField')

# number of married and unmarried employees
plt.figure(figsize=(8,5))
sns.countplot(x=data['MaritalStatus'], order= data['MaritalStatus'].value_counts().sort_values(ascending=True).index, palette = 'icefire')
plt.title('MaritalStatus of the employees')

#Attrition based on gender of the employee
plt.figure(figsize=(8,5))
sns.countplot(x='Gender',hue='Attrition',data=data, palette= 'PuRd')
plt.title("Attrition based on gender of the employee")

#Attrition based on Job satisfaction of the employees
plt.figure(figsize=(10,10))
sns.countplot(x='JobSatisfaction',hue='Attrition',data=data,palette="Reds")
plt.title("Attrition based on job satisfaction of the employees")

#Distribution of employees by the education field
plt.figure(figsize=(8,5))
sns.countplot(data=data,x=data['OverTime'], order=data['OverTime'].value_counts().sort_values(ascending=True).index, palette = 'seismic')
plt.title('Attrition count by overtime')

"""ENCODING CATEGORICAL VARIABLES"""

# One-Hot Encoding for nominal variables
data = pd.get_dummies(data, columns=['Department', 'EducationField', 'Gender', 'OverTime', 'MaritalStatus'])

data.columns

data.head()

"""MODEL BUILDING"""

# Separate the target variable (Attrition) from the features
X = data.drop('Attrition', axis=1)
y = data['Attrition']

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X, y, train_size=0.8, random_state=200)

from sklearn.tree import DecisionTreeClassifier
# Create a Decision Tree Classifier
clf = DecisionTreeClassifier()

# Train the classifier on the training data
clf.fit(X_train, y_train)

# Predict the target values on the test set
y_pred = clf.predict(X_test)
y_pred

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Print a classification report
print(classification_report(y_test, y_pred))

# Create and visualize the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", conf_matrix)