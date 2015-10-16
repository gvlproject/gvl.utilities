## Convert shed_tool_conf.xml to yaml

This script can be used to convert Galaxy's shed_tool_conf.xml file to a list of installable tools in the yaml format required by the GVL playbook.
It's currently used when creating a new GVL flavour to reverse engineer the list of tools to install from a suitably configured Galaxy instance.

Example:

    $ cd gvl.utilities/convert_shed_tools_to_yaml
    $ virtualenv .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ python shed_tool_conf_to_yaml.py -f /mnt/galaxy/galaxy-app/config/shed_tool_conf.xml

Usage:

	usage: shed_tool_conf_to_yaml.py [-h] -f FILE

	optional arguments:
	  -h, --help            show this help message and exit
	  -f FILE, --file FILE  Path to <shed_tool_conf.xml> to convert

The program will write out a new file named: shed_tool_list.yaml