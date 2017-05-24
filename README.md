# bovine-inventory
Dynamic Inventory for Ansible

This is a WORK IN PROGRESS.  It does NOT yet work. 

## Design
Static+Dynamic inventory with modular plugin system, api and command line interface

### File Structure Example
```
./ansible-repo/
.
+/ansible-repo/bovine-inventory/
.
+/ansible-repo/bovine-inventory/bin/
+/ansible-repo/bovine-inventory/static/
+/ansible-repo/bovine-inventory/static/groups/
+/ansible-repo/bovine-inventory/static/hosts/
+/ansible-repo/bovine-inventory/static/.meta/
+/ansible-repo/bovine-inventory/dynamic/
+/ansible-repo/bovine-inventory/plugins/
```

### Details

#### bin
Whithin the bin folder, we will have the main entry point script:
bovine_inventory.py

as well as the rest of this repo:
lib/bovine
plugins/

#### static
Within the static folder, we have two primary subfolders that will contain a series of yaml files, named for the group or host.  Unlike v1 of the bovine-inventory, v2 doesn't allow a host or group to be defined more than once.  

Each type may contain:
---Groups---
- hosts
- vars
- children

---Hosts---
- vars

#### dynamic
This directory is where a user can put any scripts (preferably Python) to manipulate the inventory at the last stage before it is sent to Ansible.  This is where the truly "dynamic" portion of the inventory will allow one to add/change the inventory based on custom business logic. 

#### plugins
This directory will contain symlinks to plugins from bin/plugins/.  Any directories symlinked here will be "activated", the same way that apache2 on debian based systems and icinga2 works.  

## API

## CLI usage

## Plugins
- ec2 (using ec2.py)
- ec2_scale
- vagrant
- test_node (simpler test-kitchen)
- test_kitchen
- triton (joyent)
- digital ocean
- linode
- vultr
- gce

## TODO
- [ ] flesh out ORM for yml read/writes
- [x] class to calculate group hierarchy
- [ ] complete API
- [ ] complete CLI
- [ ] dynamic vars
- [ ] ec2 plugin
- [ ] test ec2 blue/green deployment / upgrades
- [ ] test_node plugin
- [ ] vagrant plugin


