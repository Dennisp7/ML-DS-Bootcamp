# -*- coding: utf-8 -*-
"""panda_dataFrames.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qcJJiqniZp_Homh2eIFohoZVV3kbPnQV
"""

import numpy as np
import pandas as pd

from numpy.random import randn

np.random.seed(101)

# A data frame is just a bunch of series that share an index
df = pd.DataFrame(randn(5,4),['A','B','C','D','E'], ['W','X','Y','Z'])

df

# Grabbing info from the data frame

# We can pull out a column like this
df['W']

# another way to pull out a column - this way is not recommended
df.W

# to pull out multiple columns
df[['W', 'Z']]

# creating a new column in a df
df['new'] = df['W'] + df['Z']

df

# dropping a column
# drop refers to index, which won't work here unless you set axis to 1
# also need to set inplace to true otherwise this change will not be reflected in actual df
# rows are referred to as 0 axis and columns as 1 axis
df.drop('new', axis = 1, inplace=True)

df

# selecting rows - there are 2 ways

# first way 
# Getting row A
df.loc['A']

# second way - using index
df.iloc[0]

# getting a specific cell in the data
# lets say row A, col Y, which should be 0.907969
df.loc['A','Y']

# getting multiple cells in the data
df.loc[['A','B'], ['W','Y']]

"""##DataFrames Part 2

"""

# conditional selection
# Filtering out data that meets certain criteria

# data points greater than 0
# will return data as booleans
df > 0

# Changing from boolean to normal values
# NaN will occur for vals that do not meet conditional
booldf = df > 0
df[booldf]

# another way to get regular vals instead of booleans
df[df > 0]

# Conditional on specific column
# returns bool
df['W'] > 0

# Conditional on specific column
# returns regular vals
# Note! This will return all rows and columns that go with the rows of W that are greater than 0 - it does not matter if information outside or col W don't meet the conditional
# Ex: if row A in Col W meets conditional, than all rows/cols proceeding this will display -see next example for more context
df[df['W']>0]

# Less than 0 in Col z
# Notice the only row in col Z that meets this criteria is row C
# Therefore, only row C for all cols will be displayed 
df[df['Z']<0]

# now that you have seen how to filter data, you can assign this filtered data as a variable for further observations

resultdf = df[df['W']>0]

# Pulling specific information from filtered data
resultdf['X']

# Another way to do the above without using a variable
df[df['W']>0]['X']

# same as above but getting multiple columns
df[df['W']>0][['Y','X']]

# filtering data with multiple conditions
# When filtering for multiple conditions, you cannot use python's normal and operator. You must use & - same for or: |
df[(df['W']>0) & (df['Y']>1)]

df

# quicl way to create a list - instead of having to type it out
example = 'CA NY WY OR CO'.split() 
example

# creating a new column in df
# ensure it matches amount of indicies in df
df['States'] = example 
df

# Setting a column as the index
# keep in mind, this will not permenantly affect the data set unless you state inplace=True in the parameters
df.set_index('States')

"""## Pandas Pt 3

Multi indexing 

Index hierarchy
"""

# Index Levels
# Code we are using to build the dataframe with multi index levels
# Note that you can create as many levels as you want

outside = ['G1', 'G1', 'G1', 'G2', 'G2', 'G2']
inside = [1,2,3,1,2,3]
# this makes a list of tuple pairs of outside and inside - run and see output on line 15
hier_index = list(zip(outside,inside))
# customizing dataframes- this line takes a line that looks like the output of line 15 and creates a multi index from it - see output on line 16
hier_index = pd.MultiIndex.from_tuples(hier_index)

outside

inside

list(zip(outside,inside))

hier_index

# creating a df of random numbers with 6 rows by 2 cols
# set index to be hier_index
# set cols to be a list of A and B

# This is a multi level index df - otherwise known as index hierarchy
# outter most index is the G1 and G2
# inner index is the numbers 1,2,3
df1 = pd.DataFrame(randn(6,2), hier_index, ['A', 'B'])

df1

# Calling data from multi level index df
# must call from outside index to call the inner most data 
df1.loc['G1']

# calling data from the  sub index you looked at in the line above
# let's try the first row
df1.loc['G1'].loc[1]

# naming the indicies
df1.index.names=['Groups', 'Num']

df1

# now grab data further in the df - work out to in
# grab -0.597174

df1.loc['G2'].loc[2]['B']

# cross sections with xs function
# a cross section of rows or cols from a series of df used with multi level index
# another easy alternative to accessing data without .loc

