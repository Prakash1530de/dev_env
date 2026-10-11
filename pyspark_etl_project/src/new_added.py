```python
import pandas as pd
import os

# 1. EXTRACT
input_file = "input/employees.csv"
output_file = "output/cleaned_employees.csv"

df = pd.read_csv(input_file)
print("Data extracted successfully")
print(df)

# 2. TRANSFORM
df = df.drop_duplicates()
df = df.dropna()

# Add a new column
df["annual_salary"] = df["salary"] * 12

# Filter employees with salary greater than 45000
df = df[df["salary"] > 45000]

print("Data transformed successfully")
print(df)

# 3. LOAD
os.makedirs("output", exist_ok=True)

df.to_csv(output_file, index=False)

print("Data loaded successfully")
print(f"Output saved to: {output_file}")
```