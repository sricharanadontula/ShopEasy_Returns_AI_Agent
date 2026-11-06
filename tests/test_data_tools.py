
from tools.data_tools import (
    get_request,
    get_order,
    get_customer
)

# Retrieve return request
request = get_request.invoke({
    "request_id": "RET9001"
})

print("\nRETURN REQUEST:")
print(request)

# Retrieve associated order
order = get_order.invoke({
    "order_id": request["order_id"]
})

print("\nORDER DETAILS:")
print(order)

# Retrieve associated customer
customer = get_customer.invoke({
    "customer_id": order["customer_id"]
})

print("\nCUSTOMER DETAILS:")
print(customer)

# Validate relationships
assert request["order_id"] == order["order_id"]
assert order["customer_id"] == customer["customer_id"]

print("\nAll three retrieval tools are working!")
