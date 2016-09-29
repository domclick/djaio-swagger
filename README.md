# DJAIO-SWAGGER v0.0.1b

```
djaio-swagger is a battery for djaio-framework. It's replace the default app.router to own
and generate the json specification of your API in swagger-format.
```
*djaio-swagger это батарейка для djaio-framework. Она заменяет дефолтный роутер приложения
на свой и генерирует json спецификацию для Вашего API в swagger-формате*

### INSTALLATION

#### 1. Checkout last version
```ToDo: Add an installation description```
#### 2. Config your application build file.

##### 2.1 Import djaio-swagger 
*Импортируем djaio-swagger*
``` python
import djaio_swagger
```
##### 2.2 In **init_app()** set your application router to **djaio_swagger.TransmuteUrlDispatcher() It will be looks like:**
*В **init_app()** определяем роутер для нашего приложения как **djaio_swagger.TransmuteUrlDispatcher()***
 ``` python
 app = web.Application(router=djaio_swagger.TransmuteUrlDispatcher())
 ```
##### After that you must add **djaio_swagger.setup(app)**
*После этого мы должны добавить строчку:*
``` !before! return app ```
 ``` python
 djaio_swagger.setup(app)
 ```


#### 3 At the end you must config your settings file. An example:
```python
SWAGGER_APP_INFO = {
    'APP_JSON_ROUTE':'/swagger.json',
    'APP_HTML_ROUTE':'/swagger',
    'APP_INFO':{
        "title": "MY COOL API",
        "version": "1.0",
        "description":"Here you can write something from the works of William Shakespeare.",
        "license":{
            "name":"Apache 2.0",
            "url":"http://www.apache.org"
        },
        "contact": {
                "name":"William Shakespeare",
                "url":"https://Romeo-And-Juliet.net",
                "email":"romeo@juliet.net"
        },
        "termsOfService":"to be or not to be"
    }
}
```
 
