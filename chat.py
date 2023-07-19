import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from streamlit_chat import message

load_dotenv()

# Setting up Conversation Memory
memory = ConversationBufferMemory()

# Setting up Language model with temperature=0.0
llm = ChatOpenAI(temperature=0.0)

# Setting up conversation chain
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

# Initialize the conversation chain and store it in the session state
if "chain" not in st.session_state:
    st.session_state["chain"] = conversation

# Function to generate response for a given input
def generate_response(human_input):
    # Generate a response using the language model chain
    answer = st.session_state["chain"].predict(input=human_input)
    return answer

# Display the title of the app
st.title("🤖 personal bot")

# Initialize session state for generated responses and past messages
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Function to get text input
def get_text():
    # get the user's text input
    input_text = st.text_input(" ", key="input")
    return input_text

# Get user input and generate response
user_input = get_text()
if user_input:
    output = generate_response(user_input)
    # Store user input and generated response
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# Display past conversation
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        # Display user message
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        # Display bot response
        message(st.session_state["generated"][i], key=str(i))
