OpenStack extension for Cloudlet support
========================================================
A cloudlet is a new architectural element that arises from the convergence of
mobile computing and cloud computing. It represents the middle tier of a
3-tier hierarchy:  mobile device - cloudlet - cloud.   A cloudlet can be
viewed as a "data center in a box" whose  goal is to "bring the cloud closer".

Copyright (C) 2012-2015 Carnegie Mellon University This is a developing project
and some features might not be stable yet.  Please visit our website at [Elijah
page](http://elijah.cs.cmu.edu/).



License
----------

All source code, documentation, and related artifacts associated with the
cloudlet open source project are licensed under the [Apache License, Version
2.0](http://www.apache.org/licenses/LICENSE-2.0.html).



Tested Platform
-------------

- We have tested at Ubuntu 14.04 LTS 64 bits with OpenStack Kilo.


Installation (Using DevStack)
-----------------------------

This repo is OpenStack extension for cloudlet. Therefore, you need to install
OpenStack and [cloudlet
library](https://github.com/cmusatyalab/elijah-provisioning) before installing
this extension. Since installing OpenStack is not trivial if you don't have
experience, we recommend [DevStack](http://devstack.org/), which provides a set
of script to quickly install and test OpenStack. And for cloudlet library, we
provide [fabric script](http://www.fabfile.org/en/latest/) to help you install.
If you already have installed cloudlet library, please start from 3.  The
following installation steps are for [DevStack (all-in-one-single-machine)
case](http://docs.openstack.org/developer/devstack/guides/single-machine.html).


1. Prepare Ubuntu 14.04 64bit


2. Install cloudlet library

    > $ cd ~  
    > $ sudo apt-get install git openssh-server fabric git  
    > $ git clone https://github.com/cmusatyalab/elijah-provisioning  
    > $ cd elijah-provisioning  
    > $ fab install
    > (Require password for you Ubuntu account)  

    For more details and troubleshooting, please read [elijah-provisioning
    repo](https://github.com/cmusatyalab/elijah-provisioning).


3. Install OpenStack using DevStack (This instruction simply follows [DevStack
guidance](http://devstack.org/guides/single-machine.html)).

    > $ cd ~  
    > $ sudo echo "$USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers  
    > $ git clone https://github.com/openstack-dev/devstack.git  
    > $ cd devstack  
    > $ cp samples/local.conf local.conf  
    > (Modify configuration if you need. Details are at [here](http://docs.openstack.org/developer/devstack/guides/single-machine.html#run-devstack)).  
    > $ ./stack.sh  

    Please make sure that all the OpenStack funtionality is working by
    connecting to OpenStack Web interface (http://localhost/).

    If the vanilla OpenStack does not work, please check apache2 and
    keystone-all process and manually run them, if they are not running.


4. Finally, install cloudlet OpenStack extension

    > $ cd ~  
    > $ git clone https://github.com/cmusatyalab/elijah-openstack  
    > $ cd elijah-openstack  
    > $ fab localhost devstack_single_machine  
    > (Require password for you Ubuntu account)  

    After successful installation, please restart OpenStack to reflect changes.

    > (Restart your devstack)  
    > $ ./unstack  
    > $ ./rejoin-stack.sh  
    > (Sometime, you need to manually restart apache2 and keystone-all)  

    This fabric script will check cloudlet library version as well as OpenStack
    installation, and just place relevant files at right directories.  It
    **does not change any existing OpenStack code**, but designed to be purely
    pluggable extension, so you can revert back to original state by reversing
    the installation steps. We instantiate cloudlet features by changing nova
    configuration file at /etc/nova/nova.conf



How to use
-----------

If the installation is successful, you will see a new panel at project tab as
below.  ![OpenStack cloudlet extension
dashboard](https://github.com/cmusatyalab/elijah-openstack/blob/icehouse/doc/screenshot/cloudlet_dashboard_icehouse.png?raw=true)
Or you can check cloudlet extension by listing available OpenStack extension
using standard [OpenStack API](http://developer.openstack.org/api-ref-compute-v2.html#listExtensionsv2).

Then, you can import [Sample Base
VM](https://storage.cmusatyalab.org/cloudlet-vm/precise-baseVM.zip) using
"Import Base VM".  
![Import Base VM](https://github.com/cmusatyalab/elijah-openstack/blob/icehouse/doc/screenshot/import_basevm.png?raw=true)
(VM's account: cloudlet, password: cloudlet)

To resume Base VM, please use "Resume Base VM" button at Images table, and use
"Create VM overlay" button when you ready to create VM overlay from the resumed
VM. Then it will create _VM overlay_ as belows: 
![Creating VM overlay](https://github.com/cmusatyalab/elijah-openstack/blob/icehouse/doc/screenshot/creating_vm_overlay.png?raw=true)
After finishing creating VM overlay (this process can take a long time), you
can download VM overlay using "Download VM overlay" button.

To perform VM synthesis, please use "Start VM Synthesis" button at Instance
table. You need to input URL of the VM overlay you just downloaded.
![Start VM Synthesis](https://github.com/cmusatyalab/elijah-openstack/blob/icehouse/doc/screenshot/vm_synthesis.png?raw=true)


Alternatively, you can use command line client program at
[./client/cloudlet_client.py](https://github.com/cmusatyalab/elijah-openstack/blob/master/client/cloudlet_client.py)



Troubleshooting
-----------------

If you have any problem after installing Cloudlet extension, please follow
below steps to narrow the problem.

1. Check status of OpenStack after restarting services

  > $ sudo nova-manage service list  
  > Binary           Host                                 Zone             Status     State Updated_At  
  > nova-conductor   krha-cloudlet                        internal         enabled    :-)   2014-05-04 15:32:54  
  > nova-network     krha-cloudlet                        internal         enabled    :-)   2014-05-04 15:32:54  
  > nova-consoleauth krha-cloudlet                        internal         enabled    :-)   2014-05-04 15:32:54  
  > nova-scheduler   krha-cloudlet                        internal         enabled    :-)   2014-05-04 15:32:44  
  > nova-cert        krha-cloudlet                        internal         enabled    :-)   2014-05-04 15:32:54  
  > nova-compute     krha-cloudlet                        nova             enabled    :-)   2014-05-04 15:32:54  
  > $

  If any service is not running, Check error message of that service. In
  DevStack, you can find relevant tab at the screen ( 'screen -x' to attach to
  DevStack screen). In regular OpenStack log files are located under
  ``/var/log/nova``.


2. If you still have problem in using Web interface even though every nova
related service is successfully running, then it's likely to be a Dashboard
problem. We can debug it by manually running dashboard in debug mode. In
regular OpenStack, Dashboard's code (Django) is located at
/usr/share/openstack-dashbaord

   You first need to turn on the debug configuration on Django

   > $ cd /usr/share/openstack-dashboard  
   > $ vi ./settings.py

   Change ``DEBUG = False`` to ``DEBUG = True``. Then, turn on the server using specific port

   > $ ./manage.py runserver 0.0.0.0:9090  
   > Validating models...  
   >
   > 0 errors found  
   > Django version 1.4.5, using settings 'openstack_dashboard.settings'  
   > Development server is running at http://0.0.0.0:9090/  
   > Quit the server with CONTROL-C.  
   >

   At this point, you check detail debug messages of Dashboard when you connect 
   __using the specified port (ex. port 9090)__


In DevStack, mostly of steps are as same except that Dashboard root directory is
"/opt/stack/horizon".




Current Limitations
------------

* _Early start optimization_ is turned off

  Early start optimization start VM even before having the memory snapshot of
  the VM. Therefore, it might reject socket connection for the first several
  seconds. We'll update a workaround soon.

