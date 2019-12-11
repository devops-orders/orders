Feature: The order store service back-end
    As an Order Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my orders

Background:
    Given the following orders
    | uuid                                   | price | quantity | customer_id | product_id   | Status      |
    | efac5640-0437-4e83-a4d4-37f8a62359d6   |22     | 10       | 1           | 3            | In Progress |
    | 0b152078-c4f9-43fe-91e1-f235a5ac3182   |46     | 68       | 1           | 4            | Cancelled   |
    | be3229b7-179a-4119-ab4d-0e3b83aabfd1   |134    | 112      | 2           | 4            | Delivered   |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Order Demo RESTful Service"
    And I should not see "404 Not Found"

Scenario: Update an Order
    When I visit the "home page"
    And I set the "Product_ID" to "3"
    And I press the "Search" button
    Then I should see "22" in the "Price" field
    Then I should see "10" in the "Quantity" field
    Then I should see "1" in the "Customer_ID" field
    Then I should see "3" in the "Product_ID" field
    Then I should see "In Progress" in the "Status" field
    When I change "Quantity" to "150"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "150" in the "Quantity" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "150" in the results
    And I should not see "10" in the results


Scenario: Create an Order
    When I visit the "Home Page"
    And I press the "Generate" button
    And I set the "Price" to "10"
    And I set the "Quantity" to "1"
    And I set the "Customer_ID" to "10"
    And I set the "Product_ID" to "4"
    And I select "In Progress" in the "Status" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    Then the "ID" field should be empty
    And the "Price" field should be empty
    And the "Quantity" field should be empty
    And the "Customer_ID" field should be empty
    And the "Product_ID" field should be empty
    And the "Status" field should be empty
    When I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "10" in the "Price" field
    And I should see "1" in the "Quantity" field
    And I should see "10" in the "Customer_ID" field
    And I should see "4" in the "Product_ID" field
    And I should see "In Progress" in the "Status" dropdown

Scenario: Cancel an Order
    When I visit the "home page"
    And I set the "Product_ID" to "3"
    And I press the "Search" button
    Then I should see "22" in the "Price" field
    Then I should see "10" in the "Quantity" field
    Then I should see "1" in the "Customer_ID" field
    Then I should see "3" in the "Product_ID" field
    Then I should see "In Progress" in the "Status" dropdown
    When I select "Cancelled" in the "Status" dropdown
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "Cancelled" in the "Status" dropdown

Scenario: Delete an order
    When I visit the "Home Page"
    And I set the "Product_ID" to "3"
    And I press the "Search" button
    When I copy the "ID" field
    And I press the "Delete" button
    Then I should see the message "Order has been Deleted!"

Scenario: Read an order
    When I visit the "home page"
    And I set the "Product_ID" to "3"
    And I press the "Search" button
    Then I should see "22" in the "Price" field
    Then I should see "10" in the "Quantity" field
    Then I should see "1" in the "Customer_ID" field
    Then I should see "3" in the "Product_ID" field
    Then I should see "In Progress" in the "Status" field
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "22" in the "Price" field
    Then I should see "10" in the "Quantity" field
    Then I should see "1" in the "Customer_ID" field
    Then I should see "3" in the "Product_ID" field
    Then I should see "In Progress" in the "Status" field

Scenario: List orders based on Product ID
    When I visit the "home page"
    And I set the "Product_ID" to "4"
    And I press the "Search" button
    Then I should see "46" in the results
    And I should see "134" in the results
    And I should not see "22" in the results

Scenario: List order based on Customer ID
    When I visit the "home page"
    And I set the "Customer_ID" to "2"
    And I press the "Search" button
    Then I should see "112" in the results
    And I should not see "68" in the results
    And I should not see "10" in the results

Scenario: List all orders
    When I visit the "home page"
    And I press the "Search" button
    Then I should see "22" in the results
    And I should see "46" in the results
    And I should see "134" in the results
    And I should not see "1000" in the results


