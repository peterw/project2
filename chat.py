import openai
import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message

load_dotenv()


def generate_response(human_input):
    history = []
    for i in range(len(st.session_state.past)):
        history.append("Human: " + st.session_state.past[i] + "\n" + "AI: " + st.session_state.generated[i] + "\n")
    template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

    Current conversation:
    {history}
    
    AI Assistant:"""
    template = template.format(history=history)
    print(st.session_state.past)

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": template},
            {"role": "user", "content": human_input}
        ])
    response = completion.choices[0].message.content
    return response

st.title("🤖 personal bot")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input(" ", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
