## gvl.utilities

This repository is meant to contain otherwise uncategorised but useful
support scripts/programs for the GVL.

### Launch Multiple GVLs

This script can be used to launch multiple gvls in one go for training workshops.

    $ cd <your work dir>
    $ git clone https://github.com/gvlproject/gvl.utilities
    $ cd gvl.utilities/launch_multiple_gvls
    $ virtualenv .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ python launch_gvl.py --help


Example:

    $ cd gvl.utilities/launch_multiple_gvls
    $ virtualenv .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ python launch_gvl.py -a <access_key> -s <secret_key> -i ami-000035ef -z melbourne-qh2 -p <pass> -u sample_data.txt -c GVLWorkshop -n 5

Usage:

	usage: launch_gvl.py [-h] -a AK -s SK -i IMAGE [-z ZONE] [-t TYPE] -p PASSWORD
	                     -u USER_DATA_FILE [-c CLUSTER_NAME] [-n NUM_INSTANCES]

	optional arguments:
	  -h, --help            show this help message and exit
	  -a AK, --ak AK        Access Key
	  -s SK, --sk SK        Secret Key
	  -i IMAGE, --image IMAGE
	                        AMI id to use
	  -z ZONE, --zone ZONE  Placement zone for instance
	  -t TYPE, --type TYPE  Type of node. Default is m1.medium
	  -p PASSWORD, --password PASSWORD
	                        Password for instance
	  -u USER_DATA_FILE, --user_data_file USER_DATA_FILE
	                        Path to file containing flavour user data
	  -c CLUSTER_NAME, --cluster_name CLUSTER_NAME
	                        Name of cluster
	  -n NUM_INSTANCES, --num_instances NUM_INSTANCES
	                        Number of instances to launch

The user data file specified with the -u option must contain the necessary flavour data to boot the instance, copied from the GVL Launcher.


#### Convert shed_tool_conf.xml to yaml

This script can be used to convert Galaxy's shed_tool_conf.xml file to a list of installable tools in the yaml format required by the GVL playbook.
It's currently used when creating a new GVL flavour to reverse engineer the list of tools to install from a suitably configured Galaxy instance.

Example:

    $ cd gvl.utilities/convert_shed_tools_to_yaml
    $ virtualenv .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ python shed_tool_conf_to_yaml.py -a <access_key> -s <secret_key> -i ami-000035ef -z melbourne-qh2 -p <pass> -u sample_data.txt -c GVLWorkshop -n 5

Usage:

	usage: shed_tool_conf_to_yaml.py [-h] -f FILE

	optional arguments:
	  -h, --help            show this help message and exit
	  -f FILE, --file FILE  Path to <shed_tool_conf.xml> to convert

The program will write out a new file named: shed_tool_list.yaml