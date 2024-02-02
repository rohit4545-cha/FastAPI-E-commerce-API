This FastAPI project is a simple E-commerce API for managing products and orders. It is built using FastAPI, MongoDB, and PyMongo.

Table of Contents
Installation
Usage
Endpoints
List Products
Create Order
MongoDB Configuration
Project Structure
Installation
Clone the repository:


git clone https://github.com/rohit4545-cha/FastAPI-E-commerce-API.git
cd FastAPI-E-commerce-API
Install the dependencies:


pip install -r requirements.txt
Set up your MongoDB Atlas account and configure the MongoDB connection in main.py and mongo_queries.py using your credentials.

Run the FastAPI application:


python main.py
Usage
The FastAPI E-commerce API provides endpoints for listing products and creating orders. You can interact with the API using HTTP requests.

Endpoints
List Products
Endpoint: /products/
Method: GET
Parameters:
limit (optional, default: 10) - Number of records to return.
offset (optional, default: 0) - Offset from where to start.
min_price (optional) - Minimum product price.
max_price (optional) - Maximum product price.
Response:
Returns a JSON response containing a list of products based on the provided filters.
Create Order
Endpoint: /orders/
Method: POST
Request Body:
JSON object containing items and user_address.


Example:
json

{
  "items": [
    {
      "productId": "product_id_1",
      "boughtQuantity": 2,
      "totalAmount": 999.98
    },
    {
      "productId": "product_id_2",
      "boughtQuantity": 1,
      "totalAmount": 899.99
    }
  ],
  "user_address": {
    "street": "123 Main St",
    "city": "Exampleville",
    "zip_code": "12345"
  }
}


Response:
Returns a JSON response with the details of the created order.

MongoDB Configuration
The MongoDB configuration is stored in the mongo_queries.py file. Update the get_mongo_client function with your MongoDB Atlas credentials.

username = "your_username"
password = "your_password"
client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.1bnlbko.mongodb.net/")


Project Structure
main.py: FastAPI application containing the API endpoints.
mongo_queries.py: MongoDB connection and query functions.
requirements.txt: List of project dependencies.
README.md: Project documentation.
