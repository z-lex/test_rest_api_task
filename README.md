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
POST | ​/api​/cars​/search | _Search cars with parameters_


**namespace**: /api/dealers
Method | URI | Description
------------ | ------------- | ------------- 
POST | /api/dealers/ | _Add car dealers list_
GET | /api/dealers/ | _List all car dealers_
GET | /api/dealers/{id} | _Get dealer info_
PUT | /api/dealers/{id} | _Update dealer info_
DELETE | /api/dealers/{id} | _Delete dealer and all its centers_
POST | /api/dealers/{dealer_id}/centers | _Create new dealer center_
GET | /api/dealers/{dealer_id}/centers | _List all dealing centers of specified dealer_
PUT | /api/dealers/{dealer_id}/centers/{center_id} | _Update dealer center info_
DELETE | /api/dealers/{dealer_id}/centers/{center_id} | _Delete dealer center_
GET | /api/dealers/{dealer_id}/centers/{center_id} | _Get dealer center info_
PUT | /api/dealers/{dealer_id}/centers/{center_id}/cars | _Update car info_
POST | /api/dealers/{dealer_id}/centers/{center_id}/cars | _Register car in dealer center_
DELETE | /api/dealers/{dealer_id}/centers/{center_id}/cars | _Delete car_

### Flask commands
Create empty database:
```bash
flask create-empty-db
```

Create database and populate it with data:
```bash
flask create-db
```


