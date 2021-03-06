from fabric.api import *

APP_NAME = "sre_test"

APP_DIRECTORY = "www/{}".format(APP_NAME)
LOG_DIRECTORY = "www/{}/logs".format(APP_NAME)
TMP_DIRECTORY = "www/{}/tmp".format(APP_NAME)
PID_DIRECTORY = "www/{}/pid".format(APP_NAME)
SOCKET_DIRECTORY = "www/{}/socket".format(APP_NAME)
SYSTEMD_DIRECTORY = "/etc/systemd/system"

REPOSITORY = 'https://github.com/leonardocarbone/loadsm_challenge.git'
REPOSITORY_BRANCH = "master"

DEPENDENCIES = ["flask-restplus", "gunicorn", "boto3"]

def create_directories():            
    directories = [APP_DIRECTORY, LOG_DIRECTORY, TMP_DIRECTORY, PID_DIRECTORY, SOCKET_DIRECTORY]

    run("rm -rf {}".format(APP_DIRECTORY))

    for directory in directories:
        run("mkdir -p {}".format(directory))
    
    
def retrieve_source_code():
    command = "git clone {} --branch {} .".format(REPOSITORY, REPOSITORY_BRANCH)
    
    with cd(TMP_DIRECTORY):
        run(command)
    
    run("mv {}/api/* {}".format(TMP_DIRECTORY, APP_DIRECTORY))    
        
def update_config_files():
    run("mv {}/deploy/gunicorn.conf {}".format(TMP_DIRECTORY, APP_DIRECTORY))    
    sudo("mv {}/deploy/gunicorn.service {}".format(TMP_DIRECTORY, SYSTEMD_DIRECTORY))
    sudo("mv {}/deploy/gunicorn.socket {}".format(TMP_DIRECTORY, SYSTEMD_DIRECTORY))    

def remove_tmp_directory():
    run("rm -rf {}".format(TMP_DIRECTORY))

def install_dependencies():
    for dependency in DEPENDENCIES:
        sudo("pip install {}".format(dependency))

def stop_app():
    sudo("systemctl stop gunicorn.socket")

def start_app():
    sudo("setenforce 0")
    sudo("systemctl daemon-reload")
    sudo("systemctl start gunicorn.socket")

def restart_nginx():
    sudo("service nginx restart")

def deploy(key_pah):
    env.key_filename = key_pah
    
    stop_app()
    create_directories()
    retrieve_source_code()
    update_config_files()
    install_dependencies()
    remove_tmp_directory()
    start_app()
    restart_nginx()