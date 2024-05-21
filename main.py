# imports
import pandas as pd
import os
import os.path

# defines
activityPath = 'TIHM_Dataset/Activity.csv'
sleepPath = 'TIHM_Dataset/Sleep.csv'

# check if needed files exist
if os.path.isfile(activityPath) \
    and os.access(activityPath, os.R_OK) \
    and os.path.isfile(sleepPath) \
    and os.access(sleepPath, os.R_OK):
    print('filesystem intact')
else:
    raise FileExistsError('check if activity.csv and sleep.csv are readable and intact')

# reading csv file
# df = pd.read_csv("people.csv")
# print(df.head())

# load data into pandas

# select relevant data

# analyze data