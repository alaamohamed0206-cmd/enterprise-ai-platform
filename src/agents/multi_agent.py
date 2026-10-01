import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentRole(Enum):
    ANALYZER = "analyzer"
    PLANNER = "planner"
    EXECUTOR = "executor"
    VALIDATOR = "validator"
    OPTIMIZER = "optimizer"

@dataclass
class AgentTask:
    id: str
    role: AgentRole
    description: str
    input_data: Dict
    status: str = "pending"
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: datetime = None
    completed_at: Optional[datetime] = None

class EnterpriseAgent:
    def __init__(
        self,
        agent_id: str,
        role: AgentRole,
        model,
        tools: Optional[List] = None
    ):
        self.agent_id = agent_id
        self.role = role
        self.model = model
        self.tools = tools or []
        self.task_history = []
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "avg_response_time": 0,
            "success_rate": 0
        }
    
    async def execute_task(self, task: AgentTask) -> AgentTask:
        logger.info(f"Agent {self.agent_id} executing task {task.id}")
        
        task.status = "running"
        start_time = datetime.now()
        
        try:
            prompt = self._build_prompt(task)
            response = self.model.generate(prompt, max_length=256)
            
            task.result = {
                "response": response,
                "role": self.role.value,
                "agent_id": self.agent_id
            }
            
            task.status = "completed"
            self.performance_metrics["tasks_completed"] += 1
            
        except Exception as e:
            logger.error(f"Task {task.id} failed: {str(e)}")
            task.status = "failed"
            task.error = str(e)
            self.performance_metrics["tasks_failed"] += 1
        
        finally:
            task.completed_at = datetime.now()
            duration = (task.completed_at - start_time).total_seconds()
            self.task_history.append(task)
            self._update_metrics(duration)
        
        return task
    
    def _build_prompt(self, task: AgentTask) -> str:
        return f"Role: {self.role.value}\nTask: {task.description}\nInput: {str(task.input_data)[:100]}"
    
    def _update_metrics(self, response_time: float):
        total_tasks = (
            self.performance_metrics["tasks_completed"] +
            self.performance_metrics["tasks_failed"]
        )
        
        if total_tasks > 0:
            self.performance_metrics["success_rate"] = (
                self.performance_metrics["tasks_completed"] / total_tasks * 100
            )
            self.performance_metrics["avg_response_time"] = response_time
    
    def get_metrics(self) -> Dict:
        return self.performance_metrics

class MultiAgentOrchestrator:
    def __init__(self, model):
        self.model = model
        self.agents: Dict[str, EnterpriseAgent] = {}
        self.completed_tasks: List[AgentTask] = []
    
    def register_agent(self, agent: EnterpriseAgent):
        self.agents[agent.agent_id] = agent
        logger.info(f"Agent {agent.agent_id} registered")
    
    async def orchestrate(self, initial_task: AgentTask) -> Dict:
        logger.info(f"Starting orchestration for task {initial_task.id}")
        
        task_chain = [initial_task]
        current_task = initial_task
        
        while current_task:
            assigned_agent = self._assign_agent(current_task)
            
            if not assigned_agent:
                logger.error(f"No suitable agent for task {current_task.id}")
                break
            
            completed_task = await assigned_agent.execute_task(current_task)
            self.completed_tasks.append(completed_task)
            
            current_task = self._determine_next_task(completed_task)
            
            if current_task:
                task_chain.append(current_task)
        
        return self._generate_report(task_chain)
    
    def _assign_agent(self, task: AgentTask) -> Optional[EnterpriseAgent]:
        for agent in self.agents.values():
            if agent.role == task.role:
                return agent
        return None
    
    def _determine_next_task(self, completed_task: AgentTask) -> Optional[AgentTask]:
        role_sequence = [
            AgentRole.ANALYZER,
            AgentRole.PLANNER,
            AgentRole.EXECUTOR,
            AgentRole.VALIDATOR,
            AgentRole.OPTIMIZER
        ]
        
        try:
            current_index = role_sequence.index(completed_task.role)
            
            if current_index < len(role_sequence) - 1:
                next_role = role_sequence[current_index + 1]
                return AgentTask(
                    id=f"{completed_task.id}_next",
                    role=next_role,
                    description=completed_task.description,
                    input_data=completed_task.result or {}
                )
        except ValueError:
            pass
        
        return None
    
    def _generate_report(self, task_chain: List[AgentTask]) -> Dict:
        return {
            "total_tasks": len(task_chain),
            "completed_tasks": len([t for t in task_chain if t.status == "completed"]),
            "failed_tasks": len([t for t in task_chain if t.status == "failed"]),
            "agent_metrics": {
                agent_id: agent.get_metrics()
                for agent_id, agent in self.agents.items()
            }
        }
