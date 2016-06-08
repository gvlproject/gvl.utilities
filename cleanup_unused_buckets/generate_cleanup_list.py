import bioblend
from bioblend.cloudman.launch import Bunch
from bioblend.cloudman.launch import CloudManLauncher

import boto
from boto.exception import EC2ResponseError, S3ResponseError
from boto.ec2.regioninfo import RegionInfo
from boto.ec2.connection import EC2Connection
from boto.s3.connection import OrdinaryCallingFormat, S3Connection


import argparse


def get_cluster_pd(a_key, s_key):
    cloud = Bunch(id='-1',
                  name="NeCTAR",
                  cloud_type='openstack',
                  bucket_default='cloudman-os',
                  region_name='NeCTAR',
                  region_endpoint='nova.rc.nectar.org.au',
                  ec2_port=8773,
                  ec2_conn_path='/services/Cloud',
                  cidr_range='115.146.92.0/22',
                  is_secure=True,
                  s3_host='swift.rc.nectar.org.au',
                  s3_port=8888,
                  s3_conn_path='/')

    cml = CloudManLauncher(a_key, s_key, cloud)
    return cml.get_clusters_pd()


def get_ec2_conn(a_key, s_key):
    region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
    conn = boto.connect_ec2(
        aws_access_key_id=a_key,
        aws_secret_access_key=s_key,
        is_secure=True,
        region=region,
        port=8773,
        path='/services/Cloud',
        validate_certs=False)
    return conn


def get_s3_conn(a_key, s_key):
    s3_conn = S3Connection(
        aws_access_key_id=a_key, aws_secret_access_key=s_key,
        is_secure=True, port=8888, host='swift.rc.nectar.org.au',
        path='/', calling_format=OrdinaryCallingFormat())
    return s3_conn


def generate_pd_deletion_candidates(conn, cl_pd):
    instances = conn.get_only_instances()

    do_not_delete_list = {}

    for inst in instances:
        for cluster in cl_pd['clusters']:
            if cluster['cluster_name'] == inst.tags.get('clusterName', None):
                do_not_delete_list[
                    cluster['cluster_name']] = {
                    'instance': inst,
                    'cluster': cluster}

    clusters_to_preserve = [item['cluster']
                            for item in do_not_delete_list.values()]

    deletion_candidates = [
        t for t in cl_pd['clusters'] if t not in clusters_to_preserve]

    return deletion_candidates


def print_deletion_candidates(header, deletion_candidates):
    print("\n\n")
    print(header)
    print('\nBUCKET_NAME\t\t\t\tCLUSTER_NAME')
    for x in deletion_candidates:
        print(x['bucket_name'], '\t', x['cluster_name'])

    print('Total: ', len(deletion_candidates))


def get_bucket_item_count(bucket):
    count = 0
    for key in bucket.list():
        count += 1
    return count


def generate_other_deletion_candidates(s3_conn):
    buckets = s3_conn.get_all_buckets()
    deletion_candidates = []

    for bucket in [b for b in buckets if b.name.startswith('cm-')]:
        try:
            count = get_bucket_item_count(bucket)

            if bucket.get_key('persistent_data.yaml'):
                continue
            elif count <= 4:
                deletion_candidates.append(
                    {'bucket_name': bucket.name, 'cluster_name': None})
        except S3ResponseError:
            pass
    return deletion_candidates


def write_to_file(pd_deletion_candidates, other_deletion_candidates, output):
    with open(output, "w") as f:
        for x in pd_deletion_candidates:
            f.write(x['bucket_name'] + "\n")
        for x in other_deletion_candidates:
            f.write(x['bucket_name'] + "\n")


def generate_deletion_candidates(a_key, s_key, output):
    cluster_pd = get_cluster_pd(a_key, s_key)
    ec2_conn = get_ec2_conn(a_key, s_key)
    pd_deletion_candidates = generate_pd_deletion_candidates(
        ec2_conn,
        cluster_pd)
    print_deletion_candidates("Persistent Data Candidates",
                              pd_deletion_candidates)
    s3_conn = get_s3_conn(a_key, s_key)
    other_deletion_candidates = generate_other_deletion_candidates(
        s3_conn)
    print_deletion_candidates("Non-persistent Data Candidates",
                              other_deletion_candidates)
    write_to_file(pd_deletion_candidates, other_deletion_candidates, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--ak', type=str, help="Access Key",
                        required=True)
    parser.add_argument('-s', '--sk', type=str, help="Secret Key",
                        required=True)
    parser.add_argument('-o', '--output', type=str, help="Output file",
                        required=False, default='cleanup_list.txt')
    args = parser.parse_args()

    generate_deletion_candidates(args.ak, args.sk, args.output)
