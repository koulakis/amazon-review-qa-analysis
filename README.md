# Trusted Users Insight System

## Setup
Go to the `provisioning` folder. To provision an aws instance with spark and run the current notebook, fill in your aws credentials in `aws.tfvar` and add the private and public key you will use to connect to the ec2 instance.
The following commands will launch the an aws instance of type defined in `conf.tfvar` and install everything needed to run spark, the contents of this repo and some sample data files.
```bash
terraform plan -var-file="aws.tfvars" -var-file="config.tfvars" --out plan
terraform apply plan
```
To tear the instance down run:
```bash
terraform destroy -var-file="aws.tfvars" -var-file="config.tfvars"
```
After the instance is up you can ssh and launch pyspark. To connect to the pyspark shell and spark uis, you can open ssh tunnels in the following fashion:
```
ssh -i <you private key filepath> -L 8888:localhost:8888 ubuntu@<instance public url>
ssh -i <you private key filepath> -L 4040:localhost:4040 ubuntu@<instance public url>
```
Beware that closing the shells where the commands where run will terminate the ssh connections.

## Usage
In jupyter notebook open the `Trusted Users Insight System.ipynb` file. Set the name of the dataset you want to use and then run all the cells. Have fun!
