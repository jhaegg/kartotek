# Arcane Kartotek

API and more for Magic: The Gathering collections

## API
Parameters may be sent as `application/x-www-form-urlencoded` and query string
### /user
#### POST
Create a new user
##### Parameters
* `username` - Name of new user
* `password` - Password of new user
##### Response
```
{
  "user_id": 32
}
```

### /have/{user_id}
#### GET
Get have list for a user
##### Response
```
[
  {
    "mvid": 410046,
    "name": "Port Town",
    "ratity": "Rare",
    "num_regular": 2,
    "num_foil": 0
  },
  ...
]
```

#### POST
Requires authentication. Update have list with CSV. The CSV file should be the POST body.
##### Parameters
* `mvid` - Field that contains Multiverse ID, default `mvid`
* `num_regular` - Field that contains number of regular cards, default `num_regular`
* `num_foil` - Field that contains number of foiled cards, default `num_foil`
