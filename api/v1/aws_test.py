import unittest
from aws import *

class AWSElbRemoveInstance(unittest.TestCase):

    def setUp(self):
        self.elb_name = "default-elb"
        self.instance_ids = ["i-00c2b690cbd6d345c"]
        add_elb_instance(self.elb_name, self.instance_ids)

    def testRemoveInstanceFromELB(self):        
        remaining_ids = remove_elb_instance(self.elb_name, self.instance_ids)    
        self.failIf("i-00c2b690cbd6d345c" in remaining_ids)


class AWSElbCheckInstance(unittest.TestCase):

    def setUp(self):
        self.elb_name = "default-elb"
        self.instance_ids = ["i-00c2b690cbd6d345c"]
        add_elb_instance(self.elb_name, self.instance_ids)

    def testInstanceMustBeAttachedToELB(self):        
        self.failIf(not is_instance_attached_to_elb(self.elb_name, 'i-00c2b690cbd6d345c'))


class AWSElbAddInstance(unittest.TestCase):

    def setUp(self):
        self.elb_name = "default-elb"
        self.instance_ids = ["i-00c2b690cbd6d345c", "i-0422bcd568711f9bb", "i-0ff680de9fcabc78b"]        
        remove_elb_instance(self.elb_name, self.instance_ids)

    def testAddThreeInstances(self):
        remove_elb_instance(self.elb_name, self.instance_ids)
        added_instances = add_elb_instance(self.elb_name, self.instance_ids)        
        self.failIf(len(added_instances) != 3)
    
    def testAddOneInstance(self):        
        added_instances = add_elb_instance(self.elb_name, [self.instance_ids[1]])
        self.failIf(len(added_instances) != 1)


def main():
    unittest.main()

if __name__ == '__main__':
    main()