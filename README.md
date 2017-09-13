POST /businesses/

{
    "name": "xyz"           # required
    "status": "active"      # optional
}


PATCH /businesses/
{
    "name": "xyz"           # required
    "vendor": "abc"         # required
}

POST /vendors/

{
    "name": "xyz"           # required
    "status": "active"      # optional
}

POST /statuses/

{
    "name": "xyz"           # required
}

