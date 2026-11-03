provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Project   = "terraform-aws-lab"
      ManagedBy = "terraform"
      Owner     = "ibrahim"
    }
  }
}
