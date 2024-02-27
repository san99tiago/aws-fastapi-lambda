terraform {
  backend "s3" {
    bucket = "san99tiago-terraform-backend-dev" # Update to another backend as needed
    key    = "terraform.fastapi.json"
    region = "us-east-1"
  }
}
