# -*- coding: utf-8 -*-
import os
import uuid

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from flask import request, g, session, flash, redirect, url_for, render_template, send_from_directory
from flask_github import GitHub

from bitwrap_io.api import app

BRYTHON_FOLDER = os.path.abspath(os.path.dirname(__file__) + '/_brython')

app.template_folder = os.path.abspath(os.path.dirname(__file__) + '/../templates')
app.static_url_path = ''
app.config['GITHUB_CLIENT_ID'] = os.environ.get('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.environ.get('GITHUB_CLIENT_SECRET')

github = GitHub(app)

@app.route('/<path:path>')
def send_brython(path):
    """ serve static brython files """
    return send_from_directory(BRYTHON_FOLDER, path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    #user = User.query.filter_by(github_access_token=oauth_token).first()
    #if user is None:
    #    user = User(oauth_token)
        #db_session.add(user)

    #user.github_access_token = oauth_token
    #db_session.commit()
    return redirect(next_url)

def factory(options):
    app.secret_key = str(uuid.uuid4())
    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)
    return Site(wsgiResource)

if __name__ == '__main__':
    from livereload import Server
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch('./bitwrap_io/_brython/')
    server.serve(port=8080)
