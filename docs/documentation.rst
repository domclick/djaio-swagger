=================
Autodocumentation
=================

To allow djaio-swagger to autodocument your library,
you must use the TransmuteUrlDispatcher as your application's router:

.. code-block:: python

    from aiohttp import web
    import djaio_swagger

    app = web.Application(
        # a custom router is needed to help find the transmute functions.
        router=djaio_swagger.TransmuteUrlDispatcher())
    )


Afterwards, transmute can generate the swagger json and append it in the appropriate location:


.. code-block:: python

    djaio_swagger.setup(app, getattr(_settings, 'SWAGGER_APP_INFO', None))