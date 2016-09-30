# DJAIO-SWAGGER v0.0.1b
SO, LET ME SPEAK FROM MY HEATRT...

```
djaio-swagger is a battery for djaio-framework. It's replace the default app.router to own
and generate the json specification of your API in swagger-format.
```
*djaio-swagger это батарейка для djaio-framework. Она заменяет дефолтный роутер приложения
на свой и генерирует json спецификацию для Вашего API в swagger-формате*

### INSTALLATION

#### 1. Checkout last version from:
``` sh
github.com:Sberned/djaio-swagger.git@master#egg=djaio-swagger
```

#### 2 At the end you must config your settings file. An example:
```python
CUSTOM_ROUTER = 'djaio_swagger.TransmuteUrlDispatcher'
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
#### 3 Add to **init_app** function in your APP_NAME.__init__.py:
```python
djaio_swagger.setup(app)
```
It will be looks like:

```python
def init_app(app):
    ...
    
    djaio_swagger.setup(app)
    
    ...
    return app
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

For class-methods you must wright it description in ```<%METHOD_NAME%_desc>  %METHOD_DESC% <end_%METHOD_NAME%_desc>```. 
It will be looks like:

``` python
 class TestAPIView(JsonView):
    """
    A class with some magic methods


    <get_desc>This is GET<end_get_desc>
    <post_desc>This is POST<end_post_desc>
    <put_desc>This is PUT<end_put_desc>
    <delete_desc>THIS IS DELETE<end_delete_desc>

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

    get_method = methods.Testmethod()
    post_method = methods.Testmethod()
    put_method = methods.Testmethod()
    delete_method = methods.Testmethod()
```

So, at ```/swagger.json``` you can see the result and use it!
 
