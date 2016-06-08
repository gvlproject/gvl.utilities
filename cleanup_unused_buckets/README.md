## Cleanup unused buckets

This script can be used to generate a list of potentially unused cloudman buckets. There's an additional support script
to enable the bulk deletion of the generated list. This latter script first downloads/backs up the bucket locally before
deleting it from the object store.

Example:

    $ cd gvl.utilities/cleanup_unused_buckets
    $ virtualenv .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ mkdir backup
    $ cd backup
    $ python ../generate_cleanup_list.py -a <ACCESS_KEY> -s <SECRET_KEY> -o candidate_list.txt
    $ source GenomicsVL_Students-openrc.sh
    $ python ../delete_cleanup_list.sh candidate_list.txt

Usage:

    usage: generate_cleanup_list.py [-h] -a AK -s SK [-o OUTPUT]
    
    optional arguments:
      -h, --help            show this help message and exit
      -a AK, --ak AK        Access Key
      -s SK, --sk SK        Secret Key
      -o OUTPUT, --output OUTPUT
                            Output file

If no output file is specified, the filename will default to cleanup_list.txt