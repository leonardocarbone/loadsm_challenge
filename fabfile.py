from fabric.api import *
from automation.deploy import deploy

env.hosts = ["18.221.37.251"]
env.user = "ec2-user"
env.remote_admin = "ec2-user"
env.port = "22"
env.key_filename = "/root/.ssh/sre_key"