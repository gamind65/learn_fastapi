# Step 1: import FastAPI
import string
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

# Step 2: create app instance
# this will be the main point to create all your API
app = FastAPI() 

# Step 3:: create PATH operation
# PATH refer to the last part of the URL 
# stating from the first "/"
# if URL is like "http://gamind.com/yourmom/gay"
# PATH would be "/yourmom/gay"
@app.get("/") # path is /, operations is get
async def root():
    return {"message": f"Hello, GaMinD!"} # return the content

@app.get("/item/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id} # return the content

# oreder matters
# if someone first, it will never return read_gamind function, instead read_someone
@app.get("/name/gamind")
async def read_gamind():
    return {"name":"gamind", 
            "status":"the best in the world"}

@app.get("/name/{someone}")
async def read_someone(someone: str):
    return {"name": someone}


# predifined values
class PokeName(str, Enum):
    pikachu = "Pikachu"
    cinderace = "Cinderace"
    charmander = "Charmander"

@app.get("/pokemon/{poke_name}")
async def read_pokemon(poke_name: PokeName):
    if poke_name is PokeName.pikachu:
        return {"poke_name": poke_name, "message":"dien giat 500k"}
    if poke_name.value == "Cinderace":
        return {"poke_name": poke_name, "message":"tho nuong trui"}
    
    return {"pokemon_name": poke_name, "message":"khong phai rong ma la ky da"}

"""
You can also specify path with file path
using /files/{file_path:path}
:path, tells it that the parameter should match any path.

you can use it like

from fastapi import FastAPI
app = FastAPI()
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
"""



###############################
# QUERY PARAMETERS

# When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.

fake_item_db = [{"item_name":"pencil"},{"item_name":"pen"},{"item_name":"eraser"}]

@app.get("/item/") # parameter if not on path is query
async def read_items(skip: int = 0, limit: int = 10):
    return fake_item_db[skip:skip+limit]

# query is a ser of key values pairs that go after the "?" in a URL and separated by "&" characters

# Example URL: http://127.0.0.1:8000/items/?skip=0&limit=10
# here, query parameter are
# skip with value 0
# limit with value 10

# All the same process that applied for path parameters also applies for query parameters:
# Editor support (obviously)
# Data "parsing"
# Data validation
# Automatic documentation

# As query parameters are not a fixed part of a path, they can be optional and have default values
# so https//127.0.0.1:8000/items/ is equal to
# https://127.0.0.1:8000/items/?skip=0&limit=10

# and if you go to https://127.0.0.1:8000/items/?skip=20
# you will go to skip=20 and limit=10 (since this is default value)


# Optional parameters
# you can also declare optional parameters by setting its deffault parameter to None
@app.get("/back/{item_id}")
async def read_back(item_id: int, q: str | None = None):
    if q: return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# PATH + QUERY multiple parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# query without assign default value to query variables makes it a required query
@app.get("/newly/{newly_id}")
async def read_newly(newly_id: int, q: str):
    return {"newly_id": newly_id, "q": q}



########################################################################################
# REQUEST BODY

# create a new request body
# deffault value is not required
class Item(BaseModel):
    name: str = "Default Item Name"
    description: str = "Wow this is so classic"
    price: float = 0
    freeship: bool = False

@app.post("/items_buy")
async def create_item(item: Item):
    return item
################################
"""
Note:
Operation
- Operation refer to one of the HTTP methods
- aka one of: POST, GET, PUT, DELETE
- and more exotic ones: OPTIONS, HEAD,PATCH, TRACE
- In the HTTP protocol, you can communicate to each path using one (or more) of these methods
"""

"""
When using APIs, you normally use these specific HTTP methods to perform a specific action
Normally, you will use:
- POST: to create data
- GET: to read data
- PUT: to update data
- DELETE: to delete data

in OpenAPI, each of the HTTP methods is called an "operation"

In line 13, you are using get operation
"""

"""
That @something syntax in Python is called a "decorator".

You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).

A "decorator" takes the function below and does something with it.

In our case, this decorator tells FastAPI that the function below corresponds to the path / with an operation get.

It is the "path operation decorator".
"""



