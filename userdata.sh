#!/bin/bash
sudo yum update -y
sudo yum install python3 python3-pip -y
sudo yum remove python-requests
pip3 install fastf1 boto3