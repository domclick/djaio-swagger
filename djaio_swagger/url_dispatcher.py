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

    def get_swagger_dict(self, cls):
        """
        Get YAML description from class __doc__ and transform it to python dict
        """
        doc = cls.__doc__
        if not doc:
            return {}
        try:
            start = str("<start_YAML>")
            end = str("<end_YAML>")
            doc = re.search('%s(.*)%s' % (start, end), doc, re.DOTALL).group(1)
            doc = yaml.load(doc) if doc else {}
        # ToDo Need to add logging here!
        except ValueError:
            pass
        except AttributeError:
            pass
        else:
            pass
        return doc

    def add_transmute_route(self, *args):
        methods, paths, cls, name = args
        swagger_dict = self.get_swagger_dict(cls)

        if type(methods) == str:
            methods=[methods]

        for method in methods:
            obj = cls.__dict__.get(method.lower(), None)
            obj.swagger_dict = swagger_dict
            if obj:
                describe(methods=methods, paths=paths)(obj)
                transmute_func = DjaioTransmuteFunction(obj, args_not_from_request=["request"])
                swagger_path = transmute_func.get_swagger_path(self._transmute_context)
                for p in transmute_func.paths:
                    # add to swagger
                    if p not in self._swagger:
                        self._swagger[p] = swagger_path
                    else:
                        for mth, definition in swagger_path.items():
                            if mth == method.lower():
                                setattr(self._swagger[p], mth, definition)

                    # add to aiohttp
                    # ATTENTION!!! WE ADD a Class to aiohttp, not class-method!
                    aiohttp_path = self._convert_to_aiohttp_path(p)
                    resource = self.add_resource(aiohttp_path)
                    resource.add_route(method, cls)

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
