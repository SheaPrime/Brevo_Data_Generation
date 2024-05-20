import pandas as pd
import sqlparse
from faker import Faker
import random
import re
from datetime import datetime
import os
# Initialize Faker
fake = Faker()
# Function to generate specific field data based on naming
convention
def generate_specific_data(field_name, num_rows, first_names=None,
last_names=None):
if 'first_name' in field_name:
return [fake.first_name() for _ in range(num_rows)]
elif 'last_name' in field_name:
return [fake.last_name() for _ in range(num_rows)]
elif 'email' in field_name:
return [f"{fn.lower()}.{ln.lower()}@tbxofficial.com" for
fn, ln in zip(first_names, last_names)] if first_names and
last_names else [fake.email() for _ in range(num_rows)]
elif 'phone' in field_name or 'number' in field_name:
return [fake.phone_number() for _ in range(num_rows)]
elif 'address' in field_name:
return [fake.street_address() for _ in range(num_rows)]
elif 'city' in field_name:
return [fake.city() for _ in range(num_rows)]
elif 'state' in field_name:
return [fake.state() for _ in range(num_rows)]
elif 'zip' in field_name:
return [fake.zipcode() for _ in range(num_rows)]
elif 'country' in field_name:
return [fake.country() for _ in range(num_rows)]
elif 'company_name' in field_name or 'name' in field_name:
return [fake.company() for _ in range(num_rows)]
elif 'dob' in field_name or 'birthday' in field_name or 'date'
in field_name:

return [fake.date_of_birth() for _ in range(num_rows)]
elif 'job_title' in field_name:
return [fake.job() for _ in range(num_rows)]
elif 'gender' in field_name:

