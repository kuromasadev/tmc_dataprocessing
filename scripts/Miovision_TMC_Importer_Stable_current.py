# IMPORT MODULES
import pandas as pd
import os
import glob
import csv
from IPython.display import display

# IMPORT FILE PATHS AND CSV
active_project = "../reports/current/"
csv_output = "../export/"

csv_files = glob.glob(os.path.join(active_project, "*.csv"))

## setting up the list for all raw dfs
all_df = []

## listing turning movement counts as current 
current_TMC_list = []

for l in csv_files:
    current_TMC_list.append(l)

# function to read all csvs listed 

def read_csv(file_path):
    try:
        imp_df = pd.read_csv(file_path, 
                             sep='delimiter',
                             header=None,
                             engine='python'
                            )
        return imp_df #imp_df as in imported dataframe
    except pd.errors.ParserError as e:
        return (file_path, f"Error parsing CSV: {str(e)}")  # Return tuple with file path and error message
    except FileNotFoundError:
        return (file_path, "File not found")  # Return tuple with file path and error message

## validating dataframes

for file_path in current_TMC_list:
    imp_df = read_csv(file_path)  # Assign the returned DataFrame to imp_df
    all_df.append(imp_df)  # Append imp_df to all_df

valid_dfs = [df for df in all_df if isinstance(df, pd.DataFrame)]  # Filter out non-DataFrame objects

# MODIFY IMPORTED DATA

## modify each dataframe in two parts

def modify_in_df(df):
    # Part A: Summary
    summary_end_row = df.index[df.iloc[:, 0].notna() & df.iloc[:, 0].str.startswith("PM Peak")].tolist()[0]
    summary = df.iloc[:summary_end_row + 1, :]
    summary = summary.iloc[1:]  # Remove the first row
    summary = summary[~summary.eq("").all(axis=1)] # drop rows with empty strings
    summary = summary.dropna(how='all') #another attempt to drop empty
    summary.reset_index(drop=True, inplace=True)
    summary = summary.drop(10)
    summary = summary.rename(columns={summary.columns[0]: "Summary Description"})  # Rename the second column
    summary.reset_index(drop=True, inplace=True)

    ## Convert all values in the "Summary Description" column to strings
    summary["Summary Description"] = summary["Summary Description"].astype(str)

    ## Define a regular expression pattern to extract the desired substrings
    pattern = r'(.*?),(.*)'

    ## Extract the substrings using the pattern
    summary = summary["Summary Description"].str.extract(pattern)

    ## Formatting
    summary = summary.rename(columns={summary.columns[0]: "Summary Description"})  # Rename the first column
    summary = summary.rename(columns={summary.columns[1]: "Summary"})  # Rename the first column

    # Flip rows to columns
    transposed_summary = summary.transpose().reset_index(drop=True)
    new_header = transposed_summary.iloc[0]  # Store the first row as the new header
    transposed_summary.columns = new_header  # Set the new header
    transposed_summary_clean = transposed_summary[transposed_summary.index != "Summary"]
    transposed_summary_clean = transposed_summary.iloc[1:]
    transposed_summary_clean = transposed_summary_clean.dropna(axis='columns')

    # Separate out key infomration
    transposed_summary_clean[['Location A','Location B']] = transposed_summary_clean['Location'].str.split(' at ', n=1, expand=True)
    transposed_summary_clean[['Longitude', 'Latitude']] = transposed_summary_clean['Latitude and Longitude'].str.split(',', expand=True)
    transposed_summary_clean[['Longitude', 'Latitude']] = transposed_summary_clean['Latitude and Longitude'].str.replace('"', '').str.split(',', expand=True)
    transposed_summary_clean[['Year', 'Quarter']] = pd.to_datetime(transposed_summary_clean['End Time']).dt.to_period('Q').astype(str).str.split("Q", expand=True)

    # Prepare information for raw merging

    summmary_dim = transposed_summary_clean.drop(['Legs and Movements',
                                              'Bin Size',
                                              'Time Zone',
                                              'Start Time',
                                              'End Time',
                                              'Location',
                                              'Latitude and Longitude'],axis=1)

    # Part B: Raw Data 
    raw_data_startrow = df.index[df.iloc[:, 0] == "Time,Entry,Entry Direction,Exit,Exit Direction,Movement,Class,Volume"].tolist()[0]
    raw_data = df.iloc[raw_data_startrow:, :]  # Extract from the starting row onwards
    raw_data.reset_index(drop=True, inplace=True)
    raw_data = raw_data.rename(columns={raw_data.columns[0]:"rawdata"})
    raw_table = raw_data["rawdata"].str.split(',',expand=True) #split columns
    raw_header = raw_table.iloc[0]
    raw_table.columns = raw_header  # Set the new header
    raw_table = raw_table.iloc[1:]  # Remove the first row

    # Merge the row of 'summary_dim' to each row in 'raw data
    merged_data = pd.merge(raw_table, summmary_dim, how='cross')
    
    return merged_data

## loop through dataframes

modified_df_list = []  # List to store the modified DataFrames
error_log = []  # List to store the error details
df = pd.DataFrame()

for i in range(len(valid_dfs)):
    try:
        df = valid_dfs[i]  # Retrieve the DataFrame by index
        modified_df = modify_in_df(df)  # Modify the DataFrame
        modified_df_list.append(modified_df)  # Append the modified DataFrame to the list
    except Exception as e:
        error_log.append((i, str(e)))  # Log the index and error message

## finalize into a big dataframe

big_df = pd.concat(modified_df_list, ignore_index=True)
big_df['Volume'] = big_df['Volume'].astype(float)


# Analysis Sets 

grp_byproj = big_df.groupby(['Project']).agg({
    'Volume' : 'sum',
    'Year': 'first',
    'Quarter': 'first',
    'Longitude': 'first',
    'Latitude': 'first'
}).reset_index()

grp_bystudy = big_df.groupby(['Study Name']).agg({
    'Volume' : 'sum',
    'Year': 'first',
    'Quarter': 'first',
    'Longitude': 'first',
    'Latitude': 'first'
}).reset_index()

# CSV Backup Exports

big_df.to_csv(os.path.join(csv_output, 'Miovision_TMC_Current_RAW.csv'), index=False)
grp_byproj.to_csv(os.path.join(csv_output, 'Miovision_TMC_Current_prj.csv'), index=False)
grp_bystudy.to_csv(os.path.join(csv_output, 'Miovision_TMC_Current_sty.csv'), index=False)