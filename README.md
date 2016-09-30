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
class RomeoAndJulliet(web.View):
 
    async def get(self):
        ...some code here...
        return
        
    async def post(self):
        ...some code here...
        return
```

Great! But what about swagger? Ok. Djaio-swagger works with `__doc__` of class and methods. In class `__doc__` write YAML model description and enclose it in tags `<start_YAML>  %YAML_SPEC% <end_YAML>`.

In class-method you have to write a short and informative method description.
Djaio-swagger will automatically add a body parameter to your PUT and POST methods. 
For ALL methods it will automatically generate input parameters from functions. 
For now djaio-swagger accepts only PATH and BODY parameters.
Like this:

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
        returns a list
        """
        ...some code here...
        return
        
    async def post(self):
        """
        creates something
        """
        ...some code here...
        return
```

Now, navigate your favourite browser or swagger-client to `/swagger.json` and here you go!
