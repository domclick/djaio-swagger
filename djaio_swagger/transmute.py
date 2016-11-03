from schematics.exceptions import DataError
from swagger_schema import HeaderParameter
from swagger_schema import QueryParameter
from transmute_core.function import TransmuteFunction
from swagger_schema import (Operation, Schema, PathParameter, BodyParameter)
from transmute_core.context import default_context


class DjaioTransmuteFunction(TransmuteFunction):
    """
    Class based on TransmuteFunction.
    For our realies we rebuild it's main functions and adapt it
    for djaio and ClassBasedView architecture
    """
    BODY_METHODS = ('post', 'put')
    QUERY_METHODS = ('get', )

    def __init__(self, func, method, method_func, args_not_from_request=None):
        super().__init__(func, args_not_from_request=args_not_from_request)
        self.current_method = method
        self.method_func = method_func
        self.input_model = getattr(self.method_func, 'input_model', None)
        self.output_model = getattr(self.method_func, 'output_model', None)
        self.description = getattr(self.method_func, "description", "")

    def get_swagger_operation(self, context=default_context):
        """
        get the swagger_schema operation representation.
        """
        consumes = produces = ('application/json',)
        operation_dict = {
            'tags':[self.paths.copy().pop()],
            "summary": self.description,
            "description": self.description,
            "consumes": consumes,
            "produces": produces,
            "parameters": self._get_swagger_parameters(context),
            "responses": {
                "200": {
                    "description": "successful operation",
                },
            }
        }

        scheme = self.get_swagger_scheme(model=self.output_model)
        if scheme.to_primitive() !={}:
            operation_dict['responses']['200']['schema'] = scheme
        return Operation(operation_dict)

    def get_swagger_scheme(self, model, context=default_context):
        """
        function try to build swagger-json by Scheme Model.
        If dict of data has wrong format in raise an error.
        :return Scheme object:
        """

        scheme = {
            'required': [],
            'type': 'object',
            'properties': {
            }
        }
        if model:
            for f in model().keys():
                field = getattr(model, f)
                if field.required:
                    scheme['required'].append(f)
                try:
                    scheme['properties'][f] = context.serializers.to_json_schema(field)
                except:
                    scheme['properties'][f] = {'type': 'string'}

        try:
            return Schema(scheme)
        except DataError:
            raise ValueError('Error! Your YAML description is not valid! See the docs here: {docs}\n{scheme}'.
                             format(scheme=scheme, docs='http://swagger.io/specification/#schemaObject'))


    def _get_swagger_parameters(self, context=default_context):
        parameters = []

        # Create body IN params
        for name, details in self.parameters.body.items():
            parameters.append(BodyParameter({
                "name": name,
                "description": name,
                "required": details.default is None,
                "schema": context.serializers.to_json_schema(details.type) if details else 'string',
            }))

        # Create path IN params
        for name, details in self.parameters.path.items():
            parameters.append(PathParameter({
                "name": name,
                "description": name,
                "required": True,
                "type": context.serializers.to_json_schema(details.type) if details else 'string',
            }))

        for name, details in self.parameters.query.items():
            print(name, details)
            parameters.append(QueryParameter({
                "name": name,
                "required": details.default is None,
                "type": "string"
            }))

        for name, details in self.parameters.header.items():
            parameters.append(HeaderParameter({
                "name": name,
                "required": details.default is None,
                "type": "string"
            }))



        if self.current_method in self.BODY_METHODS:
            # Create here a constant field for methods of post and put
            # and if there is a database schema for it then initialize
            body = BodyParameter({
                "name": "body",
                "required": True,
                "description": "Json, Array or other data to POST or PUT",
            })
            scheme = self.get_swagger_scheme(model=self.input_model)
            if scheme:
                body.schema = scheme
            parameters.append(body)


        if self.current_method in self.QUERY_METHODS and self.input_model:
            for p in self.input_model().keys():

                if not p in list(self.parameters.path.keys()):
                    field = getattr(self.input_model, p)
                    param_type = context.serializers.to_json_schema(field).get('type', 'string')
                    param = QueryParameter({
                        "name": field.name,
                        "required": False,
                        "type": param_type,
                    })
                    if param_type == 'array':
                        param.collectionFormat = 'multi'
                    parameters.append(param)
        return parameters
