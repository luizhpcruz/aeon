#!/usr/bin/env python3
"""
AEON Ecosystem Generator
Creates separate project structure for AEON ecosystem
"""
import os
import json
from pathlib import Path

# Project definitions
PROJECTS = {
    "aeon-entropy": {
        "description": "Entropy and Complexity Simulator",
        "tech": ["python", "numpy", "matplotlib", "scipy"],
        "main_module": "entropy_core",
        "port": 8001
    },
    "aeon-cosmology": {
        "description": "Cosmological Engine", 
        "tech": ["python", "astropy", "numpy", "matplotlib"],
        "main_module": "cosmology_core",
        "port": 8002
    },
    "aeon-verna": {
        "description": "Symbolic Emergence System",
        "tech": ["python", "networkx", "numpy", "sympy"],
        "main_module": "verna_core", 
        "port": 8003
    },
    "aeon-cosma": {
        "description": "Intelligent Cosmological Engine",
        "tech": ["python", "tensorflow", "numpy", "scikit-learn"],
        "main_module": "cosma_core",
        "port": 8004
    },
    "aeon-network": {
        "description": "P2P System and Coordination",
        "tech": ["python", "websockets", "asyncio", "pydantic"],
        "main_module": "network_core",
        "port": 8005
    },
    "aeon-coordinator": {
        "description": "Central Orchestrator",
        "tech": ["python", "fastapi", "asyncio", "redis"],
        "main_module": "coordinator_core",
        "port": 8006
    },
    "aeon-api": {
        "description": "REST API and Interfaces",
        "tech": ["fastapi", "pydantic", "uvicorn", "sqlalchemy"],
        "main_module": "api_core",
        "port": 8007
    },
    "aeon-dashboard": {
        "description": "Web Interface and Visualization",
        "tech": ["streamlit", "plotly", "pandas", "websockets"],
        "main_module": "dashboard_core",
        "port": 8008
    },
    "aeon-data": {
        "description": "Persistence and Analytics",
        "tech": ["postgresql", "influxdb", "pandas", "sqlalchemy"],
        "main_module": "data_core",
        "port": 8009
    },
    "aeon-deploy": {
        "description": "Deployment and Infrastructure",
        "tech": ["docker", "kubernetes", "terraform", "ansible"],
        "main_module": "deploy_core",
        "port": 8010
    }
}

