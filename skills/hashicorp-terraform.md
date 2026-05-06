---
name: hashicorp-terraform
description: Terraform best practices — module structure, state management, provider patterns, and security hardening.
kind: skill
---

# HashiCorp Terraform Skills

Best practices for writing, reviewing, and maintaining Terraform infrastructure code. Based on HashiCorp's official agent skills.

## File Organization

Standard module structure:

```
module/
├── main.tf          # Core resource definitions
├── variables.tf     # Input variable declarations
├── outputs.tf       # Output value declarations
├── providers.tf     # Provider configuration (root modules only)
├── versions.tf      # Required providers and Terraform version
└── README.md        # Module documentation
```

Rules:
- One resource type per file in large modules (e.g., `security_groups.tf`, `iam.tf`)
- No resource definitions in `variables.tf` or `outputs.tf`
- `terraform.tfvars` only for non-sensitive defaults. Never commit secrets.
- Use `locals.tf` for computed values used across multiple resources.

## Formatting

- 2-space indentation (enforced by `terraform fmt`)
- Align `=` signs within argument blocks when they improve readability
- Blank line between resource argument blocks
- `terraform fmt -recursive` before every commit

```hcl
resource "aws_s3_bucket" "data" {
  bucket = var.bucket_name
  tags   = local.common_tags
}
```

## Naming Conventions

- Resource names: `snake_case`, descriptive, no abbreviations unless standard (`vpc`, `iam`, `sg`)
- Variables: `snake_case`, noun phrases (`instance_type`, `enable_deletion_protection`)
- Outputs: `snake_case`, prefixed by resource name (`bucket_arn`, `vpc_id`)
- Module names: kebab-case matching the directory name

## Variables

```hcl
variable "instance_type" {
  description = "EC2 instance type for the web tier"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Must be a supported instance type: t3.micro, t3.small, t3.medium"
  }
}
```

Rules:
- Every variable must have a `description`
- Sensitive variables: `sensitive = true` to suppress in plan output
- Use `validation` blocks for allowlist checks
- No default values for required inputs (forces explicit configuration)

## Outputs

```hcl
output "bucket_arn" {
  description = "ARN of the S3 data bucket"
  value       = aws_s3_bucket.data.arn
  sensitive   = false
}
```

- Every output must have a `description`
- Mark outputs as `sensitive = true` if they contain secrets
- Only export what callers actually need

## State Management

- Remote state required for any team environment (S3+DynamoDB, Terraform Cloud)
- State locking mandatory — prevent concurrent runs
- Never edit state manually. Use `terraform state mv`, `terraform import`, `terraform state rm`
- Separate state per environment (dev/staging/prod) via workspaces or separate backends
- Back up state before destructive operations

## Provider Patterns

```hcl
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

- Pin provider versions with `~>` (minor version flexibility, no major bumps)
- Never use unpinned `version = "*"`
- Run `terraform init -upgrade` intentionally, not as part of routine CI

## Security Hardening

- No secrets in `.tf` files or `tfvars` committed to git. Use `var.secret` + secret manager at runtime.
- Enable `prevent_destroy = true` on stateful resources (databases, S3 buckets)
- Encryption at rest required for all storage resources
- S3 buckets: block public access by default, enable versioning for state buckets
- IAM: least privilege. No `*` actions or `*` resources without justification
- Security groups: no `0.0.0.0/0` ingress except port 443; document exceptions

## Testing

Use `terraform test` for module testing:

```hcl
# tests/basic.tftest.hcl
run "creates_bucket" {
  command = plan

  assert {
    condition     = aws_s3_bucket.data.bucket == "my-test-bucket"
    error_message = "Bucket name did not match expected value"
  }
}
```

- Write tests for new modules before merging
- Test with `terraform plan` in CI for all PRs (no apply in CI for production)
- Use mock providers in tests to avoid cloud costs and credentials in CI

## Review Checklist

Before merging a Terraform PR:

- [ ] `terraform fmt -recursive` clean
- [ ] `terraform validate` passes
- [ ] `terraform plan` output reviewed and attached to PR
- [ ] No `prevent_destroy = false` removed without explicit justification
- [ ] No secrets in `.tf` files or committed `tfvars`
- [ ] State backend configured for remote + locking
- [ ] New resources have encryption, logging, and tagging as required
- [ ] Destructive changes (replacements, deletions) explicitly acknowledged in PR

*Source: github.com/hashicorp/agent-skills*
