# Scripts

This directory contains utility scripts for development, deployment, and maintenance of Vuhitra CLI.

## Available Scripts

The following scripts will be added during implementation:

### Development Scripts

- **`setup.sh`**: Initial project setup and dependency installation
- **`dev.sh`**: Start development environment with hot reload
- **`clean.sh`**: Clean up build artifacts, caches, and temporary files

### Build Scripts

- **`build.sh`**: Build all Docker images with BuildKit optimization
- **`build-cli.sh`**: Build only the CLI service
- **`build-sandbox.sh`**: Build only the sandbox service

### Testing Scripts

- **`test.sh`**: Run all tests with coverage
- **`test-unit.sh`**: Run unit tests only
- **`test-integration.sh`**: Run integration tests only
- **`test-e2e.sh`**: Run end-to-end tests only

### Deployment Scripts

- **`deploy.sh`**: Deploy services to production
- **`pull-images.sh`**: Pull required Docker images
- **`push-images.sh`**: Push built images to registry

### Maintenance Scripts

- **`backup.sh`**: Backup data from Redis and Elasticsearch
- **`restore.sh`**: Restore data from backups
- **`cleanup-volumes.sh`**: Clean up unused Docker volumes
- **`health-check.sh`**: Check health of all services

### Validation Scripts

- **`validate-config.sh`**: Validate configuration files
- **`lint.sh`**: Run linters on Python code
- **`security-scan.sh`**: Run security scans on containers

## Usage

All scripts should be executable:
```bash
chmod +x scripts/*.sh
```

Run scripts from the project root:
```bash
./scripts/setup.sh
./scripts/build.sh
./scripts/test.sh
```

## Script Conventions

When creating new scripts:

1. **Add shebang**: Start with `#!/bin/bash`
2. **Set options**: Use `set -euo pipefail` for safety
3. **Add description**: Comment at the top explaining purpose
4. **Add usage**: Include usage information
5. **Error handling**: Proper error messages and exit codes
6. **Logging**: Clear output messages
7. **Make executable**: `chmod +x script.sh`

## Example Script Template

```bash
#!/bin/bash
# Script Name: example.sh
# Description: Brief description of what the script does
# Usage: ./scripts/example.sh [options]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script logic here
echo -e "${GREEN}Success!${NC}"
```

## Contributing

When adding new scripts:
- Follow the conventions above
- Test thoroughly
- Update this README
- Add appropriate error handling
- Document any dependencies
