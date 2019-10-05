### NYU-DevOps Orders Squad

README for the orders squad.
##### List Resources
return valid resource endpoints
input:  `GET /orders`
run and test: return 200 and an array of orders
##### Create Resources
add new entry to the database
input: `POST /orders`
run and test: return 201 and location header for GET
##### Read Resources
return resource data
input: `GET /orders/:id`
run and test: return 200 and data with corresponding ID
##### Update Resources
update resource data
input: `PUT /orders/:id`
run and test: return 200 and data for that ID
##### Delete Resources
delete resource data
input: `DELETE /orders/:id`
run and test: return 204
##### Query resources
1. list orders based on customer ID
input: `GET /orders/customers/:customer_id`
run and test: return 200 and all orders placed by this customer
2. list orders based on produce ID
input: `GET /orders/products/:product_id`
run and test: return 200 and all orders of this product
##### Action
input:
run and test:
