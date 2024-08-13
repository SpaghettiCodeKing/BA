
def getPrompt(instruction_document, instruction_labels, document, labels):
      introduction = """You are a perfect document information extraction system.
You are given a document and a json with keys that must be extracted from the document. 
Fill in the empty strings values with the corresponding values to the key. Insert only the answer. 
If a label is not inclueded in the input, fill the empty strings with "NONE".
This is an example document:"""
      explanation_results = "This would be the results of the example document:"
      transition_to_extraction = "This is the document you must extract the information from:"
      json_to_extract = "Replace all None with the correct information:"
      return f"{introduction}\n{instruction_document}\n\n{explanation_results}\n{instruction_labels}\n\n{transition_to_extraction}\n{document}\n{json_to_extract}\n{labels}"
      
