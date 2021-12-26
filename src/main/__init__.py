from flask import Flask

class App(Flask):
    def __init__(self, instance_path):
        super(App, self).__init__(
            import_name=__name__,
            instance_path=instance_path,
            instance_relative_config=True,
        )

        # assigning the base templates & static folder
        self.template_folder = './base/templates'
        self.static_folder = './base/static'

        # loading environment variables
        self.load_environment_variables()

        # registering essential partials for the app
        self.register_base_components()
        self.register_global_functions()
        self.register_blueprints()
        # self.register_cors()
        self.register_error_handlers()
        self.register_login_manager()


    def register_base_components(self):
        """
        Registering base app's components via context_processor to get called each time a new request coming.
        """
        # registering view components
        from .base.components.navbar.navbar_component import navbar_component
        self.context_processor(navbar_component)


    def register_global_functions(self):
        # registering jinja global functions (allow calling from any jinja templates)
        from .base.helpers.jinja_env_functions import extract_avatar_url
        self.jinja_env.globals.update(extract_avatar_url=extract_avatar_url)


    def register_blueprints(self):
        """
        Registering the app's blueprints.
        """
        from .modules.index.index_controller import indx
        from .modules.auth.auth_controller import auth

        self.register_blueprint(indx, url_prefix="/")
        self.register_blueprint(auth, url_prefix="/")


    def register_cors(self):
        # adding CORS origins (all) for client ajax calling
        from flask_cors import CORS
        cors = CORS(app=self, resources={r"/*": {"origins": "*"}})


    def register_error_handlers(self):
        """
        Registering custom error handlers that show custom view (html page) for the app.
        """
        from src.main.base.helpers.error_handlers import ErrorHandler

        self.register_error_handler(403, ErrorHandler.forbidden)
        self.register_error_handler(404, ErrorHandler.not_found)
        self.register_error_handler(500, ErrorHandler.server_error)


    def register_login_manager(self):
        # adding login manager
        from flask_login import LoginManager

        login_manager = LoginManager()
        login_manager.login_view = "auth.login"
        login_manager.init_app(self)

        @login_manager.user_loader
        def load_user(id):
            # register user_loader
            from src.main.modules.user.user_model import User
            return User.query.get(id)


    def load_environment_variables(self):
        """
        Loading the configured environment variables.
        """
        # Load the default configuration (../config/default.py)
        self.config.from_object('config.default')

        # Load the configuration from the instance folder --- overriding the above
        self.config.from_pyfile('./instance/config.py')

        # Load the file specified by the APP_CONFIG_FILE environment variable
        # Variables defined here will override those in the default configuration
        self.config.from_envvar('APP_CONFIG_FILE')

