
import pandas as pd

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")
requests = pd.read_csv("data/return_requests.csv")

print("\nCUSTOMERS DATA")
print(customers.head())

print("\nORDERS DATA")
print(orders.head())

print("\nRETURN REQUESTS DATA")
print(requests.head())

print("\nDATASET SHAPES")
print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Return Requests:", requests.shape)

print("\nCOLUMN NAMES")
print("Customers:", customers.columns.tolist())
print("Orders:", orders.columns.tolist())
print("Requests:", requests.columns.tolist())
