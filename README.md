# DB Connectors

This module was built to compile all the connectors I use on a daily basis.

## How to Use:

1. Create a virtual environment with pew is recommended
    
    ```pew new -r /path/to/requirements/file/requirements.txt environment_name```
    
2. Place the ```db_connectors.py``` file into your project's root folder

3. Import the ```Connects``` Class

    ```from db_connectors import Connects```

4. Assign the correspondent variables and attributes
    ``` 
    # Variables
    username = ''
    password = ''
    query = ''
    
    # Attributes
    Connects.<attribute> = <value>
    connects = Connects(username, password, query)
    ```
 
    