import argparse
from functools import partial
import logging
import multiprocessing
import sys

from bioblend.cloudman import CloudManConfig
from bioblend.cloudman import CloudManInstance
from bioblend.util import Bunch
import yaml


POOL_SIZE = 10

logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def enable_debugging():
    logging.getLogger('bioblend').setLevel(logging.DEBUG)


def launch_gvl(access_key, secret_key, image_id, zone,
               instance_type, cluster_name, password, user_data_file):
    user_data = {}
    with open(user_data_file) as f:
        for key, value in yaml.load(f).iteritems():
            user_data[key] = value

    cloud_metadata = Bunch(id='1',  # for compatibility w/ DB representation
                           name="NeCTAR",
                           cloud_type="openstack",
                           bucket_default="cloudman-gvl-400",
                           region_name="melbourne",
                           region_endpoint="nova.rc.nectar.org.au",
                           ec2_port=8773,
                           ec2_conn_path="/services/Cloud",
                           cidr_range="115.146.92.0/22",
                           is_secure=True,
                           s3_host="swift.rc.nectar.org.au",
                           s3_port=8888,
                           s3_conn_path='/')

    cfg = CloudManConfig(access_key=access_key, secret_key=secret_key,
                         cluster_name=cluster_name, image_id=image_id,
                         instance_type=instance_type, password=password,
                         cloud_metadata=cloud_metadata, placement=zone,
                         **user_data)
    return CloudManInstance.launch_instance(cfg)


def dispatch_instance(access_key, secret_key, image_id, zone,
                      instance_type, cluster_name, password, user_data_file,
                      inst_id):
    instance_name = "{0}-{1}".format(cluster_name, inst_id)
    log.info("Launching instance %s", instance_name)
    launch_gvl(access_key, secret_key, image_id, zone, instance_type,
               instance_name, password,
               user_data_file)


def launch_gvl_instances(access_key, secret_key, image_id, zone,
                         instance_type, cluster_name, password, user_data_file,
                         num_instances, jobs):
    pool = multiprocessing.Pool(jobs)

    func = partial(dispatch_instance, access_key, secret_key, image_id, zone,
                   instance_type, cluster_name, password, user_data_file)
    pool.map(func, xrange(num_instances))
    pool.close()
    pool.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--ak', type=str, help="Access Key", required=True)
    parser.add_argument(
        '-s', '--sk', type=str, help="Secret Key", required=True)
    parser.add_argument(
        '-i', '--image', type=str, help="AMI id to use", required=True)
    parser.add_argument(
        '-z', '--zone', type=str, help="Placement zone for instance",
        required=False)
    parser.add_argument(
        '-t', '--type', type=str, help="Type of node. Default is m1.medium",
        required=False, default="m1.medium")
    parser.add_argument(
        '-p', '--password', type=str, help="Password for instance",
        required=True)
    parser.add_argument(
        '-u', '--user_data_file', type=str,
        help="Path to file containing flavour user data", required=True)
    parser.add_argument(
        '-c', '--cluster_name', type=str, help="Name of cluster",
        required=False, default="GVL")
    parser.add_argument(
        '-n', '--num_instances', type=int,
        help="Total number of instances to launch", required=False, default=1)
    parser.add_argument(
        '-j', '--jobs', type=int,
        help="Maximum number of instances to launch in parallel",
        required=False, default=POOL_SIZE)
    parser.add_argument(
        '-d', '--debug', type=bool,
        help="Enable debug output", required=False, default=False)
    args = parser.parse_args()

    if args.debug:
        enable_debugging()

    launch_gvl_instances(
        args.ak, args.sk, args.image, args.zone, args.type, args.cluster_name,
        args.password, args.user_data_file, args.num_instances, args.jobs)
