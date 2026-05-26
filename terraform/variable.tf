variable "aws_region" {
  default = "us-east-1"
}

variable "k3s_instance_type" {
  default = "t3.large"
}

variable "jenkins_instance_type" {
  default = "t3.large"
}

variable "monitoring_instance_type" {
  default = "t3.medium"
}

variable "key_name" {
  description = "EC2 Key Pair"
}