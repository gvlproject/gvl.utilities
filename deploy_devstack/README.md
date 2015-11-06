## Deploy DevStack

This script will create a basic devstack environment on a target machine with neutron networking and swift.

Example:

    $ ansible-playbook -i inventory/hosts playbook.yml --extra-vars admin_password=<admin_password>