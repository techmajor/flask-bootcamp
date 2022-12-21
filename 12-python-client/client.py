import requests

config = {
  "base-url": "http://127.0.0.1:5000"
}

# This client makes API calls to the flask server written for demo purposes by TechMajor.
# Modify the base-url to point to the IP and port where the server is running.

def get_products():
  # Send a GET request
  # response = requests.get(config['base-url']+"/products", params={'q': 'query', 'page': 2})
  response = requests.get(config['base-url']+"/products")
  print(response.status_code)
  # Is response ok
  if(response.ok):
    # Read response as json
    data = response.json()
    # print(data)
    return data
  # response.reason will have the error message, if response is NOT ok
  print(response.reason)
  return None

# This method returns the access_token upon successful login.
# If login is not successful, it returns None
def login(username, password):
  # Send a POST request with headers
  # response = requests.post(url, data={'key': 'value'}, headers={'X-Custom-Header': 'value'})
  response = requests.post(config["base-url"]+"/users/login", 
                          json={"username": username, "password": password})
  if response.ok:
    response_data = response.json()
    # print(response_data)
    access_token = response_data["access_token"]
    # print(access_token)
    return access_token
  
  print(response.reason)
  return None

# This method creates a new product.
# It takes the name, the price of the product and an access_token 
def create_product(name, price, access_token):
  response = requests.post(config["base-url"]+"/products", 
                           json={"name": name, "price": price},
                           headers={'Authorization': "Bearer " + access_token})
  if response.ok:
    response_data = response.json()
    return response_data
  print(response.reason)
  return None

products = get_products()
print(products)

# Login to get access_token
access_token = login("admin", "admin123")
print(access_token)

# Use the above access_token to access protected APIs
prod = create_product("Macbook Pro", 125000, access_token)
print(prod)