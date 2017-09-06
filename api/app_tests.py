import unittest
from v1.aws import *
from app import app as test_app

class EndpointAddInstance(unittest.TestCase):

    def setUp(self):
        test_app.testing = True
        self.app = test_app.test_client()        
        self.elb_name = "default-elb"
        remove_elb_instance(self.elb_name, ["i-0ff680de9fcabc78b"])
            
    def testAddExistingInstance(self):
        add_elb_instance(self.elb_name, ["i-0ff680de9fcabc78b"])

        url = "/elb/{}".format(self.elb_name)        
        response = self.app.post(url, data=dict(instanceId="i-0ff680de9fcabc78b"))
        
        print response.status_code        
        self.failIf(response.status_code != 409)

if __name__ == '__main__':
    unittest.main()