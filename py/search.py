import requests
import openai
import ast
    
def get_search_urls(bing_key: str, query: str):
    
    mkt = 'en-US'
    params = { 'q': query, 'mkt': mkt }
    headers = { 'Ocp-Apim-Subscription-Key': bing_key }
    try:
        response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
        response.raise_for_status()
    except Exception as ex:
        raise ex
    
    results = response.json()
    pages = results['webPages']
    values = pages['value']
    urls = [{'title': value['name'], 'url' : value['displayUrl']} for value in values]
    
    return urls

def get_search_terms(api_key: str, content: str):
    openai.api_key = api_key
    
    preprompt = \
    '''
    You are a resource assistant. You will be given notes, and you should decide if additional information such as a link to a website or a diagram is needed. You will be given notes in markdown format. You will only respond with a list of search queries to search for specific information if there are any is required. If no extra information or images are needed, you will respond only with an empty list.  Use the following examples of notes and search queries generated from the notes to guide future responses:

    Notes:
    "
    ## Flip-Flops
    # T Flip-Flop
    - digital circuit that can store a single bit of data.
    - has a single input called the "toggle" input that can change the output state on the next clock pulse.
    - can be used in frequency division circuits, counters, shift registers, and memory units.

    # JK Flip-Flop
    - stores a single bit of data and has two inputs (J and K) and two outputs (Q and Q').
    - useful in applications where both set and reset operations are required, and where the output needs to toggle when both inputs are high.
    - two types: asynchronous and synchronous JK flip-flops.
    "
    Response: ["T Flip-Flop simple circuit diagram", "JK Flip-Flop simple circuit diagram"]

    Notes:
    "
    # Memory Address Expressions
    ## Vocab
    - lea (load effective address): x86 op to compute the place in memory, yields a pointer
    ## lea
    Lea is the *one exception* to addressing mode
    - using parentheses in other circumstances goes to memory
    ### Use cases
    Used when you want the *pointer value* of data
    - can be used to get address of an array element
    "
    Response: []

    "
    #Computer Architecture

    ## Vocab
    - Memory Pages: A section of memory used by the operating system
    - Page Fault: An error caused by a process attempting to access a memory page that has been swapped out

    ## Memory Pages
    All processes in the computer use memory pages
    - Processors manage memory allocation to the different processes
    - Processors may take memory from a process without it being aware
    - Clean pages don't need to be saved before being swapped out
    - If a process attempts to access a swapped out page, it generates a page fault

    ## Page Faults
    - Any instruction that tries to access memory can generate a page fault, if the page has been swapped out
    "
    Response: ["how memory allocation works"]

    Notes:
    "
    # Morality 

    Morality is a deeply rooted concept in our lives, and an important question that we will tackle throughout this course is the question of good and evil. 

    ## Good and Evil 
    The concept of evil can be exemplified via three pictures: 
    1. Institutional evil- somebody behaving cruelly towards someone else possibly due to the situation they are in.
    2. Osama bin Laden- a mass murderer driven by political causes 
    3. Ted Bundy- an example of crazy-evil 

    ## Nature vs. Situation 
    The course aims to understand the reasons behind why certain people might act in an evil manner. 
    - Is it due to their nature (innate personality) or the situation they are caught in? 
    - There are experiments that examine and dissect the effects of nature vs. situation.
    "
    Response: ["Who is Ted Bundy?"]

    Remember, you are a resource assistant. Going forward, you will not give any responses other than a list of search terms. You will not provide any additional explanation, expand or change the notes, or do anything else. Your response will only include the list of search terms.
    '''

    prompt_message = {"role": "system", "content": preprompt}
    
    content_message = {"role": "user", "content": content}
    
    message = [prompt_message, content_message]
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
        )

    chat_response = completion.choices[0].message.content
    
    return chat_response

def search(openai_key: str, bing_key: str, notes: str):
    search_terms = get_search_terms(openai_key, notes)
    
    query_list = ast.literal_eval(search_terms)
    
    query = query_list[0]
    
    urls = get_search_urls(bing_key, query)
    
    return urls[0]