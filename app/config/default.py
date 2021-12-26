#   default environment variables for use both in production & development,
#   the variables that don't need to changed between environments should be only placed here.
#


APP_NAME = "Cổng thông tin Đại Sứ BVU"

SECRET_KEY = "bvu_envoy"

# only listed roles can access resources
RBAC_USE_WHITE = True

# get called in the App class's load_environment_variables()
SQLALCHEMY_DATABASE_URI = 'sqlite:///../../db/app.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = True
