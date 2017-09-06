# loadsm_challenge

Steps to deploy this project on a new ec2 instance.
1. Launch a new instance using RHEL image using default security group 
2. Assing Elastic IP
3. Install required packages
```sh
   sudo yum groupinstall "Development Tools"
   wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-10.noarch.rpm
   rpm -ivh epel-release-7-10.noarch.rpm
   sudo rpm -ivh epel-release-7-10.noarch.rpm
   sudo yum --enablerepo=epel
   sudo yum install nginx
```
5. Configure nginx using files deploy/nginx.conf and deploy/webapp.conf

# On you local server
6. Clone this repository
7. Install python dependencies
```python
   pip install -r dependencies
````
8. Run deploy task using secret key
```python
   fab deploy:path_to_private_key
```
