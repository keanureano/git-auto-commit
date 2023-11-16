import stanza

def process_text(text):
    # Load the English model
    nlp = stanza.Pipeline('en')
    
    # Process the text
    doc = nlp(text)
    
    return doc