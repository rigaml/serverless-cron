terraform {
  backend "s3" {
    key            = "riga-cron/terraform.tfstate"
    region         = "us-east-1"
  }
}