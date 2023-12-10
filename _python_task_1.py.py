#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd
import numpy as np

def generate_car_matrix(df):
    # Extract unique values from id_1 and id_2 columns
    id_1_values = df['id_1'].unique()
    id_2_values = df['id_2'].unique()

    # Create a new DataFrame with id_1 values as index and id_2 values as columns
    car_matrix = pd.DataFrame(index=id_1_values, columns=id_2_values)

    # Fill the DataFrame with values from the 'car' column
    for index, row in df.iterrows():
        car_matrix.at[row['id_1'], row['id_2']] = row['car']

    # Fill diagonal values with 0
    np.fill_diagonal(car_matrix.values, 0)

    # Fill NaN values with 0
    car_matrix = car_matrix.fillna(0)

    return car_matrix

# Assuming df is the DataFrame containing the dataset
# Load the dataset-1.csv into df
df = pd.read_csv("C:\\Users\\kiran\\Desktop\\dataset-1.csv")

# Call the function to generate the car matrix
car_matrix_result = generate_car_matrix(df)

# Print the result
print(car_matrix_result)


# In[54]:


import pandas as pd

def get_type_count(df):
    # Add a new categorical column 'car_type' based on the values of the 'car' column
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    
    return df

# Assuming 'dataset-1.csv' is loaded into a DataFrame named 'df'
# Replace this line with your actual loading code if needed
df = pd.read_csv("C:\\Users\\kiran\\Desktop\\dataset-1.csv")
# Apply the function
df = get_type_count(df)

# Display the resulting DataFrame
print(df)


# In[55]:


import pandas as pd

def get_bus_indexes(df):
    # Calculate the mean of the 'bus' column
    bus_mean = df['bus'].mean()
    
    # Filter the DataFrame to get rows where 'bus' values are greater than twice the mean
    filtered_df = df[df['bus'] > 2 * bus_mean]
    
    # Get the indices from the filtered DataFrame and sort them in ascending order
    bus_indices = sorted(filtered_df.index.tolist())
    
    return bus_indices

# Assuming your DataFrame is named 'df'
df = pd.read_csv("C:\\Users\\kiran\\Desktop\\dataset-1.csv")
# Call the function
result = get_bus_indexes(df)

# Print the result
print(result)


# In[57]:


import pandas as pd

def filter_routes(data):
    # Calculate average truck values for each route
    route_avg_truck = data.groupby('route')['truck'].mean()
    
    # Filter routes where the average truck value is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    
    # Sort the list of routes
    filtered_routes.sort()
    
    return filtered_routes

# Assuming your DataFrame is named df
df = pd.read_csv("C:\\Users\\kiran\\Desktop\\dataset-1.csv")
result = filter_routes(df)
print(result)


# In[58]:


import pandas as pd

def multiply_matrix(df):
    modified_df = df.copy()

    for col in df.columns[3:]:
        mask_greater_than_20 = modified_df[col] > 20
        mask_20_or_less = ~mask_greater_than_20

        modified_df.loc[mask_greater_than_20, col] *= 0.75
        modified_df.loc[mask_20_or_less, col] *= 1.25

    # Round values to 1 decimal place
    modified_df = modified_df.round(1)

    return modified_df

# Example usage
# Assuming 'resulting_df' is the DataFrame from Question 1
resulting_df = pd.read_csv("C:\\Users\\kiran\\Desktop\\dataset-1.csv")  # Replace with the actual file path
modified_df = multiply_matrix(resulting_df)

# Display the modified DataFrame
print(modified_df)


# In[ ]:




