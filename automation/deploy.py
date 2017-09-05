from fabric.api import *

env.hosts = ["18.221.37.251"]
env.user = "ec2-user"
env.remote_admin = "ec2-user"
env.port = "22"
env.key_filename = "/tmp/sre-test.pem"

APP_NAME = "sre_test"

APP_DIRECTORY = "www/{}".format(APP_NAME)
LOG_DIRECTORY = "www/{}/logs".format(APP_NAME)
TMP_DIRECTORY = "www/{}/tmp".format(APP_NAME)
PID_DIRECTORY = "www/{}/pid".format(APP_NAME)
SOCKET_DIRECTORY = "www/{}/socket".format(APP_NAME)

REPOSITORY = 'https://github.com/leonardocarbone/loadsm_challenge.git'
REPOSITORY_BRANCH = "master"

DEPENDENCIES = ["flask-restplus", "gunicorn", "boto3", "supervisor"]

def create_directories():            
    directories = [APP_DIRECTORY, LOG_DIRECTORY, TMP_DIRECTORY, PID_DIRECTORY, SOCKET_DIRECTORY]

    run("rm -rf {}".format(APP_DIRECTORY))

    for directory in directories:
        run("mkdir -p {}".format(directory))
    
    
def retrieve_source_code():
    command = "git clone {} --branch {} .".format(REPOSITORY, REPOSITORY_BRANCH)
    
    with cd(TMP_DIRECTORY):
        run (command)
    
    run("mv {}/api/* {}".format(TMP_DIRECTORY, APP_DIRECTORY))
    
        
def update_config_files():
    run("mv {}/automation/gunicorn.conf {}".format(TMP_DIRECTORY, APP_DIRECTORY))
    #run("mv {}/automation/supervisor.conf {}".format(TMP_DIRECTORY, APP_DIRECTORY))

def install_dependencies():
    for dependency in DEPENDENCIES:
        sudo("pip install {}".format(dependency))

def stop_app():
    print "Stopping..."

def start_app():
    print "Starting..."

def deploy():
    stop_app()
    create_directories()
    retrieve_source_code()
    update_config_files()
    install_dependencies()
    start_app()