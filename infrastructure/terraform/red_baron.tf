# 🔴💀 ARSENAL PRO-LEVEL IAAS (Zero-Trust Edition)

variable "project" { default = "arsenal" }

# ── NETWORK ───────────────────────────────────────────────────────────────────

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags                 = { Name = "${var.project}-vpc" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags                    = { Name = "${var.project}-public-subnet" }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project}-igw" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# ── SECURITY ──────────────────────────────────────────────────────────────────

resource "aws_security_group" "c2_sg" {
  name        = "${var.project}-c2-sg"
  description = "Allow C2 traffic with strict IP filtering"
  vpc_id      = aws_vpc.main.id

  # SSH Restricted to RIck's IP (Placeholder for dynamic update)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # TODO: Restrict to RJ Business Solutions range
  }

  # C2 Callbacks
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ── COMPUTE ───────────────────────────────────────────────────────────────────

resource "aws_instance" "c2_master" {
  ami                    = "ami-0c55b159cbfafe1f0" # Debian 12
  instance_type          = "t3.medium"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.c2_sg.id]
  
  tags = { Name = "${var.project}-c2-master" }

  user_data = <<-EOF
              #!/bin/bash
              apt-get update && apt-get install -y docker.io curl
              curl https://sliver.sh/install | sudo bash
              EOF
}

output "c2_ip" {
  value = aws_instance.c2_master.public_ip
}
