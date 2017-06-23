import json
from aiohttp import web
from swagger_schema import Swagger, Info
from transmute_core.swagger import (
    generate_swagger,
    get_swagger_static_root
)
from djaio_swagger.views import doc_handler


def create_swagger_json_handler(app, app_info=None):
    """
    Create a handler that returns the swagger definition
    for an application.

    This method assumes the application is using the
    TransmuteUrlDispatcher as the router.
    """
    _defailt_app_info = {
        "title": "My App",
        "version": "1.0",
        "description": "My magical application",
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        },
        "contact": {
            "name": "Mr. Black YoYo",
            "url": "https://nomore.org",
            "email": "mrblack@swagger.io"
        },
        "termsOfService": "Some terms of services, by the way"
    }

    spec = Swagger({
        "info": Info(app_info if app_info else _defailt_app_info),
        "paths": app.router.swagger_paths(),
        "schemes": app_info.get("APP_SCHEME", ['http']),
        "swagger": "2.0",

    })

    # Let's validate this
    spec.validate()

    spec = spec.to_primitive()
    encoded_spec = json.dumps(spec).encode("UTF-8")

    async def swagger(request):
        return web.Response(
            # we allow CORS, so this can be requested at swagger.io
            headers={
                "Access-Control-Allow-Origin": "*"
            },
            body=encoded_spec,
            content_type='application/json'
        )

    return swagger


def setup(app):
    """
    a convenience method for both adding a swagger.json route,
    as well as adding a page showing the html documentation
    """
    app_info = getattr(app.settings, 'SWAGGER_APP_INFO', {})
    spec = app_info.get('APP_INFO', None)
    json_route = app_info.get('APP_JSON_ROUTE', '/swagger.json')
    html_route = app_info.get('APP_HTML_ROUTE', '/swagger')

    app.router.add_route('GET', json_route, create_swagger_json_handler(app, spec))
    app.router.add_route('GET', html_route, doc_handler)
