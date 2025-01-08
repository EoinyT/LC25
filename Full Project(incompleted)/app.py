import pandas as pd   

# Load dataset
df = pd.read_csv(r'C:\Users\19ETallon.CDL\Desktop\CS\Full Project(incompleted)\Rainfall_Data_Germany_Complete.csv')

# Print the first 7 rows
print(df.head(7))

# Calculate summary statistics
print("Summary Statistics:")
print(df.describe())

# Replace 'column_name' with the actual column name
column_to_analyze = 'Rainfall (mm)'

print(f"Mean of {column_to_analyze}:")
print(df[column_to_analyze].mean())

print(f"Median of {column_to_analyze}:")  
print(df[column_to_analyze].median())

print(f"Mode of {column_to_analyze}:")
print(df[column_to_analyze].mode())

print(f"Standard Deviation of {column_to_analyze}:")
print(df[column_to_analyze].std())

print(f"Variance of {column_to_analyze}:")
print(df[column_to_analyze].var())

print(f"Minimum value of {column_to_analyze}:")
print(df[column_to_analyze].min())
print(f'Which is at index {df[column_to_analyze].idxmin()}')

print(f"Maximum value of {column_to_analyze}:")
print(df[column_to_analyze].max())
print(f'Which is at index {df[column_to_analyze].idxmax()}')

print(f"Count of {column_to_analyze}:")
print(df[column_to_analyze].count())

print(f"Sum of {column_to_analyze}:")
print(df[column_to_analyze].sum())

print(f"Frequency of {column_to_analyze}:")
print(df[column_to_analyze].value_counts())
