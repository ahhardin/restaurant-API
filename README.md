# restaurant-API

#### To setup, open a virtual env and install packages
```
> pipenv shell
> pip install -e .
```

#### To run with auto-reloading in terminal:
```
> export FLASK_APP=app.py
> export FLASK_ENV=development
> flask run
```

#### This will run the server on port 5000, to select a different port (here, 8000):
```
> flask run --port 8000
```

#### To run tests
```
> python3 -m unittest tests
```

#### This project serves up a single API endpoint:  
1. `/open-restaurants?datetime={datetime_string}` 
- params:  
    - datetime (required): accepts any valid url-encoded datetime string of the ISO 8601 format (ex: 2021-04-05T14:30:32.453)  
- returns:  
    - an array of restaurant names that are open on that day and time  

