import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
#from langchain_core.output_parsers import OutputFixingParser
from prompt.prompt_library import *

class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model.
    Automatically logs all actions and supports session-based organization.
    """
    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        try:
            self.loader=ModelLoader()
            self.llm=self.loader.load_llm()
            
            # Prepare parsers
            #self.parser = JsonOutputParser(pydantic_object=Metadata)
            #self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)
            self.structured_llm = self.llm.with_structured_output(Metadata)
            
            self.prompt = PROMPT_REGISTRY["document_analysis"]
            
            self.log.info("DocumentAnalyzer initialized successfully")
            
            
        except Exception as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {e}")
            raise DocumentPortalException("Error in DocumentAnalyzer initialization", sys)
        
        
    
    def analyze_document(self, document_text:str)-> dict:
        """
        Analyze a document's text and extract structured metadata & summary.
        """
        try:
            chain = self.prompt |  self.structured_llm
            
            self.log.info("Meta-data analysis chain initialized")

            response = chain.invoke({"document_text": document_text})

            #self.log.info("Metadata extraction successful", keys=list(response.keys()))
            response_dict = response.model_dump()

            self.log.info(
                "Metadata extraction successful",
                keys=list(response_dict.keys())
            )
            
            return response.model_dump()

        except Exception as e:
            self.log.error("Metadata analysis failed", error=str(e))
            raise DocumentPortalException("Metadata extraction failed", e) from e
        
    