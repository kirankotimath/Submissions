#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd

def calculate_distance_matrix(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv("C:\\Users\\kiran\\Desktop\\dataset-3.csv")

    # Create a dictionary to store distances between toll locations
    distances = {}

    # Iterate through the rows of the DataFrame and populate the distances dictionary
    for index, row in df.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']
        distance = row['distance']

        # Populate the distances dictionary with bidirectional distances
        distances[(id_start, id_end)] = distance
        distances[(id_end, id_start)] = distance

    # Create a list of unique toll locations
    unique_ids = sorted(list(set(df['id_start'].unique()) | set(df['id_end'].unique())))

    # Initialize an empty DataFrame for the distance matrix
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)

    # Iterate through each pair of toll locations and calculate cumulative distances
    for id_start in unique_ids:
        for id_end in unique_ids:
            if id_start == id_end:
                # Diagonal values set to 0
                distance_matrix.loc[id_start, id_end] = 0
            else:
                # Check if distances are known for the route
                route_distance = distances.get((id_start, id_end), None)

                if route_distance is not None:
                    # Set the cumulative distance
                    distance_matrix.loc[id_start, id_end] = route_distance
                else:
                    # If the route is unknown, set distance to NaN
                    distance_matrix.loc[id_start, id_end] = None

    return distance_matrix

# Replace 'your_dataset_path.csv' with the actual path or URL of your CSV file
csv_file_path = '"C:\\Users\\kiran\\Desktop\\dataset-3.csv'
result_matrix = calculate_distance_matrix(csv_file_path)

# Print the resulting distance matrix
result_matrix


# In[5]:


import pandas as pd

def unroll_distance_matrix(distance_matrix):
    # Initialize an empty list to store unrolled distances
    unrolled_distances = []

    # Iterate through the rows of the distance matrix
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                # Append the combination and its distance to the list
                unrolled_distances.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance_matrix.loc[id_start, id_end]
                })

    # Create a DataFrame from the list of unrolled distances
    unrolled_df = pd.DataFrame(unrolled_distances)

    return unrolled_df

# Assuming you already have the 'result_matrix' DataFrame from the previous question
# Replace 'result_matrix' with the actual DataFrame variable name you have
unrolled_df = unroll_distance_matrix(result_matrix)

# Print the resulting unrolled DataFrame
unrolled_df


# In[6]:


import pandas as pd

def find_ids_within_ten_percentage_threshold(df, reference_value):
    # Filter the DataFrame for rows with the specified reference value
    reference_rows = df[df['id_start'] == reference_value]

    if reference_rows.empty:
        print(f"No data found for reference value {reference_value}")
        return None

    # Calculate the average distance for the reference value
    average_distance = reference_rows['distance'].mean()

    # Calculate the lower and upper bounds within 10% of the average
    lower_bound = average_distance - (0.1 * average_distance)
    upper_bound = average_distance + (0.1 * average_distance)

    # Filter the DataFrame for rows within the 10% threshold
    within_threshold = df[(df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]

    # Extract and sort unique values from the 'id_start' column
    result_ids = sorted(within_threshold['id_start'].unique())

    return result_ids

# Assuming you already have the 'unrolled_df' DataFrame from the previous question
# Replace 'unrolled_df' with the actual DataFrame variable name you have
reference_value = 1001400  # Replace with the desired reference value
result_ids = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)

# Print the resulting list of values within 10% of the average distance
print(result_ids)


# In[7]:


import pandas as pd

