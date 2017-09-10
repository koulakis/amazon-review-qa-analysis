variable "access_key" {}
variable "secret_key" {}
variable "instance_type" {}

provider "aws" {
  region = "us-west-2"
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
}

resource "aws_security_group" "allow_all_tcp" {
  name        = "allow_all_tcp"
  description = "Allow all inbound tcp traffic"
  vpc_id = "vpc-26165041"	

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "spark" {
  ami = "ami-6e1a0117"
  instance_type = "${var.instance_type}"
  key_name = "spark_key"
  security_groups = ["${aws_security_group.allow_all_tcp.name}"]

  connection {
        user = "ubuntu"
        private_key = "${file("~/.ssh/spark_key.pem")}"
  }

  tags {
    Name = "Master"
  }

  provisioner "file" {
    source      = "setup_spark.sh"
    destination = "/home/ubuntu/setup_spark.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /home/ubuntu/setup_spark.sh",
      "/home/ubuntu/setup_spark.sh"
    ]
  }

  provisioner "file" {
    source = "id_rsa"
    destination = "/home/ubuntu/.ssh/id_rsa"
  }
  
  provisioner "file" {
    source = "id_rsa.pub"
    destination = "/home/ubuntu/.ssh/id_rsa.pub"
  }

  provisioner "remote-exec" {
    inline = [ 
      "chmod 600 /home/ubuntu/.ssh/id_rsa",
      "chmod 600 /home/ubuntu/.ssh/id_rsa.pub" 
    ]
  }
}
