import inspect

import yaml
import re

from transmute_core import default_context
from transmute_core import describe

from aiohttp.web import UrlDispatcher
from djaio_swagger.transmute import DjaioTransmuteFunction


class TransmuteUrlDispatcher(UrlDispatcher):
    """
    A UrlDispatcher which instruments the add_route function to
    collect swagger spec data from transmuted functions.
    """
    def __init__(self, *args, context=default_context, **kwargs):
        super().__init__()
        self._transmute_context = context
        self._swagger = {}

    def get_swagger_dict(self, handler):
        """
        Get YAML description from class __doc__ and transform it to python dict
        """
        doc = handler.__doc__
        if not doc:
            return {}
        try:
            doc = yaml.load(doc) if doc else {}
        # ToDo Need to add logging here!
        except ValueError:
            pass
        except AttributeError:
            pass
        else:
            pass
        return doc

    def add_route(self, method, path, handler, *, name=None, expect_handler=None):
        """
        Replace a base add_route to own for ClassBasedViews.
        :param method:
        :param path:
        :param handler:
        :param name:
        :param expect_handler:
        :return:
        """
        # Check if handler is class
        if inspect.isclass(handler):
            _swagger_dict = self.get_swagger_dict(handler)
            swagger_model = _swagger_dict.get('model', {})
            swagger_methods = _swagger_dict.get('methods', {})
            if type(method) == str:
                method = [method]

            for m in method:
                m_lower = m.lower()
                obj = dict((inspect.getmembers(handler, predicate=inspect.isfunction))).get(m_lower, None)
                if obj:
                    # Here we set our methods description from a ClassBasedView __doc__
                    setattr(obj,'swagger_dict', swagger_model)
                    setattr(obj, '__doc__', swagger_methods.get(m_lower))

                    describe(methods=method, paths=path)(obj)
                    transmute_func = DjaioTransmuteFunction(obj, args_not_from_request=["request"])
                    swagger_path = transmute_func.get_swagger_path(self._transmute_context)

                    # add to swagger
                    if path not in self._swagger:
                        self._swagger[path] = swagger_path
                    setattr(self._swagger[path], m_lower, swagger_path.to_native().get(m_lower))

                    # add to aiohttp
                    # ATTENTION!!! WE ADD A CLASS BASED VIEW to aiohttp, not class-method!
                    aiohttp_path = self._convert_to_aiohttp_path(path)
                    resource = self.add_resource(aiohttp_path)
                    resource.add_route(m, handler)
        # if it's a function, we return default add_route
        else:
            super().add_route(method, path, handler, name=name,expect_handler=expect_handler)

    def swagger_paths(self):
        """
        returns a swagger Paths object representing all transmute
        functions registered.
        """
        return self._swagger

    @staticmethod
    def _convert_to_aiohttp_path(path):
        """ convert a transmute path to one supported by aiohttp. """
        return path