def create_project_structure(project_name: str, config: dict, base_path: Path):
    """Creates directory structure for a project"""
    project_path = base_path / project_name
    
    # Main directories
    dirs = [
        "src",
        f"src/{config['main_module']}",
        "tests",
        "docs", 
        "scripts",
        "configs",
        "data",
        "logs"
    ]
    
    for dir_name in dirs:
        (project_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    # Configuration files
    create_requirements_txt(project_path, config['tech'])
    create_dockerfile(project_path, project_name)
    create_readme(project_path, project_name, config)
    create_main_module(project_path, config)
    create_pyproject_toml(project_path, project_name, config)
    
    print(f"✅ {project_name} created at {project_path}")

def create_requirements_txt(project_path: Path, tech_stack: list):
    """Creates requirements.txt based on tech stack"""
    requirements = []
    
    # Technology mapping to pip packages
    tech_mapping = {
        "python": [],  # base
        "numpy": ["numpy>=1.24.0"],
        "matplotlib": ["matplotlib>=3.6.0"],
        "scipy": ["scipy>=1.10.0"],
        "astropy": ["astropy>=5.2.0"],
        "networkx": ["networkx>=3.0.0"],
        "sympy": ["sympy>=1.11.0"],
        "tensorflow": ["tensorflow>=2.12.0"],
        "scikit-learn": ["scikit-learn>=1.2.0"],
        "websockets": ["websockets>=11.0.0"],
        "asyncio": [],  # built-in
        "pydantic": ["pydantic>=2.0.0"],
        "fastapi": ["fastapi>=0.100.0"],
        "uvicorn": ["uvicorn[standard]>=0.22.0"],
        "sqlalchemy": ["sqlalchemy>=2.0.0"],
        "redis": ["redis>=4.5.0"],
        "streamlit": ["streamlit>=1.25.0"],
        "plotly": ["plotly>=5.15.0"],
        "pandas": ["pandas>=2.0.0"],
        "postgresql": ["psycopg2-binary>=2.9.0"],
        "influxdb": ["influxdb-client>=1.36.0"],
        "docker": ["docker>=6.1.0"],
        "kubernetes": ["kubernetes>=26.1.0"],
        "terraform": [],  # external tool
        "ansible": ["ansible>=8.0.0"]
    }
    
    for tech in tech_stack:
        requirements.extend(tech_mapping.get(tech, []))
    
    # Add common dependencies
    requirements.extend([
        "python-dotenv>=1.0.0",
        "loguru>=0.7.0",
        "typer>=0.9.0"
    ])
    
    content = "\n".join(sorted(set(requirements)))
    (project_path / "requirements.txt").write_text(content, encoding="utf-8")

def create_dockerfile(project_path: Path, project_name: str):
    """Creates basic Dockerfile"""
    content = f"""FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY configs/ ./configs/

# Environment variables
ENV PYTHONPATH=/app/src
ENV {project_name.upper().replace('-', '_')}_ENV=production

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "-m", "src.main"]
"""
    (project_path / "Dockerfile").write_text(content, encoding="utf-8")

def create_readme(project_path: Path, project_name: str, config: dict):
    """Creates README.md"""
    content = f"""# {project_name}

{config['description']}

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python -m src.{config['main_module']}
```

## Docker

```bash
# Build
docker build -t {project_name} .

# Run
docker run -p {config['port']}:{config['port']} {project_name}
```

## Tests

```bash
pytest tests/
```

## Documentation

See `docs/` for detailed documentation.

## Technologies

- {', '.join(config['tech'])}

## Contributing

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
"""
    (project_path / "README.md").write_text(content, encoding="utf-8")

def create_main_module(project_path: Path, config: dict):
    """Creates main module"""
    main_path = project_path / "src" / config['main_module']
    
    # __init__.py
    (main_path / "__init__.py").write_text('"""Main module"""\n', encoding="utf-8")
    
    # main.py
    main_content = f'''"""
{config['description']} - Main Module
"""
import asyncio
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class {config['main_module'].title().replace('_', '')}:
    """Main module class"""
    
    def __init__(self):
        self.config = self.load_config()
        self.is_running = False
    
    def load_config(self) -> dict:
        """Load configuration"""
        # TODO: Implement config loading
        return {{
            "name": "{config['main_module']}",
            "version": "1.0.0",
            "port": {config['port']}
        }}
    
    async def start(self):
        """Start the service"""
        logger.info(f"Starting {{self.config['name']}} v{{self.config['version']}}")
        self.is_running = True
        
        # TODO: Implement main logic
        while self.is_running:
            await self.process()
            await asyncio.sleep(1)
    
    async def process(self):
        """Main processing"""
        # TODO: Implement specific processing
        logger.debug("Processing...")
    
    async def stop(self):
        """Stop the service"""
        logger.info("Stopping service...")
        self.is_running = False

async def main():
    """Main function"""
    service = {config['main_module'].title().replace('_', '')}()
    try:
        await service.start()
    except KeyboardInterrupt:
        await service.stop()

if __name__ == "__main__":
    asyncio.run(main())
'''
    (main_path / "main.py").write_text(main_content, encoding="utf-8")

def create_pyproject_toml(project_path: Path, project_name: str, config: dict):
    """Creates pyproject.toml"""
    content = f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "1.0.0"
description = "{config['description']}"
authors = [{{name = "AEON Team", email = "team@aeon.dev"}}]
license = {{text = "MIT"}}
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.4.0"
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
target-version = ["py311"]
line-length = 88

[tool.isort]
profile = "black"
"""
    (project_path / "pyproject.toml").write_text(content, encoding="utf-8")

def generate_ecosystem():
    """Generate complete project ecosystem"""
    base_path = Path("../aeon-ecosystem")
    base_path.mkdir(exist_ok=True)
    
    print(f"Building AEON ecosystem at {base_path.absolute()}")
    print("=" * 60)
    
    for project_name, config in PROJECTS.items():
        create_project_structure(project_name, config, base_path)
    
    # Create main docker-compose.yml
    create_docker_compose(base_path)
    
    # Create setup script
    create_setup_script(base_path)
    
    print("=" * 60)
    print(f"✅ Ecosystem created with {len(PROJECTS)} projects!")
    print(f"📁 Location: {base_path.absolute()}")
    print(f"🚀 To start: cd {base_path.name} && ./setup.sh")

def create_docker_compose(base_path: Path):
    """Creates main docker-compose.yml"""
    services = {}
    
    for project_name, config in PROJECTS.items():
        services[project_name.replace('-', '_')] = {
            "build": f"./{project_name}",
            "ports": [f"{config['port']}:{config['port']}"],
            "environment": [
                f"{project_name.upper().replace('-', '_')}_ENV=development"
            ],
            "volumes": [
                f"./{project_name}/data:/app/data",
                f"./{project_name}/logs:/app/logs"
            ],
            "networks": ["aeon-network"]
        }
    
    compose_content = {
        "version": "3.8",
        "services": services,
        "networks": {
            "aeon-network": {
                "driver": "bridge"
            }
        }
    }
    
    # Use JSON format since yaml might not be available
    content = json.dumps(compose_content, indent=2)
    
    (base_path / "docker-compose.json").write_text(content, encoding="utf-8")

def create_setup_script(base_path: Path):
    """Creates main setup script"""
    content = """#!/bin/bash
# Setup script for AEON ecosystem

echo "Setting up AEON ecosystem..."

# Install dependencies in each project
for project in aeon-*; do
    if [ -d "$project" ]; then
        echo "Installing dependencies in $project..."
        cd "$project"
        pip install -r requirements.txt
        cd ..
    fi
done

echo "Setup complete!"
echo "For Docker: docker-compose up"
echo "For development: cd <project> && python -m src.main"
"""
    setup_path = base_path / "setup.sh"
    setup_path.write_text(content, encoding="utf-8")
    setup_path.chmod(0o755)  # Tornar executável

if __name__ == "__main__":
    generate_ecosystem()
