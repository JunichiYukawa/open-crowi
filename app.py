# coding : utf-8
import codecs
from urlparse import urlparse

from flask import Flask, request, make_response
import mistune
import custom
from pymongo import MongoClient

app = Flask(__name__, static_folder='public')

html_template = u'''<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link rel="stylesheet" href="/public/css/crowi.min.css">
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/railscasts.min.css">
    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"></script>
</head>
<body>
<div class="container-fluid">
{0}
</div>
</body>
<script>hljs.initHighlightingOnLoad();</script>
</html>
'''

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def http(path):
    html = ''
    renderer = custom.HighlightRenderer()
    md = mistune.Markdown(renderer=renderer)

    #obj = urlparse(request.url)
    #client = MongoClient('localhost', 27017)
    #db = client.db

    with codecs.open('fixtures/sample.md', 'r', 'utf-8') as fr:
        md_text = fr.read()
        body = md(md_text)
    html = html_template.format(body)
    response = make_response(html)
    response.mimetype = 'text/html'
    return response


if __name__ == '__main__':
    app.run()