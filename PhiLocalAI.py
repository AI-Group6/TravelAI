from llama_cpp import Llama

# Function that uses the local model to generate trip planning suggestions
def get_trip_planning_suggestions_local(text):

    # Load the GGUF model (Using Phi)
    llm = Llama(model_path="Phi-3-mini-4k-instruct-q4.gguf")

    prompt = f"""
    Only create a simple travel plan in bullet points for a "{text}" trip separated by days.
    Include a short name for anywhere between 1 to 3 ACTIVITIES and LOCATIONS per day, DO NOT INCLUDE long descriptions and focus on natural language.
    DO NOT generate an output format. Once all days are planned generate 'I hope that helps!'.
    """

    # Generate a response using the local model
    response = llm(prompt, max_tokens=2000, stream=True, stop=["I hope that helps!"])

    generated_text = ""
    for chunk in response:
        # Extract the text from each streamed chunk
        token_text = chunk['choices'][0]['text']
        generated_text += token_text
        print(token_text, end='', flush=True)

    return generated_text


def get_flight_planning_suggestions_local(text):

    # Load the GGUF model (Using Phi)
    llm = Llama(model_path="Phi-3-mini-4k-instruct-q4.gguf")

    prompt = f"""
    Only create a list of flights from the departure city to arrival city in this text: "{text}".
    Include the airline name, price in USD, departure time, and arrival time. DO NOT INCLUDE long descriptions and FOCUS ON NATURAL LANGUAGE.
    Return text in NATURAL LANGUAGE SENTENCE and once 5 flights are generated, generate 'I hope that helps!'.
    """

    # Generate a response using the local model
    response = llm(prompt, max_tokens=2000, stream=True)

    generated_text = ""
    for chunk in response:
        # Extract the text from each streamed chunk
        token_text = chunk['choices'][0]['text']
        generated_text += token_text
        print(token_text, end='', flush=True)

    return generated_text

def get_lodging_planning_suggestions_local(text):

    # Load the GGUF model (Using Phi)
    llm = Llama(model_path="Phi-3-mini-4k-instruct-q4.gguf")

    prompt = f"""
        Only create a list of hotels for the city "{text}".
        Include a short name for the hotel and a price in USD, DO NOT INCLUDE long descriptions and focus on natural language.
        Return text in NATURAL LANGUAGE SENTENCE and once 5 hotels are generated, generate 'I hope that helps!'.
        """

    # Generate a response using the local model
    response = llm(prompt, max_tokens=2000, stream=True, stop=["I hope that helps!"])

    generated_text = ""
    for chunk in response:
        # Extract the text from each streamed chunk
        token_text = chunk['choices'][0]['text']
        generated_text += token_text
        print(token_text, end='', flush=True)

    return generated_text

def get_generic_planning_suggestions_local(text):

    # Load the GGUF model (Using Phi)
    llm = Llama(model_path="Phi-3-mini-4k-instruct-q4.gguf")

    prompt = f"""
    You are an expert travel assistant. Based on the following inquiry: "{text}", provide a detailed response with relevant travel information.
    DO NOT INCLUDE long descriptions and focus on natural language.
    Return text in NATURAL LANGUAGE SENTENCE and once you are done generate 'I hope that helps!'.
    """

    # Generate a response using the local model
    response = llm(prompt, max_tokens=2000, stream=True, stop=["I hope that helps!"])

    generated_text = ""
    for chunk in response:
        # Extract the text from each streamed chunk
        token_text = chunk['choices'][0]['text']
        generated_text += token_text
        print(token_text, end='', flush=True)

    return generated_text

