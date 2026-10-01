"""
Project Architect - Designs project architecture and structure
"""
from typing import List, Dict
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ArchitectureLayer:
    name: str
    components: List[str]
    technologies: List[str]
    responsibilities: List[str]

@dataclass
class ProjectArchitecture:
    project_name: str
    frontend_layer: ArchitectureLayer
    backend_layer: ArchitectureLayer
    database_layer: ArchitectureLayer
    infrastructure_layer: ArchitectureLayer
    file_structure: Dict[str, List[str]]
    design_patterns: List[str]
    security_measures: List[str]

class ProjectArchitect:
    def __init__(self):
        self.design_patterns = {
            "mvc": "Model-View-Controller",
            "mvvm": "Model-View-ViewModel",
            "clean": "Clean Architecture",
            "microservices": "Microservices",
            "monolithic": "Monolithic",
        }
        logger.info("ProjectArchitect initialized")

    def design_architecture(self, spec) -> ProjectArchitecture:
        """Design complete project architecture based on specifications"""
        logger.info(f"Designing architecture for {spec.name}")
        
        frontend_layer = self._design_frontend_layer(spec)
        backend_layer = self._design_backend_layer(spec)
        database_layer = self._design_database_layer(spec)
        infrastructure_layer = self._design_infrastructure_layer(spec)
        
        file_structure = self._generate_file_structure(spec)
        design_patterns = self._select_design_patterns(spec)
        security_measures = self._define_security_measures(spec)
        
        architecture = ProjectArchitecture(
            project_name=spec.name,
            frontend_layer=frontend_layer,
            backend_layer=backend_layer,
            database_layer=database_layer,
            infrastructure_layer=infrastructure_layer,
            file_structure=file_structure,
            design_patterns=design_patterns,
            security_measures=security_measures
        )
        
        return architecture

    def _design_frontend_layer(self, spec) -> ArchitectureLayer:
        """Design frontend architecture"""
        if "React" in spec.frontend_tech:
            components = [
                "Pages/Screens",
                "Components",
                "Hooks",
                "Context/Redux",
                "Services",
                "Utils",
                "Styles"
            ]
            technologies = ["React", "Axios", "React Router", "Tailwind CSS"]
        elif "Vue" in spec.frontend_tech:
            components = [
                "Views",
                "Components",
                "Composables",
                "Store",
                "Services",
                "Utils"
            ]
            technologies = ["Vue.js", "Axios", "Vue Router", "Pinia"]
        else:
            components = ["Pages", "Components", "Services"]
            technologies = [spec.frontend_tech]
        
        return ArchitectureLayer(
            name="Frontend",
            components=components,
            technologies=technologies,
            responsibilities=[
                "User Interface",
                "User Experience",
                "Client-side Logic",
                "State Management",
                "API Communication"
            ]
        )

    def _design_backend_layer(self, spec) -> ArchitectureLayer:
        """Design backend architecture"""
        components = [
            "API Routes",
            "Controllers",
            "Services",
            "Models",
            "Middleware",
            "Utils",
            "Error Handling"
        ]
        
        technologies = [
            spec.backend_tech,
            "SQLAlchemy",
            "Pydantic",
            "JWT Auth",
            "Logging"
        ]
        
        return ArchitectureLayer(
            name="Backend",
            components=components,
            technologies=technologies,
            responsibilities=[
                "Business Logic",
                "API Endpoints",
                "Data Processing",
                "Authentication",
                "Authorization",
                "Error Handling",
                "Logging"
            ]
        )

    def _design_database_layer(self, spec) -> ArchitectureLayer:
        """Design database architecture"""
        db_tech = spec.database.split("+")[0]
        
        components = [
            "Tables/Collections",
            "Indexes",
            "Relationships",
            "Migrations",
            "Seed Data"
        ]
        
        technologies = [db_tech, "Alembic", "Query Optimization"]
        
        return ArchitectureLayer(
            name="Database",
            components=components,
            technologies=technologies,
            responsibilities=[
                "Data Storage",
                "Data Integrity",
                "Query Performance",
                "Backup & Recovery",
                "Indexing"
            ]
        )

    def _design_infrastructure_layer(self, spec) -> ArchitectureLayer:
        """Design infrastructure architecture"""
        components = [
            "Docker Configuration",
            "CI/CD Pipeline",
            "Monitoring",
            "Logging",
            "Load Balancing"
        ]
        
        technologies = [
            "Docker",
            "Docker Compose",
            "GitHub Actions",
            "AWS",
            "Nginx"
        ]
        
        return ArchitectureLayer(
            name="Infrastructure",
            components=components,
            technologies=technologies,
            responsibilities=[
                "Deployment",
                "Scaling",
                "Monitoring",
                "Security",
                "Performance"
            ]
        )

    def _generate_file_structure(self, spec) -> Dict[str, List[str]]:
        """Generate recommended file structure"""
        return {
            "frontend": [
                "src/pages",
                "src/components",
                "src/hooks",
                "src/services",
                "src/utils",
                "src/styles",
                "src/assets",
                "public"
            ],
            "backend": [
                "app/api/routes",
                "app/core",
                "app/models",
                "app/schemas",
                "app/services",
                "app/utils",
                "tests",
                "migrations"
            ],
            "config": [
                ".env",
                ".env.example",
                "docker-compose.yml",
                "Dockerfile",
                ".dockerignore",
                ".gitignore"
            ],
            "docs": [
                "README.md",
                "ARCHITECTURE.md",
                "API.md",
                "DEPLOYMENT.md"
            ]
        }

    def _select_design_patterns(self, spec) -> List[str]:
        """Select appropriate design patterns"""
        patterns = [
            "Repository Pattern",
            "Service Layer Pattern",
            "Dependency Injection",
            "Factory Pattern",
            "Observer Pattern"
        ]
        
        if "complex" in spec.estimated_complexity:
            patterns.extend([
                "Strategy Pattern",
                "Decorator Pattern",
                "Chain of Responsibility"
            ])
        
        return patterns

    def _define_security_measures(self, spec) -> List[str]:
        """Define security measures"""
        measures = [
            "JWT Authentication",
            "Input Validation",
            "SQL Injection Prevention",
            "XSS Protection",
            "CORS Configuration",
            "Rate Limiting",
            "Environment Variables",
            "HTTPS/TLS",
            "Password Hashing",
            "Audit Logging"
        ]
        
        return measures

    def visualize_architecture(self, architecture: ProjectArchitecture) -> str:
        """Generate ASCII visualization of architecture"""
        viz = f"""
╔════════════════════════════════════════════════════════════════╗
║                {architecture.project_name.upper()} ARCHITECTURE                      ║
╚════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND LAYER                                                  │
│ {', '.join(architecture.frontend_layer.technologies)}
├─────────────────────────────────────────────────────────────────┤
│ Components: {', '.join(architecture.frontend_layer.components[:3])}...
└─────────────────────────────────────────────────────────────────┘
                          ↓↑
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND LAYER                                                   │
│ {', '.join(architecture.backend_layer.technologies)}
├─────────────────────────────────────────────────────────────────┤
│ Components: {', '.join(architecture.backend_layer.components[:3])}...
└─────────────────────────────────────────────────────────────────┘
                          ↓↑
┌─────────────────────────────────────────────────────────────────┐
│ DATABASE LAYER                                                  │
│ {', '.join(architecture.database_layer.technologies)}
├─────────────────────────────────────────────────────────────────┤
│ Components: {', '.join(architecture.database_layer.components[:3])}...
└─────────────────────────────────────────────────────────────────┘

SECURITY MEASURES:
{chr(10).join('  • ' + m for m in architecture.security_measures[:5])}
  
DESIGN PATTERNS:
{chr(10).join('  • ' + p for p in architecture.design_patterns[:5])}
        """
        return viz
