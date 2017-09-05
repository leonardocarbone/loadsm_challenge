from fabric.api import *
#from fabric.context_managers import cd

env.hosts = ["18.221.37.251"]
env.user = "ec2-user"
env.remote_admin = "ec2-user"
env.port = "22"
env.key_filename = "/tmp/sre-test.pem"

APP_NAME = "sre_test"
#HOME_DIRECTORY = "/home/ec2-user"

APP_DIRECTORY = "www/{}".format(APP_NAME)
LOG_DIRECTORY = "www/{}/logs".format(APP_NAME)
TMP_DIRECTORY = "www/{}/tmp".format(APP_NAME)

REPOSITORY = 'https://github.com/leonardocarbone/loadsm_challenge.git'
REPOSITORY_BRANCH = "master"


def create_directories():            
    directories = [APP_DIRECTORY, LOG_DIRECTORY, TMP_DIRECTORY]

    #with cd(HOME_DIRECTORY):
    run("rm -rf {}".format(APP_DIRECTORY))

    for directory in directories:
        run("mkdir -p {}".format(directory))
    
    
def retrieve_source_code():
    command = "git clone {} --branch {} .".format(REPOSITORY, REPOSITORY_BRANCH)
    
    with cd(TMP_DIRECTORY):
        run (command)
    
    run("mv {}/api/* {}".format(TMP_DIRECTORY, APP_DIRECTORY))
        

def deploy():
    create_directories()
    retrieve_source_code()    