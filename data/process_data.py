import sys
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''
    Loading the two database
    input:messages_filepath, categories_filepath
    output: dataset
    '''
    
    messages = pd.read_csv(messages_filepath) #load messages data from csv
    categories = pd.read_csv(categories_filepath) #load categories data from csv
    df = pd.merge(messages, categories, left_on='id', right_on='id', how='outer')
    return df


def clean_data(df):
    '''
    preprocessing
    input:df whoch was developed in teh prior function
    output:cleaned df
    '''
    categories = df.categories.str.split(';', expand = True)
    row = categories.loc[0]
    
    category_colnames = row.apply(lambda x: x[:-2]).values.tolist()
    categories.columns = category_colnames
    categories.related.loc[categories.related == 'related-2'] = 'related-1'
    
    # lets loop through columns in the catagories
    for column in categories:
        categories[column] = categories[column].astype(str).str[-1]
        categories[column] = pd.to_numeric(categories[column])
    
    df.drop('categories', axis = 1, inplace = True)
    df = pd.concat([df, categories], axis = 1)
    df.drop_duplicates(subset = 'id', inplace = True)
    
    return df


def save_data(df, database_filename):
    '''
    saving the data in sql
    Input:df, database_filename
    OutputL saved sql file
    '''
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('disaster_messages_tbl', engine, index=False)
  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()