# say I want all vals where index is = 1 in entire df
# xs allows you to go inside df without working outside-in
df1.xs(1,level='Num')

"""##Missing Data

Dropping NAs

Filling NAs
"""

# dropping and filling in missing data
# creating a data frame from a Dictionary

# Key A, B, and C will be columns in our data frame
# We will pass in a list of values for each key, which will be data points for each row in that col
# np.nan signifies missing or null values
d = {'A':[1,2,np.nan], 'B':[5, np.nan, np.nan], 'C':[1,2,3]}

# creating df by passing in dictionary
df2 = pd.DataFrame(d)
df2

# drop na method

# drops any row with 1 or more missing values
df2.dropna()

# drops any col with 1 or more missing values
df2.dropna(axis=1)

# drops any row with 1 or more missing values
# specifying a threshold will allow you to determine how many NA vals you want to keep - meaning, if a row or col has at least the threshold, you keep the na vals

# col ex
# this says if rows have at least 1 NA val, keep the NAs
df2.dropna(thresh=1)

# row ex
# this says if rows have at least 1 NA val, keep the NAs
df2.dropna(thresh=2)

# fill na 
# filling in missing values

# you can fill with any value you would like
# This is a string example
df2.fillna(value='Fill Value')

# filling na value with mean of a column

df2['A'].fillna(value=df2['A'].mean())

"""##Groupby

Grouping data together to call aggregate functions

Group by allows you to group together rows based off of a column and perform an aggregate function on them
"""

# Also a good example of how to create a dataframe using a dictionary!

data = {'Company':['GOOG', 'GOOG', 'MSFT', 'MSFT', 'FB', 'FB'],
        'Person':['Sam', 'Charlie', 'Amy', 'Vanessa', 'Carl', 'Sarah'],
        'Sales':[200,120,340,124,243,350]}

df = pd.DataFrame(data) 
df

# group by company
byComp=df.groupby('Company')



# get the mean sales by company

# this function automatically knows to take the mean of the column that has numeric vals
# Pandas will ignore columns that do not have numeric vals when using this function
byComp.mean()



# Notice that you get back an actual dataframe with an index called company
# and column value of sales
byComp.std()

# because it is returned as a dataframe 
# you can access information through indexing

# get sum of sales for fb
byComp.sum().loc['FB']

# most of the time you wont need to create a variable to use the group by function
# once you get comfortable you can write one line to do everything you want

df.groupby('Company').sum().loc['FB']

# Notice on this one it was able to count strings
df.groupby('Company').count()

# notice python stores people in order so you will have 
# the latest in the alphabet first here

df.groupby('Company').max()

# here you will have the earliest in the alphabet here

df.groupby('Company').min()

# useful information all at once
df.groupby('Company').describe()

# transposed view of describe

df.groupby('Company').describe().transpose()

# pulling information from a single column of describe
df.groupby('Company').describe().transpose()['FB']

"""##Merging, Joining, and Concatenating"""

df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3'],
                        'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1', 'D2', 'D3']},
                        index=[0, 1, 2, 3])

df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                        'B': ['B4', 'B5', 'B6', 'B7'],
                        'C': ['C4', 'C5', 'C6', 'C7'],
                        'D': ['D4', 'D5', 'D6', 'D7']},
                        index=[4, 5, 6, 7])

df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                        'B': ['B8', 'B9', 'B10', 'B11'],
                        'C': ['C8', 'C9', 'C10', 'C11'],
                        'D': ['D8', 'D9', 'D10', 'D11']},
                        index=[8, 9, 10, 11])

df1

df2

df3

"""##Concatenation

basically glues together DataFrames. Keep in mind that dimensions should match along the axis you are concatenating on. You can use **pd.concat** and pass in a list of DataFrames to concatenate together.
"""

# notice that the axis it joined the dfs on was 0
# in other words, it is joining them by rows
pd.concat([df1,df2,df3])

# if you want to concatenate by columns
# specify axis as 1
# notice you have a bunch of missing values
# this is because the dataframes did not have enough values that you wanted to concatenate on
pd.concat([df1,df2,df3], axis=1)

"""##Example DataFrames"""

left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})

right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                          'C': ['C0', 'C1', 'C2', 'C3'],
                          'D': ['D0', 'D1', 'D2', 'D3']})

left

right

"""##Merging"""

pd.merge(left,right,how='inner',on='key')

left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                     'key2': ['K0', 'K1', 'K0', 'K1'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})

