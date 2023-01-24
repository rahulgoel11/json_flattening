## Json-flattening

Flatten Json to Relational Dataframe

### Instructions

1. **Install**

```
pip install json-flattening
```

2. **Parameters**
```
json_data: Input data to be flattend, should be dict or list of dict
list_split_to_many: If the final node list data should be splitted to one to many relation(i.e to multiple rows)
ignore_parent_key: Parent Keys to be ignored should be string or list
filter_parent_key: Parent Keys only to be considered should be string or list,if none of key specified is in data,will return empty dataframe
```


3. **Flatten json**

``` Python
from json_flattening import json_flatten

data = [{
    "firstName": "Rack",
    "lastName": "Jackon",
    "gender": "man",
    "age": 24,
    "address": {
        "streetAddress": "126",
        "city": "San Jone",
        "state": "CA",
        "postalCode": "394221"
    },
    "phoneNumbers": [
        { "type": "home", "number": "7383627627" }
    ]
},
{
    "firstName": "rock",
    "lastName": "Jackon",
    "gender": "man",
    "age": 24,
    "address": {
        "streetAddress": "126",
        "city": "San Jone",
        "postalCode": "394221"
    },
    "phoneNumbers": [
        { "type": "home", "number": "7383627627" }
    ]
}]

flatten_data = json_flatten(data)

```

| firstName | lastName | gender | age | address_state | address_streetAddress | address_postalCode | address_city | phoneNumbers_type | phoneNumbers_number |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  
|Rack|Jackon|man|24|CA|126|394221|San Jone|home|7383627627|
|rock|Jackon|man|24|NaN|126|394221|San Jone|home|7383627627|


4. **With ignore parent Key**
```
flatten_data = json_flatten(data,ignore_parent_key=['phoneNumbers','age'])
```
| firstName | lastName | gender | address_state | address_streetAddress | address_postalCode | address_city |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
|Rack|Jackon|man|CA|126|394221|San Jone|
|rock|Jackon|man|NaN|126|394221|San Jone|

