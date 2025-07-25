from src.utils.config import config
from src.utils.logger import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Define the output schema
class CodeSuggestion(BaseModel):

    improved_code: str= Field( description= "The improved/ modified code.")
    explanation: str= Field( description= "Concise explanation of the changes done.")



class LLMService:

    def __init__(self):

        # Initialize the LLM
        self.llm= ChatGoogleGenerativeAI(model='gemini-2.5-flash', api_key= config.GOOGLE_API_KEY)

        # Create the parser for output validation and parsing
        self.parser=PydanticOutputParser(pydantic_object=CodeSuggestion)

        # Design the prompt
        self.prompt= ChatPromptTemplate.from_messages(
            

            [
                ("system", (f"""  
                                You are a  specialized code improvement assistant. Given the original code and a user prompt, output improved code and explanation of changes.
                                  
                                Format your output as JSON matching this schema: {{format_instructions}}

                                RULES:
                                - ONLY respond to code impovement requests.
                                - NEVER engage with jokes, personal questions, or non-code topics.
                                - If the request is not about code improvement, respond with: "I can only help with code improvement tasks."
                            
                            """
                            )

                ),

                ("human", (f""" 
                
                                Original code: {{original_code}}
                                User prompt: {{user_prompt}} """

                            )
                
                ),
                
            ])

        # Define the chain
        self.chain= self.prompt | self.llm | self.parser


    
    def generate_code_suggestion(self, original_code: str, user_prompt: str) -> dict:

        try:
            
            logger.debug("Sending request to the LLM.")

            # Call the chain with the inputs

            result: CodeSuggestion = self.chain.invoke({
                    "original_code": original_code,
                    "user_prompt": user_prompt,
                    "format_instructions": self.parser.get_format_instructions()
                })

            logger.info("Received the code suggestion successfully")

            return{
                
                "improved_code": result.improved_code,
                "explanation": result.explanation,
                "success": True,
            }
        
        except Exception as e:

            logger.error(f"LLM Service Error: {str(e)}")

            return{

                "improved_code": original_code,
                "explanation": f"Error occurred while generating code suggestion: {str(e)}",
                "success": False,
            }

