#Cloudlet Gateway
Cloudlet Gateway is a web server that launches cloudlet applications within VMs
and/or containers. The user-facing web server is based on
[flask](http://flask.pocoo.org/). VM orchestration uses [OpenStack
Heat](https://wiki.openstack.org/wiki/Heat). Container orchestration uses
[Docker Swarm](https://docs.docker.com/engine/swarm/). The service sits behind an [OpenVPN](https://openvpn.net/) server
which allows VMs and containers running in OpenStack++ to be publicly addressable without having
a plethora of IPv4 addresses available in your environment.


##Variable Configuration
A number of variables can be configured in ```ansible/roles/cloudlet-gateway/vars/main.yml``` before launching the playbook:
* gateway_ip - This IP of the host where the gateway will run
* gateway_port - The port that the flask web server will run on 
* openstack_flavor - An existing OpenStack flavor for the size of the VM that will be launched
* openstack_image - The OpenStack image to launch for the cluster
* openstack_network - The name of the nova network that was created during OpenStack setup
* ssh_user - The user to SSH into the VM with
* caas_user - The default login that will be created to log into the web portal
* caas_pw - The password associated with caas_user (this will also be used for the Redis cache)

##Installation
The components for the Cloudlet Gateway are **NOT** installed by default when executing the Ansible playbook. To install the Cloudlet Gateway, the Ansible playbook can be executed whilst specifying the gateway tag:

```ansible-playbook -i ./hosts openstackpp.yaml --tags gateway```

By default it will be installed to the controller node.
The Ansible script will install the requirements for the web server into a virtual environment so as not to conflict with the other OpenStack client libraries that are installed at the system level during the setup of the controller node.

##OpenVPN Server Configuration
The Cloudlet Gateway Ansible script will install OpenVPN and easy-rsa on the host. The OpenVPN server configuration will be seeded with a template that has typical values specified in ```/etc/openvpn/cloudletgateway.conf```. Of importance are the following items:
* **local** - the IP address where the OpenVPN server will run; this should be publicly accessible
* **ca, cert, key, dh** - these are paths to the various keys/certs that will be used by OpenVPN; they can be generated by using the easy-rsa tool
* **push** - these are routes that should be pushed to VPN clients when they connect to the OpenVPN server; this should likely match the floating IP pool that was creating during the OpenStack installation steps

More information regarding the OpenVPN server configuration can be found [here](https://openvpn.net/index.php/open-source/documentation/howto.html#config).

###Generating certificate chains with easy-rsa
In order for clients to connect to OpenVPN, a certificate chain has to be created and the client certificate(s) must be distributed to the user clients.
A guide to generating the certificate authority, server certificate, and client certificates can also be found on the OpenVPN [website](https://openvpn.net/index.php/open-source/documentation/howto.html#pki). Be sure to reference the paths to the files that are generated in the OpenVPN server configuration.

##Cluster Creation
Before the Cloudlet Gateway can be used, a Docker Swarm cluster must first be instantiated. 
The ```cloudlet-gateway/scripts/create_cluster.sh``` script will instantiate a cluster of VMs in OpenStack where containers can be executed.

###Prerequisites
Prior to launching the script to create the Docker Swarm cluster, you should ensure that several prerequisites have been met.
* Ensure that a nova network has been created and that the name of the nova network is the same as what was specified in the openstack_network Ansible variable.
* Ensure that a floating IP pool has been created using ```nova floating-ip-bulk-create```
* Download a suitable image and push it into Openstack Glance. For example:
```
wget https://cloud-images.ubuntu.com/trusty/current/trusty-server-cloudimg-amd64-disk1.img
glance image-create --name ubuntu-14.04 --disk-format qcow2 --container-format bare --file trusty-server-cloudimg-amd64-disk1.img  --is-public True --human-readable --progress
```
* Configure the default security group in OpenStack so that there are rules to allowing incoming connections on ports **22** and **2376**.  These ports will be used by the script to SSH into the VM, configure, and test the docker swarm cluster.

###Script Execution
Once the prerequisites have been met, you can initiate the cluster creation using the following script:

```
cd cloudlet-gateway/scripts
./create_cluster.sh -e /root/admin-openrc.sh -n 1 -p test-swarm
```

The -e flag specifies the OpenStack resource file, -n is the number of nodes to put into the cluster, and -p is the prefix for the name of the VM to instantiate. **NOTE: The prefix must be specified as test-swarm at the moment. This should be remedied in a future patch.**

The script will use docker-machine to create one or more VMs in OpenStack and configure them as a cluster where containers can be launched.

##Using the Cloudlet Gateway
###Application Template Creation (Provider Role)
Once the Docker Swarm cluster is initialized, you may log into the web front end. The last task of the Ansible script launches the flask webserver on the gateway_port that was configured in Ansible variables.

Log into the portal using the caas_user and caas_pw you specified in the Ansible variables.
You can then click the button to create an application. The form will allow you to specify a template (.yml file) for your application. You can look in the ```/examples``` directory of the source tree of how the applications should be specified ([OpenStack Heat](https://docs.openstack.org/heat/pike/template_guide/hot_spec.html) syntax for VMs and [Docker Compose](https://docs.docker.com/compose/compose-file/) for containers)

**NOTE: Currently you may only create new application templates if you are logged in as the caas_user you specified during installation. You may create a new user and log in with that user, but that provider will not be able to create applications. This should be remedied in a future patch.** 
###Launch an application (Customer Role)
Once one or more applications have been added by providers, customers can launch an application by making a request at the ```/customers``` endpoint of the web server. Parameters may be passed via URL or in the body of the request and include the following:
* **user_id** - the customer's user id (the user will be created if it does not already exist)
* **app_id** - the application to launch (via POST)/ obtain information about (via GET)
* **action** - valid values are 'create' and 'delete'; only applicable to POST method






