from flask_restplus import Api
from endpoints.healthcheck import healthcheck

webapi = Api(title="Site Reliable Engineer Test", version="1.0.0", description="SRE Test - Loadsmart")
webapi.add_namespace(healthcheck)