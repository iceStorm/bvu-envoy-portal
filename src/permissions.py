from flask_principal import Permission, namedtuple


UserNeed = namedtuple('UserNeed', ['method', 'value'])

# class UserPermission(Permission):
#   need = 
