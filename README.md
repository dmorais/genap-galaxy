GenAP Galaxy ansible playbooks
===========

A collection of customized ansible playbooks to install postgress, nginx,
Galaxy, Galaxy-tools and manage the installed Galaxies.

This is to be used by the [GenAP][genap] project to configure, test and 
deploy its Galaxies servers.


[genap]:https://www.genap.ca/login

Requirements
------------

These roles require ansible 2.1.2.0 or higher and images with CentOS 6.8
or higher.

How to run
----------

There are several playbooks to be run and their order matter for the 
success of the installation.

- First add list of IPs and hosts to /etc/hosts. **This step will not
be necessary as we move to lxd on CC-Cloud**
```
10.5.5.209       vz
```

- **addkey.yml** - Adds pub key to list of host.
```
 ssh-keyscan vz >>~/.ssh/known_hosts
 
 ansible-playbook addkey.yml —ask-pass
```

- **main.yml** - This is the first playbook to be ran. It coordinated the 
calling of other roles. After the main is finished you should have the 
Galaxy user created, postgres, nginx and supervisord installed and
configured, and uwsgi installed.

- **manage-galaxy-with-supervisord.yml** - Run this playbook to start 
supervisord and Galaxy. Galaxy, ngixn, postgres and supervisord can also
be started/stopped/restarted from this playbook using the right tags.
```
ansible-playbook manage-galaxy-with-supervisor.yml --tags "galaxy-start,stat"

```

- After Galaxy is started connect log into to it as admin and create a
API key. Decrypt the host_var/<host_name>.yml file and past the API key.

- **install-tools-playbook.yml** - installs all tools on the server.

- **post-tool-installation.yml** - Fix some Galaxy bugs and copy the loc 
files and tool-data/shared directory to its right location.


Role Variables
--------------


Author
------
#### David Morais ####