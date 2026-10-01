import asyncio
from src.models.language_model import EnterpriseLanguageModel
from src.agents.multi_agent import MultiAgentOrchestrator, EnterpriseAgent, AgentRole, AgentTask
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Initializing Enterprise AI System")
    
    model = EnterpriseLanguageModel(
        model_name="gpt2",
        device="cpu"
    )
    
    orchestrator = MultiAgentOrchestrator(model)
    
    analyzer = EnterpriseAgent(
        agent_id="analyzer_1",
        role=AgentRole.ANALYZER,
        model=model
    )
    
    planner = EnterpriseAgent(
        agent_id="planner_1",
        role=AgentRole.PLANNER,
        model=model
    )
    
    orchestrator.register_agent(analyzer)
    orchestrator.register_agent(planner)
    
    task = AgentTask(
        id="task_001",
        role=AgentRole.ANALYZER,
        description="Analyze user requirements",
        input_data={"user_input": "Build an e-commerce platform"}
    )
    
    result = await orchestrator.orchestrate(task)
    
    print("\n=== Orchestration Results ===")
    print(f"Total Tasks: {result['total_tasks']}")
    print(f"Completed: {result['completed_tasks']}")
    print(f"Failed: {result['failed_tasks']}")
    print(f"Agent Metrics: {result['agent_metrics']}")

if __name__ == "__main__":
    asyncio.run(main())
