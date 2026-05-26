output "k3s_elastic_ip" {
  value = aws_eip.k3s_eip.public_ip
}

output "jenkins_server_ip" {
  value = aws_instance.jenkins_server.public_ip
}

output "monitoring_server_ip" {
  value = aws_instance.monitoring_server.public_ip
}