import inspect

import yaml
from aiohttp.web import UrlDispatcher
from djaio_swagger.transmute import DjaioTransmuteFunction
from transmute_core import default_context
from transmute_core import describe


class TransmuteUrlDispatcher(UrlDispatcher):
    """
    A UrlDispatcher which instruments the add_route function to
    collect swagger spec data from transmuted functions.
    """

    METHODS = ('get', 'post', 'put', 'delete')

    def __init__(self, *args, context=default_context, **kwargs):
        super(TransmuteUrlDispatcher, self).__init__(None)
        self._transmute_context = context
        self._swagger = {}

    def get_methods_swagger_doc(self, handler):
        doc = getattr(handler, '__doc__')
        return yaml.load(doc) if doc else {}

    def add_to_swagger(self, handler, path):
        for m in self.METHODS:
            method_func = getattr(handler, '{}_method'.format(m), None)
            if method_func:
                describe(methods=m, paths=path)(handler)
                transmute_func = DjaioTransmuteFunction(handler, m, method_func, args_not_from_request=["request"])
                swagger_path = transmute_func.get_swagger_path(self._transmute_context)
                #add to swagger
                if path not in self._swagger:
                    self._swagger[path] = swagger_path
                setattr(self._swagger[path], m, swagger_path.to_native().get(m))


    def add_route(self, methods, path, handler, *, name=None, expect_handler=None):
        """
        Replace a base add_route to own for ClassBasedViews.
        """
        if inspect.isclass(handler):
            resource = self.add_resource(path, name=name)
            if type(methods) == str:
                methods = [methods]
            for m in methods:
                resource.add_route(m, handler, expect_handler=expect_handler)
            self.add_to_swagger(handler, path)
        else:
            super().add_route(methods, path, handler, name=name,expect_handler=expect_handler)

    def swagger_paths(self):
        """
        returns a swagger Paths object representing all transmute
        functions registered.
        """
        return self._swagger
