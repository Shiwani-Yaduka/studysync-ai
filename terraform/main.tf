resource "aws_instance" "k3s_server" {

  ami           = "ami-04b4f1a9cf54c11d0"
  instance_type = var.k3s_instance_type

  key_name = var.key_name

  vpc_security_group_ids = [
    aws_security_group.studysync_sg.id
  ]

  root_block_device {
    volume_size = 40
    volume_type = "gp3"
  }

  tags = {
    Name = "StudySync-k3s-Server"
  }
}

resource "aws_instance" "jenkins_server" {

  ami           = "ami-04b4f1a9cf54c11d0"
  instance_type = var.jenkins_instance_type

  key_name = var.key_name

  vpc_security_group_ids = [
    aws_security_group.studysync_sg.id
  ]

  root_block_device {
    volume_size = 60
    volume_type = "gp3"
  }

  tags = {
    Name = "StudySync-Jenkins-Server"
  }
}

resource "aws_instance" "monitoring_server" {

  ami           = "ami-04b4f1a9cf54c11d0"
  instance_type = var.monitoring_instance_type

  key_name = var.key_name

  vpc_security_group_ids = [
    aws_security_group.studysync_sg.id
  ]

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  tags = {
    Name = "StudySync-Monitoring-Server"
  }
}

resource "aws_eip" "k3s_eip" {

  instance = aws_instance.k3s_server.id

  domain = "vpc"

  tags = {
    Name = "StudySync-k3s-EIP"
  }
}