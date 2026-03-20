import pandas as pd
path = r'C:\Users\48514\Desktop\python csv\my_file (1).csv'
table = pd.read_csv(path, sep = ',')
pd.set_option('display.max_columns',20)

# Clean "Peak" column by removing citations like "[1]" then converting to nullable data type.

table['Peak'] = table['Peak'].str.split('[').str[0]
table['Peak'] = pd.to_numeric(table['Peak'], errors = 'coerce').astype('Int64')

# The same operation with "All Time Peak".

table['All Time Peak'] = table['All Time Peak'].str.split('[').str[0]
table['All Time Peak'] = pd.to_numeric(table['All Time Peak'], errors = 'coerce').astype('Int64')

# Replacing "$" and "," symbols with nothing, then converting "Actual gross" to nullable data type.

table['Actual gross'] = table['Actual gross'].str.replace('$','', regex = False)
table['Actual gross'] = table['Actual gross'].str.replace(',','', regex = False)
table['Actual gross'] = pd.to_numeric(table['Actual gross'], errors = 'coerce').astype('Int64')

# Repeating this process for column named: "Actual gross (in 2022 dollars)".
table['Actual gross(in 2022 dollars)']= table['Actual gross(in 2022 dollars)'].str.replace('$','',regex=False)
table['Actual gross(in 2022 dollars)']= table['Actual gross(in 2022 dollars)'].str.replace(',','',regex=False)
table['Actual gross(in 2022 dollars)']= pd.to_numeric(table['Actual gross(in 2022 dollars)'],errors= 'coerce').astype('Int64')

# Deleting Wikipedia citations "[1]".
# Define special symbols to be removed and iterate through them.
# Removing spaces after deleting symbols.

table['Tour title'] = table['Tour title'].str.split('[').str[0]
symbols_to_remove=['†','‡','*']
for sym in symbols_to_remove:
    table['Tour title'] = table['Tour title'].str.replace(sym,'',regex=False)
table['Tour title'] = table['Tour title'].str.strip()

# Change datatype to string, replacing dash "–" by hyphen '-' and create supporting column "Years_clean" .
# Extract start year and handle cases where end year is missing.
# Fill missing end years with start years and convert both to nullable datatype.

table['Years_clean'] = table['Year(s)'].astype(str).str.replace('–','-',regex = False)
years_split = table['Years_clean'].str.split('-',expand = True) 
table['start'] = years_split[0]
if 1 in years_split.columns:
    table['end'] = years_split[1]
else:
    table['end'] = years_split[0]

table['end'] = table['end'].fillna(table['start'])
table['start'] = pd.to_numeric(table['start'],errors = 'coerce').astype('Int64')
table['end'] = pd.to_numeric(table['end'],errors = 'coerce').astype('Int64')

# Removing unnecessary columns from dataframe.
table = table.drop(columns = ['Year(s)','Ref.']).copy()
table = table.drop(columns = ['Years_clean']).copy()
# Change datatype of "Shows" column to string, then replace "," by nothing, change datatype to numeric

table['Shows'] = table['Shows'].astype(str).str.replace(',','',regex = False)
table['Shows'] = pd.to_numeric(table['Shows'],errors = 'coerce')

# Change datatype in column "Average gross" to string
# Replace signs like "$" or "," by loop usage.
# Change datatype to numeric.

ag = ['$',',']
for znak in ag:
    table['Average gross'] = table['Average gross'].astype(str).str.replace(znak,'')
table['Average gross'] = pd.to_numeric(table['Average gross'],errors = 'coerce')

# Rename some columns with different names
table = table.rename(columns ={'Actual gross(in 2022 dollars)':'Actual_gross_2022_dolars','All Time Peak':'Ath','Actual gross':'Actual_gross','start':'Tour_start_day','end':'End_start_day'})

# Export to excel file
p =  r'C:\Users\48514\Desktop\python csv\Data cleaning singers.xlsx'
table.to_excel(p, sheet_name = 'Result', index = False)
