#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
import argparse
import logging
import os

parser = argparse.ArgumentParser(description='Script para listar, ligar e desligar cluster rds')
parser.add_argument('--profile', help='profile', required=True)
parser.add_argument('--region', help='aws region', required=True)
parser.add_argument('--action', help='stop/start', required=True)
args = parser.parse_args()

profile = args.profile
region = args.region
action = args.action

logfile = os.path.join(os.getcwd(), 'log_script_stop_start_rds.log')

## Handler class
class Handler:

    ##Static method to config Logging
    @staticmethod
    def Logger():
        logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def listRDS(profile, region):
    """
    Function to list all cluster rds in an account and region
    """
    session = boto3.Session(profile_name=profile)
    rds = session.client('rds', region_name=region)
    pages = rds.get_paginator('describe_db_clusters').paginate()

    for page in pages:
        clusters = ''
        for dbcluster in page['DBClusters']:
            try:
                clusters += dbcluster['DBClusterIdentifier'] + ','
            except KeyError:
                logging.error("Account: {0}, region: {1}, action: {2}, Error in listRDS()" .format(profile, region, action))
                pass
    return clusters

def actionRDS(action, clusterName):
    """
    Function to check the cluster status and take power on or off action.
    """
    session = boto3.Session(profile_name=profile)
    rds = session.client('rds', region_name=region)

    get_rds_state = rds.describe_db_clusters(DBClusterIdentifier=clusterName)
    rds_state = get_rds_state['DBClusters'][0]['Status']
    logging.info("Account: {0}, region: {1}, action: {2}, RDS cluster: {3}, Cluster status is: {4}" .format(profile, region, action, clusterName, rds_state))

    if action == 'start':
        if rds_state == 'stopped':
            command = rds.start_db_cluster(DBClusterIdentifier=clusterName)
            logging.info("Account: {0}, region: {1}, action: {2}, RDS cluster: {3}, Command to turn ON was executed." .format(profile, region, action, clusterName))
        else:
            logging.warning("Account: {0}, region: {1}, action: {2}, RDS cluster: {3}, Cluster is not stopeed. No action required." .format(profile, region, action, clusterName))

    if action == 'stop':
        if rds_state == 'available':
            command = rds.stop_db_cluster(DBClusterIdentifier=clusterName)
            logging.info("Account: {0}, region: {1}, action: {2}, RDS cluster: {3}, Command to turn OFF was executed." .format(profile, region, action, clusterName))
        else:
            logging.warning("Account: {0}, region: {1}, action: {2}, RDS cluster: {3}, Cluster is not available. No action required." .format(profile, region, action, clusterName))

def main(): 
    """ 
    Filter only time and stg accounts and stop or start action
    Otherside display a warning
    """
    Handler.Logger()
    listClusters = listRDS(profile, region)
    logging.info("Account: {0}, region: {1}, action: {2}, Listing rds clusters " .format(profile, region, action))
    clusters = listClusters.split(',')
            
    """
    Check if the account has rds cluster and perform the action
    """
    if len(clusters) > 1:
        logging.info("Account: {0}, region: {1}, action: {2}, Clusters founded: {3}" .format(profile, region, action, clusters))

        for clusterName in listClusters.split(','):
            if clusterName != '':
                actionRDS(action, clusterName)
    else:
      logging.info("Account: {0}, region: {1}, action: {2}, Account does not have rds cluster" .format(profile, region, action))

if __name__ == "__main__":
    main()
