# -*- coding: utf-8 -*-
from aiohttp import web

_HTML = """
<!DOCTYPE html>
<html>
  <head>
    <title>API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body {margin: 0;padding: 0;}</style>
  </head>
  <body>
    <redoc spec-url='/apidocs.json'></redoc>
    <script src="https://rebilly.github.io/ReDoc/releases/latest/redoc.min.js"> </script>
  </body>
</html>
"""

async def doc_handler(request):
    return web.Response(text=_HTML, content_type='text/html')
