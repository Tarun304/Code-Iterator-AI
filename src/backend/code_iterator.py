from src.utils.logger import logger
from src.backend.llm_service import LLMService
from src.backend.diff_service import DiffService
from typing import TypedDict, Dict
from langgraph.graph import StateGraph,  START, END

# Define the worflow state
class WorkflowState(TypedDict):
    original_code: str
    user_prompt: str
    improved_code: str
    explanation: str
    diff_result: dict
    success: bool


class CodeIteratorOrchestrator:

    def __init__(self):
        
        self.llm_service= LLMService()
        self.diff_service= DiffService()

        logger.info("Code Iterator Orchestrator initialized")


    def process_with_llm(self, state: WorkflowState):

        """ Get the improved code from the LLM."""

        logger.debug("Processing with LLM")

        result=self.llm_service.generate_code_suggestion(
            state["original_code"],
            state['user_prompt']
        )


        return {
            "improved_code": result["improved_code"],
            "explanation": result["explanation"],
            "success": result["success"]
        }

    
    def generate_diff(self, state: WorkflowState):

        """ Generate the diff. """

        logger.debug("Generating diff")

        diff_result= self.diff_service.generate_diff(
            state["original_code"],
            state["improved_code"]
        )


        return {"diff_result": diff_result}

    
    def process_code_request(self, original_code: str, user_prompt: str) -> Dict: 

        # Build the workflow: START -> LLM -> DIFF -> END   
        graph= StateGraph(WorkflowState)


        # Add the nodes
        graph.add_node("llm_step", self.process_with_llm)
        graph.add_node("diff_step", self.generate_diff)


        # Add the edges
        graph.add_edge(START, "llm_step")
        graph.add_edge("llm_step", "diff_step")
        graph.add_edge("diff_step", END)

        # Compile the workflow
        workflow=graph.compile()

        # Intitial State
        initial_state: WorkflowState = {
            "original_code": original_code,
            "user_prompt": user_prompt,
            "improved_code": "",
            "explanation": "",
            "diff_result": {},
            "success": False,
        }
        # Run the workflow
        final_state=workflow.invoke(initial_state)

        # Return the results
        return{

            "original_code": final_state["original_code"],
            "improved_code": final_state["improved_code"],
            "explanation": final_state["explanation"],
            "diff": final_state["diff_result"],
            "success": final_state["success"]
        }
        





