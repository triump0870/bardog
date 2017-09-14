## Bardog Demo App

_**GET /businesses/**_

#### Response Body:

    [
        {
            "_links": {
                "collection": "/businesses/",
                "self": "/businesses/?id=1"
            },
            "created_at": "2017-09-13T13:21:56+00:00",
            "id": 1,
            "modified_at": "2017-09-13T13:21:56+00:00",
            "name": "bardog5",
            "status": {
                "name": "pending"
            },
            "vendors": [
                {
                    "id": 1,
                    "name": "indigo",
                    "status": {
                        "name": "pending"
                    }
                }
            ]
        },
        {
            "_links": {
                "collection": "/businesses/",
                "self": "/businesses/?id=2"
            },
            "created_at": "2017-09-13T13:44:47+00:00",
            "id": 2,
            "modified_at": "2017-09-13T13:44:47+00:00",
            "name": "new",
            "status": {
                "name": "pending"
            },
            "vendors": []
        }
    ]


_**POST /businesses/**_

#### Request Body:

    {
        "name": "xyz",              # required field
        "status": {                 # optional field, will set to pending if not provided
            "name":"active"
        }
    }

#### Response Body:

    {
        "_links": {
            "collection": "/businesses/",
            "self": "/businesses/?id=7"
        },
        "created_at": "2017-09-14T14:00:40+00:00",
        "id": 7,
        "modified_at": "2017-09-14T14:00:40+00:00",
        "name": "xyz",
        "status": {
            "name": "active"
        },
        "vendors": []
    }


_**PATCH /businesses/**_

#### Request Body

    {
        "name": "bardog",               # required
        "vendor": {                     # optional, but required for mapping between business and vendor
            "name":"indigo"
        },
        "status": {                     # optional, but required to change the status of the business
            "name": "active"
        }
    }

#### Response Body

    [
        {
            "_links": {
                "collection": "/businesses/",
                "self": "/businesses/?id=2"
            },
            "created_at": "2017-09-13T13:44:47+00:00",
            "id": 2,
            "modified_at": "2017-09-14T14:05:51+00:00",
            "name": "bardog",
            "status": {
                "name": "active"
            },
            "vendors": [
                {
                    "id": 15,
                    "name": "indigo",
                    "status": {
                        "name": "active"
                    }
                }
            ]
        }
    ]
    
__**GET /vendors/**_

#### Response Body:

    [
        {
            "_links": {
                "collection": "/vendors/",
                "self": "/vendors/?id=1"
            },
            "id": 1,
            "name": "indigo",
            "status": {
                "name": "pending"
            }
        },
        {
            "_links": {
                "collection": "/vendors/",
                "self": "/vendors/?id=2"
            },
            "id": 2,
            "name": "ravi",
            "status": {
                "name": "pending"
            }
        },
        {
            "_links": {
                "collection": "/vendors/",
                "self": "/vendors/?id=3"
            },
            "id": 3,
            "name": "10 st.",
            "status": {
                "name": "pending"
            }
        }
    ]
    
    
_**POST /vendors/**_

#### Request Body:

    {
        "name": "10 downing st.",           # required
        "status": {                         # optional field, will set to pending if not provided
            "name":"active" 
        }
    }
    
#### Response Body:

    {
        "_links": {
            "collection": "/vendors/",
            "self": "/vendors/?id=23"
        },
        "id": 23,
        "name": "Happy Brew",
        "status": {
            "name": "pending"
        }
    }
    
_**PATCH /vendors/**_
  
#### Request Body:

    {
        "name": "Toit",             # required
        "status": {                 # required
            "name":"inactive"
        }
    }
    
#### Response Body:
    
    {
        "_links": {
            "collection": "/vendors/",
            "self": "/vendors/?id=24"
        },
        "id": 24,
        "name": "Toit",
        "status": {
            "name": "inactive"
        }
    }
    
  
_**GET /statuses/**_

#### Response Body:

    [
        {
            "_links": {
                "collection": "/statuses/",
                "self": "/statuses/?id=2"
            },
            "id": 2,
            "name": "active"
        },
        {
            "_links": {
                "collection": "/statuses/",
                "self": "/statuses/?id=4"
            },
            "id": 4,
            "name": "inactive"
        },
        {
            "_links": {
                "collection": "/statuses/",
                "self": "/statuses/?id=1"
            },
            "id": 1,
            "name": "pending"
        }
    ]
    
    
_**POST /statuses/**_

#### Request Body:

    {
        "name": "active"           # required
    }

#### Response Body:

    {
    "_links": {
        "collection": "/statuses/",
        "self": "/statuses/?id=5"
    },
    "id": 5,
    "name": "active"
}