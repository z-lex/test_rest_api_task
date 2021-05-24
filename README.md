### API

**namespace**: /api/cars  
Method | URI | Description
------------ | ------------- | ------------- 
GET | /api​/cars​/brands | _List all car brands_  
POST | ​/api​/cars​/brands | _Add car brands list_   
GET | ​/api​/cars​/brands​/{id} | _Get car brand info_  
PUT | ​/api​/cars​/brands​/{id} | _Update car brand info_  
DELETE | ​/api​/cars​/brands​/{id} | _Delete car brand and all car models recursively_  
GET | /api/cars/brands​/{brand_id}​/models | _List all car models of specified brand_
POST | ​/api​/cars​/brands​/{brand_id}​/models | _Create new car model_
DELETE | /api​/cars​/brands​/{brand_id}​/models​/{model_id} | _Delete car model and all its instances recursively_
GET | ​/api​/cars​/brands​/{brand_id}​/models​/{model_id} | _List car models of specified brand_
PUT | /api​/cars​/brands​/{brand_id}​/models​/{model_id} | _Update car model info_

**namespace**: /api/dealers
TODO

### Flask commands
Create empty database:
```bash
flask create-empty-db
```

Create database and populate it with data:
```bash
flask create-db
```


