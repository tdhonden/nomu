'''
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def group_by_delta(df, delta = 0.25):
    # Assuming your DataFrame is named 'df'
    specified_value = delta
    # Group the DataFrame by 'Date', 'securityId', and 'expiration'
    grouped = df.groupby(['Date', 'SecurityID', 'Expiration'])
    # Find the row with the delta closest to the specified value for each group
    selected_rows = grouped.apply(lambda group: group.loc[
        (group['Delta'] - specified_value).abs().idxmin()])
    # Reset the index of the selected rows DataFrame
    selected_rows = selected_rows.reset_index(drop=True)
    return selected_rows

def find_target_dates(df):
    target_expirations = [
        timedelta(days=30),   # 1m
        timedelta(days=90),   # 3m
        timedelta(days=180),  # 6m
        timedelta(days=365),  # 12m
        timedelta(days=365)   # 1year
    ]
    # Create a list to store the results
    result_list = []
    # Group the DataFrame by 'Date' and 'SecurityID'
    grouped = df.groupby(['Date', 'SecurityID'])
    # Iterate over each group
    for group_keys, group in grouped:
        group['Expiration'] = pd.to_datetime(group['Expiration'])
        date_str, security_id = group_keys
        date = datetime.strptime(date_str, '%Y-%m-%d')  # Convert date string to datetime object
        # Create a dictionary to store the results for this group
        group_result = {'Date': date_str, 'SecurityID': security_id}
        # Iterate over the target expirations
        for target_expiration in target_expirations:
            target_date = date + target_expiration
            # Find the row with the closest expiration to the target date
            closest_row = group.loc[(group['Expiration'] - target_date).abs().idxmin()]
            # Add the Implied_Vol, Delta, and Expiration to the group_result dictionary
            group_result[f'Implied_Vol_{target_expiration.days // 30}m'] = closest_row['ImpliedVolatility']
            group_result[f'Delta_{target_expiration.days // 30}m'] = closest_row['Delta']
            group_result[f'Expiration_{target_expiration.days // 30}m'] = closest_row['Expiration'].strftime('%Y-%m-%d')
        # Append the group_result dictionary to the result_list
        result_list.append(group_result)
    # Create a new DataFrame from the result_list
    result_df = pd.DataFrame(result_list)
    return result_df

def find_ratios(df, target_ratios):
    target_ratios = target_ratios
    # iv_cols = ['Expiration_' + x for x in target_ratios]
    all_ratios = [f'{b}/{a}' for i, a in enumerate(target_ratios) for b in target_ratios[i+1:]]
    # print(all_ratios)

    for ratio in all_ratios:
        fraction = ratio.split('/')
        numerator = 'Implied_Vol_'+ fraction[0]
        denominator = 'Implied_Vol_' + fraction [1] 
        df[ratio] = df[numerator] / df [denominator]
        
    return df

def row_percent(row, all_ratios):
    bing = row[all_ratios].rank(pct=True)
    return bing

def find_percentiles(df, target_ratios):
    target_ratios = target_ratios
    all_ratios = [f'{b}/{a}' for i, a in enumerate(target_ratios) for b in target_ratios[i+1:]]
    output_cols = ['Percentile_' + x for x in all_ratios]
    # print(output_cols)
    df[output_cols] = (df.groupby(['SecurityID'], group_keys=False)).apply(row_percent, all_ratios)
    return df

def analyze_for_delta(delta, target_ratios, path_to_file='sample_data.csv'):
    columns_of_interest = ['Date', 'SecurityID', 'Expiration', 'ImpliedVolatility', 'Delta']
    df = pd.read_csv(path_to_file)
    df = df[columns_of_interest]
    df = group_by_delta(df, delta)
    df = find_target_dates(df)
    df = find_ratios(df, target_ratios)
    df = find_percentiles(df, target_ratios)
    return df
TARGET_DELTA = 0.5
TARGET_RATIOS = ['1m', '3m', '6m', '12m']

df = analyze_for_delta(TARGET_DELTA, TARGET_RATIOS, 'sample_data.csv')
df.to_csv('delta50.csv')
'''

# join on date and security
