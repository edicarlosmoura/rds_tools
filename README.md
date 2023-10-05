# rds_tools

Script python to list, turn on or off a rds cluster in diferent AWS accounts an regions.

It's necessary:

    Python 3
    Libs: boto3, argparse, logging and os
    aws-cli configured 


#Usage
python3 script.py -h
usage: script.py [-h] --profile PROFILE --region REGION --action ACTION

Script para listar, ligar e desligar cluster rds

options:
  -h, --help         show this help message and exit
  --profile PROFILE  profile
  --region REGION    aws region
  --action ACTION    stop/start
