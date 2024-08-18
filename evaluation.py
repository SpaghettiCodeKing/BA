from anls_star import anls_score

def test_if_extraction_successfull():
    anls = anls_score("Hello World", "Hello World")
    print(anls)