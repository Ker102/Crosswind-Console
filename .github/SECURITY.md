# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < 1.0   | :white_check_mark: |

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities to the repository maintainers. You will receive a response within 48 hours. If the issue is confirmed, we will release a patch as soon as possible depending on complexity.

### What to include in a report:
- Type of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Security Measures

This repository implements the following security measures:

### Automated Security Scanning
- **CodeQL Analysis**: Automated code scanning for JavaScript/TypeScript and Python vulnerabilities
- **Dependency Review**: Automatic scanning of dependencies for known vulnerabilities
- **Dependabot**: Automated dependency updates with security patches

### Security Labels
Pull requests related to security are labeled with the `security` label for easy tracking and prioritization.

### Auto-merge Policy
- Dependabot PRs for patch and minor updates are automatically merged after passing all checks
- PRs with the `auto-merge` label are merged automatically after all required checks pass
- Major version updates require manual review

## Security Best Practices

When contributing to this project, please follow these security best practices:

1. **Never commit secrets** - Use environment variables and `.env` files
2. **Validate all inputs** - Sanitize and validate user inputs
3. **Keep dependencies updated** - Regularly update dependencies to patch vulnerabilities
4. **Follow the principle of least privilege** - Request only necessary permissions
5. **Use secure communications** - Always use HTTPS for API calls
