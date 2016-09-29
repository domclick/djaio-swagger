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


### HOW TO USE

#### 1. Djaio works with Class-based Views
So, lets wright some Class-based View:

``` python
 class RomeoAndJulliet(web.View):
 
    async def get(self):
        ...some code here...
        return
        
    async def post(self):
        ...some code here...
        return
```

Greate! But what about swagger? Ok. djaio-swagger works with ```__doc__``` of class an class-methods. In class __doc__ you must wright a YAML model description and enclosed it in tags ```<start_YAML>  %YAML_SPEC% <end_YAML>```.

In class-method you must wrigh just a method short and informative description.
djaio-swagger will automate add a body parameter for PUT and POST methods. For ALL methods it will be automaticly generate in parametrs if it defined in function. On this time djaio-swagger accepts only PATH and BODY parameters.
It will be looks like:

``` python
 class RomeoAndJulliet(web.View):
    """
    A class with some magic methods
    <start_YAML>
    type: object
    required:
      - id
      - name
    properties:
      id:
        type: integer
        format: int32
      name:
        type: string
    <end_YAML>
    """
    
    async def get(self):
        """
        returns a  list
        """
        ...some code here...
        return
        
    async def post(self):
        """
        creates some thing
        """
        ...some code here...
        return
```

So, at ```/swagger.json``` you can see the result and use it!
 
