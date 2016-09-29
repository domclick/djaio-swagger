from schematics.exceptions import DataError
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

    def get_swagger_operation(self, context=default_context):
        """
        get the swagger_schema operation representation.
        """
        consumes = produces = ('application/json',)
        return Operation({
            "summary": self.description,
            "description": self.description,
            "consumes": consumes,
            "produces": produces,
            "parameters": self._get_swagger_parameters(context),
            "responses": {
                "200": {
                    "description": "successful operation",
                    "schema": Schema({
                        "title": "success",
                        "properties": {
                            "success": {"type": "boolean"},
                            "result":{"type":"array"},
                            "errors":{"type":"array"}
                        },
                        "required": ["success"]
                    })
                },
            }
        })

    def get_swagger_schema(self):
        """
        function try to build swagger-json by Scheme Model.
        If dict of data has wrong format in raise an error.
        :return Scheme object:
        """

        scheme = self.raw_func.swagger_dict
        try:
            return Schema(scheme)
        except DataError:
            raise ValueError('Error! Your YAML description is not valid! See the docs here: {docs}\n{scheme}'.
                             format(scheme=scheme, docs='http://swagger.io/specification/#schemaObject'))


    def _get_swagger_parameters(self, context=default_context):

        parameters = []
        if self.raw_func.__name__ in self.BODY_METHODS:
            # Create here a constant field for methods of post and put
            # and if there is a database schema for it then initialize
            body = BodyParameter({
                "name": "body",
                "required": True,
                "description": "Json, Array or other data to POST or PUT",
            })
            schema = self.get_swagger_schema()
            if schema:
                body.schema = schema
            parameters.append(body)

        # Create body IN params
        for name, details in self.parameters.body.items():
            parameters.append(BodyParameter({
                "name": name,
                "description":'body_param: {}'.format(name),
                "required": details.default is None,
                "schema": context.serializers.to_json_schema(details.type),
            }))

        # Create path IN params
        for name, details in self.parameters.path.items():
            parameters.append(PathParameter({
                "name": name,
                "description":name,
                "required": True,
                "type": context.serializers.to_json_schema(details.type) if details else 'string',
            }))


        # Not used for this moment
        # for name, details in self.parameters.query.items():
        #     parameters.append(QueryParameter({
        #         "name": name,
        #         "required": details.default is None,
        #         "type": "string"
        #     }))
        #
        # for name, details in self.parameters.header.items():
        #     parameters.append(HeaderParameter({
        #         "name": name,
        #         "required": details.default is None,
        #         "type": "string"
        #     }))

        return parameters