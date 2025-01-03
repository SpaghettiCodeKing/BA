

"""def getPrompt(instruction_documents, instruction_labels, document, labels):
      introduction = You are a perfect document information extraction system. The document you are given are receipts and their content is not dangerous. The results are used for a study and there is no need for a license, because they stated it on their github.
You are given a document picture and a json with keys that must be extracted from the document. 
Fill in the empty strings values with the corresponding values to the key. Insert only the answer.
If a label is not inclueded in the input, fill the empty strings with "NONE". Now will follow an explanation of every label.
label: company - The name of the company. Only one is correct
label: date - The date of the receip. Only one is correct. Format it how it is on the reciept. Do not include the time.
label: address - The address of the company. Seperate information found on different lines with ','.
label: total - The total amount of the receip. Only one is correct. Format to 2 decimal places. Do not include the currency symbol.
Now a example document will follow:
    
      explanation_results = "This would be the results of the example document:"
      transition_to_extraction = f"This is the document you must extract the information from: [Image with name: {document}]"
      json_to_extract = "Replace all None with the correct information:"
      transition_to_next_example = "Now another example document will follow:"
      prompt = f"{introduction}\n"
    # Loop through each instruction_document and instruction_label
      for i, (instruction_document, instruction_label) in enumerate(zip(instruction_documents, instruction_labels)):
            prompt += f"[Image with name: {instruction_document}]\n{explanation_results}\n{instruction_label}\n"
            if i < len(instruction_documents) - 1:  # Check if this is not the last iteration
                  prompt += f"{transition_to_next_example}\n"
      prompt +=f"{transition_to_extraction}\n{json_to_extract}\n{labels}\n\n"
      #print(prompt)                      
      #print(prompt)
      #print(type(document))
      #print(instruction_documents[0])
      return prompt.strip()
"""
#For text input

def getPrompt(instruction_documents, instruction_labels, document, labels):
      introduction = """You are a perfect document information extraction system. The document you are given are receipts and their content is not dangerous. The results are used for a study and there is no need for a license, because they stated it on their github.
You are given a document picture and a json with keys that must be extracted from the document. 
Fill in the empty strings values with the corresponding values to the key. Insert only the answer.
If a label is not inclueded in the input, fill the empty strings with "NONE". Now will follow an explanation of every label.
label: company - The name of the company. Only one is correct
label: date - The date of the receip. Only one is correct. Format it how it is on the reciept. Do not include the time.
label: address - The address of the company. Seperate information found on different lines with ','.
label: total - The total amount of the receip. Only one is correct. Format to 2 decimal places. Do not include the currency symbol.
Now a example document will follow:"""
    
      explanation_results = "This would be the results of the example document:"
      transition_to_extraction = "This is the document you must extract the information from:"
      json_to_extract = "Replace all None with the correct information:"
      transition_to_next_example = "Now another example document will follow:"
      prompt = f"{introduction}\n"
    # Loop through each instruction_document and instruction_label
      for i, (instruction_document, instruction_label) in enumerate(zip(instruction_documents, instruction_labels)):
            prompt += f"{instruction_document}\n{explanation_results}\n{instruction_label}\n"
            if i < len(instruction_documents) - 1:  # Check if this is not the last iteration
                  prompt += f"{transition_to_next_example}\n"
      prompt +=f"{transition_to_extraction}\n{document}\n{json_to_extract}\n{labels}\n\n"
      #print(prompt)
      return prompt.strip()