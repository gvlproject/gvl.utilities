## Deploy Devstack

This script can be used to deploy a devstack instance

Example:

    $ cd gvl.utilities/deploy_devstack
    $ virtualenv .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ cp inventory/hosts.sample inventory/hosts
    $ vi inventory/hosts # point to your desired host
    $ ansible-playbook -i inventory/hosts playbook.yml --extra-vars admin_password=<your password>

Usage:

   Additional variables include:
   --extra-vars admin_password=<your password>
   --extra-vars devstack_version=stable/ocata