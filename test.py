import pandas as pd

df = pd.read_excel('data/arved.xlsx')
data = df.values.tolist()

# List of values to filter
filter_values = [2004]

# Filter the DataFrame based on the first element of each row
filtered_df = df[df['---'].isin(filter_values)]
filtered_df = filtered_df.values.tolist()

# Print the filtered rows
print(filtered_df)



