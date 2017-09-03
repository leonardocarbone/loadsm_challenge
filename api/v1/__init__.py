from flask_restplus import Api
from endpoints.healthcheck import endpoint as healthcheck_endpoint
from endpoints.elb import endpoint as elb_endpoint

webapi = Api(title="Site Reliable Engineer Test", version="1.0.0", description="SRE Test - Loadsmart")
webapi.add_namespace(healthcheck_endpoint)
webapi.add_namespace(elb_endpoint)