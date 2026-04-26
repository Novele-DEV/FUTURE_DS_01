import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
output_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_data.csv")


import pandas as pd

def load_clean_data():
    return pd.read_csv(output_path)

def compute_KPIs(df):
    total_revenue = (df['Sales']).sum()
    total_order = len(set(df["InvoiceNo"]))
    total_customers = len(set(df["CustomerID"])) 
    avg_order_value = total_revenue/total_order

    return total_revenue, total_order,total_customers,avg_order_value

def sales_by_region(df):
    sales_by_region = df.groupby("Country",as_index = False)['Sales'].sum().sort_values(by ="Country",ascending=True)
    sales_by_region["Country"]= sales_by_region["Country"].astype(str)
    sales_by_region["Sales"]=sales_by_region["Sales"].astype(float)
    return sales_by_region

def top_10_products(df):

    top_10 = df.groupby('Description',as_index = False)['Sales'].sum()
    #sort and take top 10
    top_10 = top_10.sort_values(by = "Sales",ascending=False).head(10)
    #format columns
    top_10["Description"] = top_10["Description"].astype(str)
    top_10["Sales"] = top_10["Sales"].astype(float)

    return top_10

def monthly_trend(df):
    return df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()


if __name__ == "__main__":
    df = load_clean_data()

    revenue, orders,total_customers, avg = compute_KPIs(df)
    listRegionSales:dict = sales_by_region(df)
    listProducts:dict = top_10_products(df)

    print(f"Total Revenue: ${revenue:,.2f}")
    print(f"Average Monthly Revenue: ${revenue/24:,.2f}")
    print(f"Total Orders: {orders:,}")
    print(f"Total Customers: {total_customers:,}")
    print(f"Avg Order Value: ${avg:.2f}")
    print("Top Products ")
    i = 1
    for index,product in listProducts.iterrows():
        print(f"{i}: {product['Description']} | ${product['Sales']:,.2f}")
        i+=1
    print("Countries | Sales")
    for index,country in listRegionSales.iterrows():
          print(f" {country['Country']} | ${country['Sales']:,.2f}")

    print(monthly_trend(df))