import os
from flask import Flask, request, abort, jsonify, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, setup_db
from authlib.integrations.flask_client import OAuth
from functools import wraps
import json
from six.moves.urllib.parse import urlencode
import requests


AUTH0_CLIENT_ID = 'uwtYXBbc4j5uAiO4fJcNonoojnkyevKM'
AUTH0_CLIENT_SECRET = 's4hnWksDYkt_y09i_CdPSUZnPL0NJmG3EmsewrasJ-WJszFSiG0KDLcUn61ZcXiN'
AUTH0_CALLBACK_URL = 'http://localhost:5000/callback'
AUTH0_DOMAIN = 'sp31051998.auth0.com'
AUTH0_AUDIENCE = 'http://127.0.0.1:5000'
PROFILE_KEY = 'profile'
SECRET_KEY = 'ThisIsTheSecretKey'
JWT_PAYLOAD = 'jwt_payload'
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN



def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    setup_db(app)
    CORS(app)
    

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    def requires_auth(permission = '', permissions = []):
        def requires_auth_decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                if PROFILE_KEY not in session:
                    abort(401)
                    return redirect('/login')
                if permission not in session['permissions']:
                    abort(401)
                return f(*args, **kwargs)
            return decorated
        return requires_auth_decorator
    
    

    # Controllers API
    @app.route('/')
    def home():
        return redirect('/login')


    @app.route('/callback')
    def callback_handling():
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()
        url = 'https://sp31051998.auth0.com/api/v2/users/' + userinfo['sub'] +'/permissions'
        headers = {"authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBaV1Q1UjJ6QURlcFFKTF91cHM0eCJ9.eyJpc3MiOiJodHRwczovL3NwMzEwNTE5OTguYXV0aDAuY29tLyIsInN1YiI6ImZPT2gyUGVVblRWdGtGcFJtbm9wUGRvNndVbTVydmp2QGNsaWVudHMiLCJhdWQiOiJodHRwczovL3NwMzEwNTE5OTguYXV0aDAuY29tL2FwaS92Mi8iLCJpYXQiOjE1OTI3NTMxMjIsImV4cCI6MTU5MjgzOTUyMiwiYXpwIjoiZk9PaDJQZVVuVFZ0a0ZwUm1ub3BQZG82d1VtNXJ2anYiLCJzY29wZSI6InJlYWQ6Y2xpZW50X2dyYW50cyBjcmVhdGU6Y2xpZW50X2dyYW50cyBkZWxldGU6Y2xpZW50X2dyYW50cyB1cGRhdGU6Y2xpZW50X2dyYW50cyByZWFkOnVzZXJzIHVwZGF0ZTp1c2VycyBkZWxldGU6dXNlcnMgY3JlYXRlOnVzZXJzIHJlYWQ6dXNlcnNfYXBwX21ldGFkYXRhIHVwZGF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgZGVsZXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBjcmVhdGU6dXNlcnNfYXBwX21ldGFkYXRhIHJlYWQ6dXNlcl9jdXN0b21fYmxvY2tzIGNyZWF0ZTp1c2VyX2N1c3RvbV9ibG9ja3MgZGVsZXRlOnVzZXJfY3VzdG9tX2Jsb2NrcyBjcmVhdGU6dXNlcl90aWNrZXRzIHJlYWQ6Y2xpZW50cyB1cGRhdGU6Y2xpZW50cyBkZWxldGU6Y2xpZW50cyBjcmVhdGU6Y2xpZW50cyByZWFkOmNsaWVudF9rZXlzIHVwZGF0ZTpjbGllbnRfa2V5cyBkZWxldGU6Y2xpZW50X2tleXMgY3JlYXRlOmNsaWVudF9rZXlzIHJlYWQ6Y29ubmVjdGlvbnMgdXBkYXRlOmNvbm5lY3Rpb25zIGRlbGV0ZTpjb25uZWN0aW9ucyBjcmVhdGU6Y29ubmVjdGlvbnMgcmVhZDpyZXNvdXJjZV9zZXJ2ZXJzIHVwZGF0ZTpyZXNvdXJjZV9zZXJ2ZXJzIGRlbGV0ZTpyZXNvdXJjZV9zZXJ2ZXJzIGNyZWF0ZTpyZXNvdXJjZV9zZXJ2ZXJzIHJlYWQ6ZGV2aWNlX2NyZWRlbnRpYWxzIHVwZGF0ZTpkZXZpY2VfY3JlZGVudGlhbHMgZGVsZXRlOmRldmljZV9jcmVkZW50aWFscyBjcmVhdGU6ZGV2aWNlX2NyZWRlbnRpYWxzIHJlYWQ6cnVsZXMgdXBkYXRlOnJ1bGVzIGRlbGV0ZTpydWxlcyBjcmVhdGU6cnVsZXMgcmVhZDpydWxlc19jb25maWdzIHVwZGF0ZTpydWxlc19jb25maWdzIGRlbGV0ZTpydWxlc19jb25maWdzIHJlYWQ6aG9va3MgdXBkYXRlOmhvb2tzIGRlbGV0ZTpob29rcyBjcmVhdGU6aG9va3MgcmVhZDphY3Rpb25zIHVwZGF0ZTphY3Rpb25zIGRlbGV0ZTphY3Rpb25zIGNyZWF0ZTphY3Rpb25zIHJlYWQ6ZW1haWxfcHJvdmlkZXIgdXBkYXRlOmVtYWlsX3Byb3ZpZGVyIGRlbGV0ZTplbWFpbF9wcm92aWRlciBjcmVhdGU6ZW1haWxfcHJvdmlkZXIgYmxhY2tsaXN0OnRva2VucyByZWFkOnN0YXRzIHJlYWQ6dGVuYW50X3NldHRpbmdzIHVwZGF0ZTp0ZW5hbnRfc2V0dGluZ3MgcmVhZDpsb2dzIHJlYWQ6c2hpZWxkcyBjcmVhdGU6c2hpZWxkcyB1cGRhdGU6c2hpZWxkcyBkZWxldGU6c2hpZWxkcyByZWFkOmFub21hbHlfYmxvY2tzIGRlbGV0ZTphbm9tYWx5X2Jsb2NrcyB1cGRhdGU6dHJpZ2dlcnMgcmVhZDp0cmlnZ2VycyByZWFkOmdyYW50cyBkZWxldGU6Z3JhbnRzIHJlYWQ6Z3VhcmRpYW5fZmFjdG9ycyB1cGRhdGU6Z3VhcmRpYW5fZmFjdG9ycyByZWFkOmd1YXJkaWFuX2Vucm9sbG1lbnRzIGRlbGV0ZTpndWFyZGlhbl9lbnJvbGxtZW50cyBjcmVhdGU6Z3VhcmRpYW5fZW5yb2xsbWVudF90aWNrZXRzIHJlYWQ6dXNlcl9pZHBfdG9rZW5zIGNyZWF0ZTpwYXNzd29yZHNfY2hlY2tpbmdfam9iIGRlbGV0ZTpwYXNzd29yZHNfY2hlY2tpbmdfam9iIHJlYWQ6Y3VzdG9tX2RvbWFpbnMgZGVsZXRlOmN1c3RvbV9kb21haW5zIGNyZWF0ZTpjdXN0b21fZG9tYWlucyB1cGRhdGU6Y3VzdG9tX2RvbWFpbnMgcmVhZDplbWFpbF90ZW1wbGF0ZXMgY3JlYXRlOmVtYWlsX3RlbXBsYXRlcyB1cGRhdGU6ZW1haWxfdGVtcGxhdGVzIHJlYWQ6bWZhX3BvbGljaWVzIHVwZGF0ZTptZmFfcG9saWNpZXMgcmVhZDpyb2xlcyBjcmVhdGU6cm9sZXMgZGVsZXRlOnJvbGVzIHVwZGF0ZTpyb2xlcyByZWFkOnByb21wdHMgdXBkYXRlOnByb21wdHMgcmVhZDpicmFuZGluZyB1cGRhdGU6YnJhbmRpbmcgZGVsZXRlOmJyYW5kaW5nIHJlYWQ6bG9nX3N0cmVhbXMgY3JlYXRlOmxvZ19zdHJlYW1zIGRlbGV0ZTpsb2dfc3RyZWFtcyB1cGRhdGU6bG9nX3N0cmVhbXMgY3JlYXRlOnNpZ25pbmdfa2V5cyByZWFkOnNpZ25pbmdfa2V5cyB1cGRhdGU6c2lnbmluZ19rZXlzIHJlYWQ6bGltaXRzIHVwZGF0ZTpsaW1pdHMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.lnL_zFiHF1NjkRIK6MBNusoUO9NawuxBXQzZ_ocvFHsu2fz8GFzVevMSfvQL1jp7QE_5Qv6I6Up1yiyogO616G8ZOHfIJnX2bpI3WecMLziVGRU-Lbw-SXx7JoqZeiKHkWGXEDCLepUrAGOHlhBaNFHYkZaXdB4hcxRXSjAFDbP-_fFm4spOjCTOr09kQLlyhAP_f1tPPd1u_jUZr5lDkahodTghP7_fmSncgCtdqbhc6ivFWnDppP2SgDMyft5hXV8YMSMEKIAkLwkB7oSou9bmxqdDcG3YmhRCbwdDTlLTY1-d8bHLXYDhx3SBK1hBNB7yJPhYNXHnP1mfxAKplw"}
        req = requests.get(url, headers=headers)
        permissions = []

        response = json.loads(req.text)
        
        for permission in response:
            permissions.append(permission['permission_name'])
        session['permissions'] = permissions
        session[JWT_PAYLOAD] = userinfo
        session[PROFILE_KEY] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/dashboard')


    @app.route('/login')
    def login():
        if session.get(PROFILE_KEY) is not None:
            return render_template('dashboard.html', permissions = session['permissions'])
        else:
            return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


    @app.route('/logout')
    def logout():
        session.clear()
        params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


    @app.route('/dashboard')
    def dashboard():
        if session.get(PROFILE_KEY) is not None:
            return render_template('dashboard.html', permissions = session['permissions'])
        else:
            return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


    
    @app.route('/actors')
    #@requires_auth('get:actors')
    def retrieve_actors():
        selection = Actor.query.order_by(Actor.id).all()
        current_actors = [data.format() for data in selection]
        if len(current_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': current_actors,
            'total_actors': len(Actor.query.all())
        })

    @app.route('/actors', methods=['POST'])
    #@requires_auth('post:actors')
    def create_actor():
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        print(new_name, new_age, new_gender)

        try:
            actor = Actor(name=new_name, age=new_age,
                                gender=new_gender)
            actor.insert()

            return jsonify({
                'success': True,
                'created': actor.format(),
            })
        except Exception as e:
            abort(422)   

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    #@requires_auth('patch:actors')
    def update_actor(actor_id):
        body = request.get_json()
        name = body.get('name', None)
        gender = body.get('gender', None)
        age = body.get('age', None)
        try:
            actor = Actor.query.filter(Actor.id == actor_id)\
                        .one_or_none()
            if actor is None:
                abort(404)
            if name is not None:
                actor.name = name
            if gender is not None:
                actor.gender = gender
            if age is not None:
                actor.age = age
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format(),
            })

        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    #@requires_auth('delete:actors')
    def delete_actor(actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id)\
                        .one_or_none()
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': actor_id,
            })
        except Exception as e:
            abort(404) 

    @app.route('/movies')
    #@requires_auth('get:movies')
    def retrieve_movies():
        selection = Movie.query.order_by(Movie.id).all()
        current_movies = [data.format() for data in selection]
        if len(current_movies) == 0:
            abort(404)
        print((current_movies[0]['release_date']).strftime("%x"))
        return jsonify({
            'success': True,
            'movies': current_movies,
            'total_movies': len(Movie.query.all())
        })
    
    @app.route('/movies', methods=['POST'])
    #@requires_auth('post:movies')
    def create_movie():
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)
        
        try:
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.format(),
            })
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    #@requires_auth('patch:movies')
    def update_movie(movie_id):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        try:
            movie = Movie.query.filter(Movie.id == movie_id)\
                        .one_or_none()
            if movie is None:
                abort(404)
            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format(),
            })

        except Exception as e:
            abort(422)
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    #@requires_auth('delete:movies')
    def delete_movie(movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id)\
                        .one_or_none()
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': movie_id,
            })
        except Exception as e:
            abort(404)
        

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500
    
    @app.errorhandler(401)
    def user_not_authorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "User not authorized"
        }), 401

    return app