# bovine-inventory
Dynamic Inventory for Ansible

## Design
Static+Dynamic inventory with modular plugin system, api and command line interface

### File Structure Example
./ansible-repo/
.
+/ansible-repo/bovine-inventory/
.
+/ansible-repo/bovine-inventory/bin/
+/ansible-repo/bovine-inventory/static/
+/ansible-repo/bovine-inventory/dynamic/
+/ansible-repo/bovine-inventory/plugins/

### Plugins
- ec2 (using ec2.py)

