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

#### plugins

## API

## CLI usage

## Plugins
- ec2 (using ec2.py)
- ec2_scale
- vagrant
- temp_node (simpler test-kitchen)
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
- [ ] temp_node plugin
- [ ] vagrant plugin