return [fake.random_element(['Male', 'Female', 'Non-
binary', 'Other']) for _ in range(num_rows)]

elif 'nationality' in field_name:
return [fake.country() for _ in range(num_rows)]
elif 'ssn' in field_name:
return [fake.ssn() for _ in range(num_rows)]
elif 'tax_id' in field_name or 'ein' in field_name:
return [fake.ein() for _ in range(num_rows)]
elif 'credit_card' in field_name or 'cc_number' in field_name:

return [fake.credit_card_number() for _ in

range(num_rows)]
elif 'cc_expiration' in field_name:
return [fake.credit_card_expire() for _ in

range(num_rows)]
elif 'account_num' in field_name or 'iban' in field_name:
return [fake.iban() for _ in range(num_rows)]
elif 'routing_num' in field_name:
return [fake.routing_number() for _ in range(num_rows)]
elif 'department' in field_name:
return [fake.word() for _ in range(num_rows)]
else:
return [fake.word() for _ in range(num_rows)] # Default

case to generate a random word
# Function to generate data based on column type
def generate_data(column_name, column_type, num_rows,
target_total=None, reference_data=None, first_names=None,
last_names=None):
if reference_data:
return [random.choice(reference_data) for _ in

range(num_rows)]
elif column_type.startswith('INT'):
return [random.randint(1, 1000) for _ in range(num_rows)]
elif column_type.startswith('FLOAT') or
column_type.startswith('DECIMAL'):

if column_name == 'Amount' and target_total is not None:
return generate_total_amount(num_rows, target_total)
return [round(random.uniform(1.0, 1000.0), 2) for _ in

range(num_rows)]
elif column_type.startswith('VARCHAR') or
column_type.startswith('CHAR'):

return generate_specific_data(column_name, num_rows,

first_names, last_names)
elif column_type.startswith('DATE'):
return [fake.date_between_dates(date_start=datetime(2022,
1, 1), date_end=datetime(2024, 12, 31)) for _ in range(num_rows)]
elif column_type.startswith('DATETIME'):
return

[fake.date_time_between_dates(datetime_start=datetime(2022, 1, 1),
datetime_end=datetime(2024, 12, 31)) for _ in range(num_rows)]
elif column_type.startswith('BOOLEAN'):
return [fake.boolean() for _ in range(num_rows)]
else:
return [fake.word() for _ in range(num_rows)] # Default

case to generate a random word
# Function to generate an Amount field that sums to target_total
def generate_total_amount(num_rows, target_total):
amounts = [random.uniform(20.0, 100.0) for _ in range(num_rows
- 1)]
current_total = sum(amounts)
amounts.append(target_total - current_total) # Adjust last
amount to meet the target total

return [round(amount, 2) for amount in amounts]
# Function to parse the DDL and extract table schemas and foreign
keys
def parse_ddl(ddl):
statements = re.split(r'\bTable\b', ddl, flags=re.IGNORECASE)
table_schemas = {}
foreign_keys = {}
for statement in statements:
if not statement.strip():
continue
table_name_match = re.match(r'\s*(\w+)\s*{', statement)
if table_name_match:
table_name = table_name_match.group(1).strip()
columns = {}
fkeys = {}
column_definitions = statement.split('\n')[1:-1] #

Skip the first and last lines

for column_def in column_definitions:
column_def = column_def.strip().strip(',').strip()
if not column_def or column_def.startswith('--'):
continue
if 'ref:' in column_def:
column_name, rest = column_def.split(' ', 1)
column_type = rest.split('[')[0].strip()
ref_match = re.search(r'ref:\s*>\s*(\w+)\.

(\w+)', column_def)

if ref_match:
ref_table = ref_match.group(1)
ref_column = ref_match.group(2)
fkeys[column_name] = (ref_table,

ref_column)

columns[column_name] = column_type
else:
column_parts = re.split(r'\s+', column_def,

maxsplit=1)

if len(column_parts) == 2:
column_name, column_type = column_parts
columns[column_name] = column_type
else:
print(f"Skipping malformed column

definition: {column_def.strip()}")

table_schemas[table_name] = columns
foreign_keys[table_name] = fkeys
return table_schemas, foreign_keys
# Function to generate a DataFrame based on the table schema
def generate_table(schema, num_rows, ref_data=None,
target_totals=None, data_frames=None, id_to_ref=None,

user_inputs=None):
data = {}
first_names = None
last_names = None
for column_name, column_type in schema.items():
if user_inputs.get(column_name) == 'blank':
data[column_name] = ['[PLEASE CHECK]' for _ in

range(num_rows)]
else:
if 'first_name' in column_name:
first_names = generate_specific_data('first_name',

num_rows)

data['first_name'] = first_names
elif 'last_name' in column_name:
last_names = generate_specific_data('last_name',

num_rows)

data['last_name'] = last_names
else:
ref_column_data = ref_data.get(column_name) if

ref_data else None

target_total = target_totals.get(column_name) if

target_totals else None

data[column_name] = generate_data(column_name,
column_type, num_rows, target_total, ref_column_data, first_names,
last_names)
# Generate email if both first_name and last_name are present
if 'first_name' in schema and 'last_name' in schema and
'email' in schema:

data['email'] = generate_specific_data('email', num_rows,

first_names, last_names)
# Calculate Total_Amount for tables with ID and Qty
if 'Total_Amount' in schema:
id_column = list(schema.keys())[-3] # Assuming ID column

is two places before Total_Amount

qty_column = list(schema.keys())[-2] # Assuming Qty

column is one place before Total_Amount

if id_column in schema and qty_column in schema:
quantities = data[qty_column]
ref_table, ref_column = id_to_ref[id_column]
unit_prices =

data_frames[ref_table].set_index(ref_column).loc[data[id_column]]
['Unit_Price']

data['Total_Amount'] = [round(q * p, 2) for q, p in

zip(quantities, unit_prices)]
return pd.DataFrame(data)
# Function to prompt user for inputs for each table
def prompt_user_for_table(table_name, schema, foreign_keys):
user_inputs = {}

print(f"Configuring table: {table_name}")
# Prompt for existing CSV file
use_csv = input(f"Do you have an existing CSV file for the
table '{table_name}'? (yes/no): ").strip().lower()
if use_csv == 'yes':
user_inputs['use_csv'] = True
return user_inputs # No further input needed if using CSV
else:
user_inputs['use_csv'] = False
# Prompt for field-level customization
for column_name, column_type in schema.items():
fill_or_blank = input(f"For the field '{column_name}' in

table '{table_name}', do you want to:\n1. Leave the field
blank\n2. Fill the field using the program\nPlease choose an
option (1/2): ").strip()

user_inputs[column_name] = 'blank' if fill_or_blank == '1'

else 'fill'
return user_inputs
# Function to generate data for all tables defined in the DDL
def generate_data_from_ddl(ddl, output_folder,
specific_table=None, target_totals=None):
table_schemas, foreign_keys = parse_ddl(ddl)
data_frames = {}
ref_data = {}
id_to_ref = {} # Dictionary to map ID columns to their
reference tables and columns
# If generating only a specific table, load existing data from
CSVs
if specific_table:
print(f"Generating data for specific table:

{specific_table}")

for table_name in table_schemas:
if table_name != specific_table:
file_path = os.path.join(output_folder, f"

{table_name}.csv")

if os.path.exists(file_path):
data_frames[table_name] =

pd.read_csv(file_path)
else:
print(f"Error: CSV file '{file_path}' does not

exist. Cannot generate data for dependent tables.")

return None
# Prompt user for each table
user_inputs = {}
for table_name in table_schemas:
if specific_table and table_name != specific_table:
continue

user_inputs[table_name] =

prompt_user_for_table(table_name, table_schemas[table_name],
foreign_keys)
# Generate data for each table, respecting foreign key
dependencies
for table_name in table_schemas:
if specific_table and table_name != specific_table:
continue
schema = table_schemas[table_name]
fkeys = foreign_keys.get(table_name, {})
table_ref_data = {}
# Populate ref_data with columns referenced by foreign

keys

for column, (ref_table, ref_column) in fkeys.items():
if ref_table in data_frames:
table_ref_data[column] = data_frames[ref_table]

[ref_column].tolist()

id_to_ref[column] = (ref_table, ref_column) #

Update id_to_ref with reference table and column

print(f"Generating data for table: {table_name}") # Debug

statement

# Check if generating from CSV
if user_inputs[table_name]['use_csv']:
file_path = os.path.join(output_folder, f"

{table_name}.csv")

if os.path.exists(file_path):
df = pd.read_csv(file_path)
else:
print(f"Error: CSV file '{file_path}' does not

exist.")

continue

else:
num_rows = int(input(f"How many rows do you want to

generate for the table '{table_name}'? "))

df = generate_table(schema, num_rows, table_ref_data,
target_totals, data_frames, id_to_ref, user_inputs[table_name])

output_path = os.path.join(output_folder, f"

{table_name}.csv")

df.to_csv(output_path, index=False)
data_frames[table_name] = df
# Update ref_data for primary keys in the current table
for column in schema:
if column == 'id':
ref_data[column] = df[column].tolist()

return data_frames
# Example usage

ddl = """
"""
# Prompt user for output folder
output_folder = input("Please specify the folder where the CSV
files should be saved: ")
# Prompt user for whole DB or specific table generation
generate_option = input("Do you want to generate the whole
database or just a specific table? (whole/specific):
").strip().lower()
if generate_option == 'specific':
specific_table = input("Please specify the name of the table
to generate: ").strip()
specific_ddl = input("Please input the DDL for the specific
table: ")
data_frames = generate_data_from_ddl(specific_ddl,
output_folder, specific_table=specific_table)
else:
data_frames = generate_data_from_ddl(ddl, output_folder)
# Print the generated data
for table_name, df in data_frames.items():
print(f"Table: {table_name}")
print(df.head())
print()
