# TFLint settings for the whole repo.
# Docs: https://github.com/terraform-linters/tflint/blob/master/docs/user-guide/config.md
config {
  # Also lint the local modules we call (modules/vpc, modules/ec2 ...)
  call_module_type = "local"
}

# Built-in Terraform language rules (unused variables, missing version pins, ...)
plugin "terraform" {
  enabled = true
  preset  = "recommended"
}

# The AWS rules plugin (invalid instance types, etc.) comes in 1.3 with the VPC module.