def calculate_toll_rate(df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Add columns for each vehicle type with their respective toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

# Assuming you already have the 'unrolled_df' DataFrame from the previous question
# Replace 'unrolled_df' with the actual DataFrame variable name you have
df_with_toll_rates = calculate_toll_rate(unrolled_df)

# Print the resulting DataFrame with toll rates
df_with_toll_rates


# In[12]:





import pandas as pd
from datetime import time

def calculate_time_based_toll_rates(df):
    # Define time ranges and corresponding discount factors
    time_ranges = [
        {'start_time': time(0, 0, 0), 'end_time': time(10, 0, 0), 'discount_factor': 0.8},
        {'start_time': time(10, 0, 0), 'end_time': time(18, 0, 0), 'discount_factor': 1.2},
        {'start_time': time(18, 0, 0), 'end_time': time(23, 59, 59), 'discount_factor': 0.8}
    ]

    # Apply constant discount factor for weekends
    weekend_discount_factor = 0.7

    # Create columns for start_day, start_time, end_day, and end_time
    df['start_day'] = df['end_day'] = df['start_time'] = df['end_time'] = None

    # Iterate through each unique (id_start, id_end) pair
    for (id_start, id_end), group in df.groupby(['id_start', 'id_end']):
        for day in range(7):  # 0 is Monday, 6 is Sunday
            for time_range in time_ranges:
                start_time = time_range['start_time']
                end_time = time_range['end_time']
                discount_factor = weekend_discount_factor if day >= 5 else time_range['discount_factor']

                # Add row with time-based information
                df = df.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'start_day': pd.Categorical(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])[day],
                    'end_day': pd.Categorical(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])[(day + 1) % 7],
                    'start_time': start_time,
                    'end_time': end_time,
                    'distance': group['distance'].iloc[0],
                }, ignore_index=True)

    # Sort the DataFrame by (id_start, id_end, start_day, start_time)
    df.sort_values(by=['id_start', 'id_end', 'start_day', 'start_time'], inplace=True)

    # Calculate toll rates based on time ranges and discount factors
    for time_range in time_ranges:
        start_time = time_range['start_time']
        end_time = time_range['end_time']
        discount_factor = weekend_discount_factor if start_time == time(0, 0, 0) else time_range['discount_factor']

        df['moto'] = df.apply(lambda row: row['distance'] * discount_factor if start_time <= row['start_time'] <= end_time else row['moto'], axis=1)
        df['car'] = df.apply(lambda row: row['distance'] * discount_factor if start_time <= row['start_time'] <= end_time else row['car'], axis=1)
        df['rv'] = df.apply(lambda row: row['distance'] * discount_factor if start_time <= row['start_time'] <= end_time else row['rv'], axis=1)
        df['bus'] = df.apply(lambda row: row['distance'] * discount_factor if start_time <= row['start_time'] <= end_time else row['bus'], axis=1)
        df['truck'] = df.apply(lambda row: row['distance'] * discount_factor if start_time <= row['start_time'] <= end_time else row['truck'], axis=1)

    return df

# Creating the initial DataFrame from the provided dataset
data = {
    'id_start': [1001400, 1001402, 1001404, 1001406, 1001408, 1001410, 1001412, 1001414, 1001416, 1001418, 1001420,
                 1001422, 1001424, 1001426, 1001428, 1001430, 1001432, 1001434, 1001436, 1001436, 1001438, 1001438,
                 1001438, 1001440, 1001442, 1001488, 1004356, 1004354, 1004355, 1001444, 1001446, 1001448, 1001450,
                 1001452, 1001454, 1001456, 1001458, 1001460, 1001460, 1001461, 1001460, 1001462, 1001461, 1001462,
                 1001464, 1001466, 1001468, 1001468, 1001470, 1001470, 1001472],
    'id_end': [1001402, 1001404, 1001406, 1001408, 1001410, 1001412, 1001414, 1001416, 1001418, 1001420, 1001422,
               1001424, 1001426, 1001428, 1001430, 1001432, 1001434, 1001436, 1001438, 1001437, 1001437, 1001440,
               1001442, 1001488, 1004356, 1004354, 1004355, 1001444, 1001446, 1001448, 1001450, 1001452, 1001454,
               1001456, 1001458, 1001460, 1001461, 1001462, 1001462, 1001464, 1001466, 1001468, 1001470, 1001472,
               1001462, 1001464, 1001466],


# In[ ]:





# In[ ]:




