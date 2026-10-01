import asyncio
from src.models.language_model import EnterpriseLanguageModel
from src.agents.multi_agent import MultiAgentOrchestrator, EnterpriseAgent, AgentRole, AgentTask
from src.inference.rag_and_tools import EnterpriseRAG, EnterpriseTools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("=== Enterprise AI System - Full Integration ===")
    
    # Initialize RAG
    rag = EnterpriseRAG()
    documents = [
        "Python is a high-level programming language.",
        "Machine Learning is a subset of AI.",
        "FastAPI is a modern web framework.",
        "Docker containers package applications."
    ]
    rag.add_documents(documents)
    
    # Initialize Tools
    tools = EnterpriseTools()
    logger.info(f"Available tools: {tools.list_tools()}")
    
    # Initialize Model
    model = EnterpriseLanguageModel(model_name="gpt2", device="cpu")
    
    # Initialize Orchestrator
    orchestrator = MultiAgentOrchestrator(model)
    
    # Register Agents
    analyzer = EnterpriseAgent("analyzer_1", AgentRole.ANALYZER, model)
    planner = EnterpriseAgent("planner_1", AgentRole.PLANNER, model)
    executor = EnterpriseAgent("executor_1", AgentRole.EXECUTOR, model)
    
    orchestrator.register_agent(analyzer)
    orchestrator.register_agent(planner)
    orchestrator.register_agent(executor)
    
    # Test RAG
    print("\n=== RAG System Test ===")
    query = "What is machine learning?"
    context = rag.get_context(query, top_k=2)
    print(context)
    
    # Test Tools
    print("\n=== Tools System Test ===")
    result = tools.call_tool("calculate", expression="2+2*10")
    print(f"Calculate: {result}")
    
    result = tools.call_tool("summarize", text="This is a very long text that needs to be summarized into a shorter version for better understanding and faster reading.")
    print(f"Summarize: {result}")
    
    # Execute Task with RAG Context
    print("\n=== Task Orchestration with RAG Context ===")
    task = AgentTask(
        id="task_integrated",
        role=AgentRole.ANALYZER,
        description="Analyze requirements with context",
        input_data={
            "user_query": "What technologies should I use?",
            "context": context,
            "available_tools": tools.list_tools()
        }
    )
    
    result = await orchestrator.orchestrate(task)
    
    print("\n=== Final Results ===")
    print(f"Total Tasks: {result['total_tasks']}")
    print(f"Completed: {result['completed_tasks']}")
    print(f"Failed: {result['failed_tasks']}")
    print(f"\nAgent Performance:")
    for agent_id, metrics in result['agent_metrics'].items():
        print(f"  {agent_id}: {metrics['success_rate']}% success")

if __name__ == "__main__":
    asyncio.run(main())
