terraform {
  backend "s3" {
    key            = "jg-fitness-admin/terraform.tfstate"
    region         = "eu-west-1"
  }
}