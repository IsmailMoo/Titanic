import pandas as pd
import numpy as np
import os

def read_data():
    #set the path of the raw data
    raw_data_path = os.path.join(os.path.pardir,'data','raw')
    train_file_path = os.path.join(raw_data_path, 'train.csv')
    test_file_path = os.path.join(raw_data_path, 'test.csv')

    #read data with all default values
    train_df = pd.read_csv(train_file_path, index_col='PassengerId')
    test_df = pd.read_csv(test_file_path, index_col='PassengerId')

    test_df['Survived'] = -786 #adding Survived column to test data 

    df = pd.concat((test_df, train_df),axis=0, sort=False)
    return df


def fill_missing_values(df):
    #embarked
    df.Embarked.fillna('C',inplace=True)

    #Fare
    median_fare=df.loc[(df.Pclass==3) & (df.Embarked=='S')].Fare.median()
    df.Fare.fillna(median_fare,inplace=True)

    #age
    title_median_age = df.groupby('Title').Age.transform('median')
    df.Age.fillna(title_median_age,inplace=True)

    return df


def get_deck(cabin):
    return np.where(pd.notnull(cabin), str(cabin)[0].upper(), 'Z' ) 

def reorder_columns(df):
    columns = [column for column in df.columns if column != 'Survived']
    columns = ['Survived'] + columns
    df = df[columns]
    return df

def GetTitle(name):
    title = name.split(',')[1].split('.')[0].strip().lower()
    return title

def processed_data(df):
    #using method chaining concept
    return(df
           #create title attribute - then add this
           .assign(Title = lambda x: x.Name.map(GetTitle))
           #working missing values - start with this 
           .pipe(fill_missing_values)
           #create fare bin feature
           .assign(Fare_Bin = lambda x: pd.qcut(x.Fare, 4, labels=['very_low','low','high','very_hig']))

           #create AgeState FamilySize n IsMother
           .assign(AgeState = lambda x: np.where(x.Age >= 18, 'Adult', 'Child') )
           .assign(FamilySize = lambda x: x.Parch + x.SibSp + 1)
           .assign(IsMother = lambda x: np.where(((x.Sex == 'female') & (x.Parch > 0) & (x.Age > 18) & (x.Title != 'miss')), 1, 0))

           #create deck feature
           .assign(Cabin = lambda x: np.where(x.Cabin == 'T',np.nan, x.Cabin))
           .assign(Deck = lambda x: x.Cabin.map(get_deck))

           #feature encoding
           .assign(IsMale = lambda x: np.where(x.Sex == 'male', 1, 0))
           .pipe(pd.get_dummies, columns=['Deck','Pclass','Title','Fare_Bin','Embarked','AgeState'])
           
            #drop unnecessary columns
            .drop(['Cabin','Name','Ticket','Parch','SibSp','Sex'], axis=1)
            #reorder columns
            .pipe(reorder_columns)
    )


def write_data(df):
    processed_data_path = os.path.join(os.path.pardir,'data','processed')
    write_train_path = os.path.join(processed_data_path,'train.csv')
    write_test_path = os.path.join(processed_data_path,'test.csv')

    # writing train data to file
    #df[df.Survived != -786].to_csv(write_train_path) # this one also gives same result
    df.loc[df.Survived != -786].to_csv(write_train_path)
    # writing test data to file
    # as we dont have Survived column in test lets remove it
    columns = [column for column in df.columns if column != 'Survived' ]
    df.loc[df.Survived == -786,columns].to_csv(write_test_path)
                   
if __name__ == '__main__':
    df = read_data()
    df = processed_data(df)
    write_data(df)

#df.info()
print 'Done.......'
#print df.Survived.value_counts()
