import unittest
from aws import *

class AWSTests(unittest.TestCase):

    def setUp(self):
        self.elb_name = "default-elb"

    def testRemoveInstanceFromELB(self):
        instance_ids = ["i-0422bcd568711f9bb"]
        remaining_ids = remove_elb_instance(self.elb_name, instance_ids)    
        self.failIf("i-0422bcd568711f9bb" in remaining_ids)


    def testInstanceMustBeAttachedToELB(self):        
        self.failIf(not is_instance_attached_to_elb(self.elb_name, 'i-00c2b690cbd6d345c'))


def main():
    unittest.main()

if __name__ == '__main__':
    main()