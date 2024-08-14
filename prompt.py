
def getPrompt(instruction_document, instruction_labels, document, labels):
      introduction = """You are a perfect document information extraction system.
You are given a document and a json with keys that must be extracted from the document. 
Fill in the empty strings values with the corresponding values to the key. Insert only the answer. 
If a label is not inclueded in the input, fill the empty strings with "NONE". Now will follow an explanation of every label.
label: company - The name of the company. Only one is correct
label: date - The date of the receip. Only one is correct. Format it how it is on the reciept.
label: address - The address of the company. Seperate information found on different lines with ','.
label: total - The total amount of the receip. Only one is correct. Format to 2 decimal places. Do not include the currency symbol.
Now a example document will follow:"""
      explanation_results = "This would be the results of the example document:"
      transition_to_extraction = "This is the document you must extract the information from:"
      json_to_extract = "Replace all None with the correct information:"
      return f"{introduction}\n{instruction_document}\n\n{explanation_results}\n{instruction_labels}\n\n{transition_to_extraction}\n{document}\n{json_to_extract}\n{labels}"
      
