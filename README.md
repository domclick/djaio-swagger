# DJAIO-SWAGGER v0.0.1b

`djaio-swagger` is an extension for `djaio-framework`. It replaces the default `app.router` and
generates JSON specification of your API in swagger-format.


### INSTALLATION

#### 1. Checkout last version  

```pip install git+git@github.com:Sberned/djaio-swagger.git@master#egg=djaio-swagger```  

#### 2. Config your application build file.  

##### 2.1 Add following lines to your settings 
``` python
CUSTOM_ROUTER = 'djaio_swagger.TransmuteUrlDispatcher'

SWAGGER_APP_INFO = {
    'APP_JSON_ROUTE': '/swagger.json',
    'APP_HTML_ROUTE': '/swagger',
    'APP_INFO':{
        'title': 'MY COOL API',
        'version': '1.0',
        'description': 'Here you can write something from the works of William Shakespeare.',
        'license': {
            'name': 'Apache 2.0',
            'url': 'http://www.apache.org'
        },
        'contact': {
            'name': 'William Shakespeare',
            'url': 'https://Romeo-And-Juliet.net',
            'email': 'romeo@juliet.net'
        },
        'termsOfService': 'to be or not to be'
    }
}
```

##### 2.2 After that add `djaio_swagger.setup(app)` to application init function
 ``` python
 def init_app():
    ...
    djaio_swagger.setup(app)
    
 ```

### HOW TO USE

#### 1. Djaio works with Class-based Views

So, let's write some Class-based View:
``` python
 class TestAPIView(JsonView):
 
    get_method = methods.Testmethod()
    post_method = methods.Testmethod()
    put_method = methods.Testmethod()
    delete_method = methods.Testmethod()
```

Great! But what about swagger? Ok. Djaio-swagger works with `__doc__` of class. In class `__doc__` write YAML model description.

It will be looks like:


``` python
 class TestAPIView(JsonView):
    """
    methods:
        get: This is GET
        post: This is POST
        put: This is PUT
        delete: This is DELETE
    model:
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
    """

    get_method = methods.Testmethod()
    post_method = methods.Testmethod()
    put_method = methods.Testmethod()
    delete_method = methods.Testmethod()
```

Now, navigate your favourite browser or swagger-client to `/swagger.json` and here you go!
