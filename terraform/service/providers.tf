provider "aws" {
  region                      = var.integration_test_deployment ? "us-west-2" : "eu-west-1"
  access_key                  = var.integration_test_deployment ? "fake-access-key-id" : ""
  secret_key                  = var.integration_test_deployment ? "fake-secret-key" : ""
  s3_force_path_style         = var.integration_test_deployment ? true : false
  skip_credentials_validation = var.integration_test_deployment ? true : false
  skip_metadata_api_check     = var.integration_test_deployment ? true : false
  skip_requesting_account_id  = var.integration_test_deployment ? true : false

  endpoints {
    lambda         = var.integration_test_deployment ? "http://${var.localstack_domain}:4566" : ""
    s3             = var.integration_test_deployment ? "http://${var.localstack_domain}:4566" : ""    
  }