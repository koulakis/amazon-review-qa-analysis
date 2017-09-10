#!/bin/bash

set -e

# Installs java
sudo apt-get update
sudo apt-get --assume-yes install default-jdk

# Installs scala
sudo apt-get --assume-yes install scala

# Installs spark
wget https://s3-us-west-2.amazonaws.com/spark-installer/spark-2.1.1-bin-hadoop2.7.tgz
tar -xvf spark-2.1.1-bin-hadoop2.7.tgz 

# Configures spark slave
echo 'ubuntu@localhost' > spark-2.1.1-bin-hadoop2.7/conf/slave

# Installs anaconda
wget https://s3-us-west-2.amazonaws.com/spark-installer/Anaconda2-4.4.0-Linux-x86_64.sh
chmod +x Anaconda2-4.4.0-Linux-x86_64.sh
./Anaconda2-4.4.0-Linux-x86_64.sh -b
sudo apt-get --assume-yes install python

# Adds useful binaries via .profile
echo 'export PATH="$HOME/spark-2.1.1-bin-hadoop2.7/bin:$HOME/spark-2.1.1-bin-hadoop2.7/sbin:$HOME/anaconda2/bin:$PATH"' >> .profile

# PySpark notebook
echo 'alias pyspark-notebook="PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS=notebook pyspark"' >> .profile

# Downloads project
git clone https://github.com/koulakis/amazon-review-qa-analysis.git

# Copies datasets
mkdir amazon-review-qa-analysis/data
mkdir amazon-review-qa-analysis/data/raw_data
mkdir amazon-review-qa-analysis/data/metadata
wget https://s3-us-west-2.amazonaws.com/spark-installer/reviews_Home_and_Kitchen_5.json.gz -O amazon-review-qa-analysis/data/raw_data/reviews_Home_and_Kitchen_5.json.gz
wget https://s3-us-west-2.amazonaws.com/spark-installer/meta_Home_and_Kitchen.json.gz -O amazon-review-qa-analysis/data/metadata/meta_Home_and_Kitchen.json.gz

