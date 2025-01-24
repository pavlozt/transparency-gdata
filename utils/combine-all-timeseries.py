#!/usr/bin/env python3

# This script processes multiple Excel files, extracts data, and merges them into a single DataFrame.
# It handles files with a specific naming convention and ensures that the resulting DataFrame
# has a consistent structure by dropping columns with any NA values.

import pandas as pd
import glob
import os

def process_file(file_path):
    # Extract the label from the file name
    base_name = os.path.basename(file_path)
    label = base_name.split('-')[1].split('.')[0]

    df = pd.read_excel(file_path)

    # Rename the columns
    df.columns = ['timestamp', label]

    # Set 'timestamp' as the index
    df.set_index('timestamp', inplace=True)

    return df

def merge_dataframes(file_list):

    #  Read and marge file list into dataframe
    merged_df = pd.DataFrame()

    for file_path in file_list:
        df = process_file(file_path)
        if merged_df.empty:
            merged_df = df
        else:
            merged_df = merged_df.join(df, how='outer')

    return merged_df

file_list = glob.glob('../data/data-*.xlsx')

result_df = merge_dataframes(file_list)

# Drop columns where there is at least one NA value. This can happen if parsing occurs at different times and data slightly mismatches
result_df = result_df.dropna()

result_df.to_csv('../data/combined.csv', index=True)

