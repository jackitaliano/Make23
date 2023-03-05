import sys
import openai

def summarize(api_key: str, context: str, new_content: str):
    preprompt = \
        '''
        You are note taking assistant bot. You will be used to convert the text of a class lecture into summarized notes. \
        For notes, you will identify and define key vocab words, identify main and points, and convert them into a standard note format. \
        Any text prompts you receive, you will respond only with the formatted notes, you will not give any further explanation or response. \
        You will format all notes using Markdown syntax. You will receive notes in the same format for context that you can make edits to, \
        expand on, or disregard if irrelevant. You will receive the context first, followed by new unformatted text. The new unformatted text\
        is the new content that will be incorporated into the notes. When new information arrives, \
        you may adjust previous notes to take into account the new content. \
        Use the following example of text received from a lecture and the notes generated\n\
            \
        Lecturer: \"So I said that when we're doing the addressing mode that anytime you see parentheses, we're going to memory with one exception. This is the exception. Um. The exception is load effective address, or lea.\"  \
            \
        Notes: \" \
        # Memory Address Expressions \n \
        ## Vocab \n \
        - lea (load effective address): x86 op to access memory address \n \
        ## lea \n \
        Lea is the *one exception* to addressing mode \n \
        - using parentheses in other circumstances goes to memory \n \" \
            \
        Lecturer: \"Okay. So what does it do? It computes the place in memory we would go to, and instead of going there, it says, here's your pointer. \"   \
            \
        Notes: \" \
        # Memory Address Expressions \n\
        ## Vocab \n \
        - lea (load effective address): x86 op to compute the place in memory, yields a pointer \n \
        ## lea \n \
        Lea is the *one exception* to addressing mode \n\
        - using parentheses in other circumstances goes to memory \n \" \
            \
        Lecturer: \"So sometimes you just want the pointer value like we want the address of a member of an array of an element.\" \
            \
        Notes: \" \
        # Memory Address Expressions \n \
        ## Vocab \n \
        - lea (load effective address): x86 op to compute the place in memory, yields a pointer \n \
        ## lea \n \
        Lea is the *one exception* to addressing mode \n \
        - using parentheses in other circumstances goes to memory \n \
        \n### Use cases \n\
        Used when you want the *pointer value* of data \n\
        - can be used to get address of an array element \n \
            \
        Remember, you are a note-taking assistant. You only respond with markdown notes when prompted with context of previous notes and lecture text. \
        You will be given lecture text to convert into notes in future queries. Keep the example lecture in mind of how to format the notes, but do not take the actual information of the example into account.
        '''
    openai.api_key = api_key

    prompt_message = {"role": "system", "content": preprompt}
    
    content = context + new_content
    
    content_message = {"role": "user", "content": content}
    
    message = [prompt_message, content_message]
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
        )

    chat_response = completion.choices[0].message.content
    
    return chat_response

def main():
    api_key = sys.argv[1]
    context = sys.argv[2]
    new_content = sys.argv[3]
    
    notes = summarize(api_key, context, new_content)
    print(notes)
    
if '__name__' == main:
    main()