import pandas as pd
path = r'C:\Users\48514\Desktop\North_Files.xlsx'
tables = pd.read_excel(path,sheet_name= ['Categories','Orders','Products','Orderdate','Customers'])

#setting excel objects as 'Python' tables:

table_orders = tables['Orders']
table_categories = tables['Categories']
table_products = tables['Products']
table_orderdate = tables['Orderdate']
table_customers = tables['Customers']


#Removing unneccesary columns in table_orderdate:

table_orderdate_fixed = table_orderdate.drop(['całokwita','nowakolumna'], axis = 1).copy()
table_orderdate_fixed['Gross_profit'] = table_orderdate_fixed ['UnitPrice']*table_orderdate_fixed['Quantity'] * (1-table_orderdate_fixed['Discount'])

#Merging columns and grouping in a way to get total profit for each category:

merged = table_orderdate_fixed.merge(table_products, on= 'ProductID').merge(table_categories, on = 'CategoryID').copy()
categ_gross = merged.loc[:,['Gross_profit','CategoryName']]
categories_with_highest_gross = categ_gross.groupby('CategoryName').agg(Total_gp_per_category = ('Gross_profit','sum')).reset_index()
sorted_categories = categories_with_highest_gross.sort_values(by='Total_gp_per_category',ascending = False)


#Setting flag for delayed orders:

new_table_orders = table_orders.loc[:,['OrderID','RequiredDate','ShippedDate']]
new_table_orders['Delay'] = new_table_orders['RequiredDate']<new_table_orders['ShippedDate']


#Companies with the highest frequency:

grouped_orders = table_orders.groupby('CustomerID').agg(Amount_of_orders = ('OrderID','count')).reset_index()
sorted_orders = grouped_orders.sort_values(by='Amount_of_orders', ascending = False)


#Average Order Value
aov = table_orderdate_fixed['Gross_profit'].mean()
Average_Order_Value = pd.DataFrame({'Name':['Average_Order_Value'],'Result':[round(aov,2)]})


#Export tables to excel file
path = r'C:\Users\48514\Desktop\North_results.xlsx'
with pd.ExcelWriter(path) as writer:
    sorted_categories.to_excel(writer,sheet_name = 'Categories_with_biggest_profit')
    new_table_orders.to_excel(writer,sheet_name = 'Delayed_orders')
    sorted_orders.to_excel(writer,sheet_name = 'Highest_frequency_Companies')
    Average_Order_Value.to_excel(writer,sheet_name = 'Average_Order_Value')