right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                          'key2': ['K0', 'K0', 'K0', 'K0'],
                          'C': ['C0', 'C1', 'C2', 'C3'],
                          'D': ['D0', 'D1', 'D2', 'D3']})

pd.merge(left,right,on=['key1', 'key2'])

pd.merge(left,right,how='outer',on=['key1', 'key2'])

pd.merge(left,right,how='right',on=['key1', 'key2'])

pd.merge(left,right,how='left',on=['key1', 'key2'])

"""##Joining

Joining is a convenient method for combining the columns of two potentially differently-indexed DataFrames into a single result DataFrame.
"""

left = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2']},
                     index=['K0', 'K1', 'K2'])

right = pd.DataFrame({'C': ['C0','C2', 'C3'],
                      'D': ['D0','D2', 'D3']},
                     index=['K0', 'K2', 'K3'])

left.join(right)

left.join(right,how='outer')

"""##Operations"""

df = pd.DataFrame({'col1':[1,2,3,4],
                   'col2':[444,555,777,444],
                   'col3':['abc','def','ghi','xyz']})
df.head()

# Getting unique vals

df['col2'].unique()

# number of unique vals
len(df['col2'].unique()) 

#or 
df['col2'].nunique()

# number of each value
df['col2'].value_counts()

# conditionals to sort data

# This says all rows in the dataset where col1>2 will be output
df[df['col1']>2]

# This does the same as above except it checks for boolean 

df['col1']>2

# two conditionals

# Returns all rows where col1 is greater than two and where col2 = 444
df[(df['col1']>2) & (df['col2']==444)]

# summing a column

df['col1'].sum()

def times2(x):
  return x*2

# Apply function allows you two apply operations to col vals
# passing a function on a df
# function takes col vals and applies method from the function

df['col1'].apply(times2)

# counting for cols with strings

# returns the length of each string that are in rows
df['col3'].apply(len)

# instead of writing an entire function, you can use lambda
df['col1'].apply(lambda x: x*2)

# removing cols
# since it is on the col, we need to specify an axis
# in order for this change to be permenant you need to maybe assign it to the df variable or use inspace=True in the arguments
df.drop('col1',axis=1)

# Veryfying I didn't permenantly change the df on previous line of code
df

# column names

df.columns

# Indicies
df.index

# sorting
# the default first parameter in the sort_values function is "by"
# what you put in there is what you want to sort by

# sorting by col2 values
# note how the index stays attached to the row
df.sort_values('col2')

# Finding null vals

# Boolean check
df.isnull()

# Pivoting

data = {'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
        'B': ['one', 'one', 'two', 'two', 'one', 'one'],
        'C': ['x', 'y', 'x', 'y', 'x', 'y'],
        'D': [1,3,2,5,4,1]}
df = pd.DataFrame(data)

df

# table where:
# vals are from col D
# indexes are from A and B (multilevel index)
# Column headers will be from Col C

# look at the table it output to understand what is going on
# note that you have NaN vals for rows that did not have an x or y
df.pivot_table(values='D', index=['A','B'], columns=['C'])

"""##Data Input and Output"""

from google.colab import files
files.upload()

from google.colab import drive
drive.mount('/content/drive')

# pd.read_ can be used for any type of file. We are using csv rn
df = pd.read_csv('example')

# df.to_ allows you to create any type of file
# this example shows you how to create a csv
# index is false because we don't want to save the colab index as a column - see my output2 example

# df.to_csv('My Output', index= False)
df.to_csv('My Output2')

pd.read_csv('My Output2')

# pandas can only import data, not images, forumlas or macros
# if you get xlrd error on your machine, go to terminal and type: conda install xlrd or pip install xlrd

# reading in an excel notebook with multiple sheets
# got error with sheetname because it has since been renamed to sheet_name
# pd.read_excel('Excel_Sample.xlsx',sheetname='Sheet1')

pd.read_excel('Excel_Sample.xlsx',sheet_name='Sheet1')

# creating an excel sheet
df.to_excel('Excel_Sample2.xlsx', sheet_name='NewSheet')

# reading in html files
# keep in mind pandas is going to make a list of tables from the html file
from bs4 import BeautifulSoup
# from sqlalchemy import create_engine

!pip install lxml
!pip install sqlalchemy
!pip install html5lib
!pip install BeautifulSoup

# kept getting "no tables found error" even after installing the correct packages
# read Q&A section from this lecture and found something helpful:
# the solution was as simple as using a different link, which was provided by someone in Q&A section
data = pd.read_html('https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/')

type(data)