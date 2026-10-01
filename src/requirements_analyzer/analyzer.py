"""
Requirements Analyzer - Understands client needs and generates project specifications
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Requirement:
    category: str
    description: str
    priority: str
    tech_suggestion: Optional[str] = None

@dataclass
class ProjectSpec:
    name: str
    description: str
    requirements: List[Requirement]
    frontend_tech: str
    backend_tech: str
    database: str
    deployment_platform: str
    estimated_complexity: str
    estimated_hours: int

class RequirementsAnalyzer:
    def __init__(self):
        self.tech_recommendations = {
            "real-time": ["WebSocket", "Socket.io"],
            "scalable": ["Microservices", "Docker", "Kubernetes"],
            "fast": ["FastAPI", "Node.js", "Go"],
            "secure": ["OAuth2", "JWT", "HTTPS"],
            "mobile": ["React Native", "Flutter"],
            "data": ["PostgreSQL", "MongoDB", "Redis"],
            "analytics": ["Elasticsearch", "Grafana"],
        }
        logger.info("RequirementsAnalyzer initialized")

    def analyze_client_input(self, client_input: str) -> Dict:
        """Parse client input and extract requirements"""
        logger.info(f"Analyzing client input...")
        
        analysis = {
            "raw_input": client_input,
            "extracted_keywords": self._extract_keywords(client_input),
            "project_type": self._identify_project_type(client_input),
            "features": self._extract_features(client_input),
            "non_functional_requirements": self._extract_non_functional(client_input),
            "estimated_scope": self._estimate_scope(client_input)
        }
        
        return analysis

    def generate_spec(self, analysis: Dict) -> ProjectSpec:
        """Generate complete project specification from analysis"""
        logger.info("Generating project specification")
        
        frontend_tech = self._recommend_frontend(analysis)
        backend_tech = self._recommend_backend(analysis)
        database = self._recommend_database(analysis)
        deployment = self._recommend_deployment(analysis)
        
        requirements = self._create_requirements_list(analysis)
        complexity = self._assess_complexity(analysis)
        hours = self._estimate_hours(complexity, len(requirements))
        
        spec = ProjectSpec(
            name=self._generate_project_name(analysis),
            description=analysis["raw_input"],
            requirements=requirements,
            frontend_tech=frontend_tech,
            backend_tech=backend_tech,
            database=database,
            deployment_platform=deployment,
            estimated_complexity=complexity,
            estimated_hours=hours
        )
        
        return spec

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from input"""
        keywords = []
        important_words = [
            "real-time", "mobile", "api", "database", "authentication",
            "payment", "analytics", "dashboard", "ecommerce", "social",
            "machine learning", "ai", "blockchain", "iot", "streaming"
        ]
        
        text_lower = text.lower()
        for word in important_words:
            if word in text_lower:
                keywords.append(word)
        
        return keywords

    def _identify_project_type(self, text: str) -> str:
        """Identify the type of project"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["mobile", "app", "ios", "android"]):
            return "mobile_app"
        elif any(word in text_lower for word in ["website", "web", "ecommerce", "blog"]):
            return "web_app"
        elif any(word in text_lower for word in ["api", "backend", "server"]):
            return "backend_service"
        elif any(word in text_lower for word in ["dashboard", "analytics", "data"]):
            return "data_platform"
        else:
            return "full_stack_app"

    def _extract_features(self, text: str) -> List[str]:
        """Extract main features from input"""
        features = []
        feature_keywords = {
            "user auth": ["login", "signup", "authentication", "oauth"],
            "payment": ["payment", "checkout", "stripe", "paypal"],
            "database": ["database", "storage", "data management"],
            "api": ["api", "rest", "graphql"],
            "realtime": ["realtime", "live", "socket"],
            "analytics": ["analytics", "dashboard", "reporting"],
            "notification": ["notification", "email", "sms"],
        }
        
        text_lower = text.lower()
        for feature, keywords in feature_keywords.items():
            if any(kw in text_lower for kw in keywords):
                features.append(feature)
        
        return features

    def _extract_non_functional(self, text: str) -> Dict:
        """Extract non-functional requirements"""
        text_lower = text.lower()
        
        return {
            "performance": "fast" in text_lower or "performance" in text_lower,
            "scalability": "scale" in text_lower or "scalable" in text_lower,
            "security": "secure" in text_lower or "security" in text_lower,
            "availability": "available" in text_lower or "uptime" in text_lower,
        }

    def _estimate_scope(self, text: str) -> str:
        """Estimate project scope"""
        word_count = len(text.split())
        
        if word_count < 50:
            return "small"
        elif word_count < 200:
            return "medium"
        else:
            return "large"

    def _recommend_frontend(self, analysis: Dict) -> str:
        """Recommend frontend technology"""
        keywords = analysis["extracted_keywords"]
        
        if "mobile" in keywords:
            return "React Native"
        elif "real-time" in keywords:
            return "React + Socket.io"
        elif "data" in keywords or "analytics" in keywords:
            return "Vue.js + D3.js"
        else:
            return "React + Tailwind CSS"

    def _recommend_backend(self, analysis: Dict) -> str:
        """Recommend backend technology"""
        keywords = analysis["extracted_keywords"]
        
        if "real-time" in keywords:
            return "FastAPI + WebSocket"
        elif "scalable" in keywords:
            return "FastAPI + Docker"
        else:
            return "FastAPI"

    def _recommend_database(self, analysis: Dict) -> str:
        """Recommend database"""
        keywords = analysis["extracted_keywords"]
        
        if "real-time" in keywords:
            return "PostgreSQL + Redis"
        elif "data" in keywords or "analytics" in keywords:
            return "PostgreSQL + Elasticsearch"
        else:
            return "PostgreSQL"

    def _recommend_deployment(self, analysis: Dict) -> str:
        """Recommend deployment platform"""
        return "Docker + AWS"

    def _create_requirements_list(self, analysis: Dict) -> List[Requirement]:
        """Create list of requirements"""
        requirements = []
        
        for feature in analysis["features"]:
            req = Requirement(
                category=feature,
                description=f"Implement {feature}",
                priority="high",
                tech_suggestion=self.tech_recommendations.get(feature, [None])[0]
            )
            requirements.append(req)
        
        return requirements

    def _assess_complexity(self, analysis: Dict) -> str:
        """Assess project complexity"""
        feature_count = len(analysis["features"])
        scope = analysis["estimated_scope"]
        
        if scope == "small" and feature_count <= 3:
            return "simple"
        elif scope == "medium" and feature_count <= 6:
            return "medium"
        else:
            return "complex"

    def _estimate_hours(self, complexity: str, feature_count: int) -> int:
        """Estimate project hours"""
        base_hours = {
            "simple": 20,
            "medium": 60,
            "complex": 150
        }
        
        return base_hours.get(complexity, 60) + (feature_count * 10)

    def _generate_project_name(self, analysis: Dict) -> str:
        """Generate project name from input"""
        words = analysis["raw_input"].split()[:3]
        return "_".join(words).lower().replace(" ", "_")
