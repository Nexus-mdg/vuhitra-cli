# Step 1: Project Structure Setup

## Objective
Create the foundational directory structure and configuration files for the Vuhitra CLI project.

## Context
This is the first step in building Vuhitra CLI, a Docker-based AI-powered command-line interface. We need to establish a clean, organized project structure that will support all future development.

## Requirements

### Directory Structure
Create the following directory structure:
```
vuhitra-cli/
├── cli/                    # CLI application code
│   ├── src/               # Source code
│   │   └── cli/          # Main package
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile        # CLI service Dockerfile
├── docker/                # Docker-related files
│   ├── sandbox/          # Sandbox service files
│   │   └── Dockerfile
│   └── configs/          # Service configurations
├── config/                # Configuration files
│   ├── .env.template     # Environment template
│   └── redis.conf        # Redis configuration (if needed)
├── docs/                  # Documentation
│   ├── architecture/
│   ├── user-guide/
│   └── examples/
├── tests/                 # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── examples/              # Example workflows
├── prompts/               # Implementation prompt files
├── scripts/               # Utility scripts
├── docker-compose.yml     # Main orchestration file
├── .gitignore            # Git ignore file
├── .dockerignore         # Docker ignore file
├── README.md             # Project README
├── TODO.md               # Project TODO/ToR
├── IMPLEMENTATION.md     # Implementation guide
├── LICENSE               # MIT License (already exists)
└── CHANGELOG.md          # Version changelog
```

### .gitignore Content
Create a comprehensive .gitignore file that excludes:
- Python artifacts (__pycache__, *.pyc, .pytest_cache)
- Virtual environments (venv/, env/, .venv/)
- IDE files (.vscode/, .idea/, *.swp)
- Environment files (.env, .env.local, but not .env.template)
- Docker volumes and temporary files
- Build artifacts (dist/, build/, *.egg-info)
- OS files (.DS_Store, Thumbs.db)
- Logs (*.log)
- Temporary files (/tmp/*, *.tmp)

### .dockerignore Content
Create .dockerignore for CLI service:
- .git/
- .gitignore
- README.md
- docs/
- tests/
- examples/
- **/__pycache__
- **/*.pyc
- .env
- .vscode/
- .idea/

### README.md
Create a basic README.md with:
- Project title and description
- Key features list
- Prerequisites (Docker, Docker Compose)
- Quick start instructions (placeholder)
- Link to full documentation
- License information
- Contributing guidelines (placeholder)

### CHANGELOG.md
Initialize with:
- Version 0.1.0 (Unreleased) section
- Template for version entries

## Tasks

1. **Create all directories**
   - Use `mkdir -p` to create nested directories
   - Ensure proper permissions

2. **Create .gitignore**
   - Include all necessary patterns
   - Add comments for clarity

3. **Create .dockerignore**
   - Focus on reducing build context
   - Exclude development files

4. **Create README.md**
   - Provide clear project overview
   - Include badges (optional: build status, version, license)
   - Add architecture diagram placeholder

5. **Create CHANGELOG.md**
   - Use Keep a Changelog format
   - Initialize with v0.1.0 (Unreleased)

6. **Create placeholder files**
   - Empty __init__.py files in Python packages
   - Placeholder Dockerfiles with TODOs
   - Basic requirements.txt with TODO comments

## Expected Output

After completion:
- All directories exist
- .gitignore properly excludes build artifacts
- .dockerignore optimizes build context
- README provides clear project overview
- Project structure is ready for development

## Validation Steps

1. Verify directory structure:
   ```bash
   tree -L 3 -a vuhitra-cli/
   ```

2. Check .gitignore:
   ```bash
   # Create a test Python cache file
   touch cli/src/__pycache__/test.pyc
   git status  # Should not show the .pyc file
   ```

3. Ensure README is clear and informative

## Next Step
Proceed to Step 2: Docker Compose Foundation
