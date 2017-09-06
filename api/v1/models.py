class MachineInfo:

    def __init__(self, instance_id = None, instance_type = None, launch_date = None):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.launch_date = launch_date

class MachineId:

    def __init__(self, instance_id = None):
        self.instance_id = instance_id