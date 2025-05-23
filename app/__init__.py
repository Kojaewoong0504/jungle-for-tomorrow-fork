import os
from flask import Flask
from app.core.database import init_db
from app.core.extension import init_extensions, bcrypt, jwt
from jinja2 import Environment

def update_query_params(original, updates):
    params = original.copy()
    params.update(updates)
    return params

def create_app(config=None):
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','static'))
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['SECRET_KEY'] = 'test1231245'
    app.config['JWT_SECRET_KEY'] = 'test'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    # pagination (김민석)
    app.jinja_env.filters['update'] = update_query_params

    init_db(app)
    init_extensions(app)

    from app.controller.admin_controller import router as admin_router
    from app.controller.user_controller import router as user_router
    from app.controller.main_controller import router as main_router
    from app.controller.recommended_items_controller import router as recommended_items_router
    from app.controller.my_list_controller import router as mylist_router

    app.register_blueprint(admin_router)
    app.register_blueprint(user_router)
    app.register_blueprint(main_router)
    app.register_blueprint(recommended_items_router)
    app.register_blueprint(mylist_router)

    return app

