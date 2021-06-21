from .main import SignupApi,LoginApi

 def initialize_routes(api):
 api.add(SignupApi, '/api/auth/signup')
 api.add(LoginApi, '/api/auth/login')