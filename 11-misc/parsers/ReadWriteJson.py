import requests
import json
 
# Now we have to request our JSON data through
# the API package
res = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(res.text)
print (len(todos))
# To view your Json data, type var and hit enter
#print (todos)
 
# Now our Goal is to find the User who have
# maximum completed their task !!
# i.e we would count the True value of a
# User in completed key.
# {
    # "userId": 1,
    # "id": 1,
    # "title": "Hey",
    # "completed": false,  # we will count
                           # this for a user.
# }
 
# Note that there are multiple users with
# unique id, and their task have respective
# Boolean Values.
 
def find(todo):
    print (todo)
    check = todo["completed"]
    #max_var = todo["userId"] in todos
    #print (max_var)
    return check
 
# # To find the values.
 
value = list(filter(find, todos))
print (value)
print (len(value))

 
# # To write these value to your disk
 
with open("completed.json", "w") as data:
    json.dump(value, data, indent = 2)