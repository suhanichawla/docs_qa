from dotenv import load_dotenv
import os
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
import streamlit as st
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.core.postprocessor import SentenceEmbeddingOptimizer

load_dotenv()


@st.cache_resource(show_spinner=False)
def get_index():
    pc = Pinecone(
        api_key=os.environ["PINECONE_API_KEY"],
        environment=os.environ["PINECONE_ENVIRONMENT"],
    )
    pinecone_index = pc.Index(name="docs-helper")
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    callback_manager = CallbackManager(handlers=[llama_debug])
    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store, callback_manager=callback_manager
    )


if __name__ == "__main__":
    print("RAG Start")


index = get_index()
if "chat_engine" not in st.session_state.keys():
    postprocessor = SentenceEmbeddingOptimizer(embed_model=index._embed_model, percentile_cutoff=0.5, threshold_cutoff=0.7)
    st.session_state.chat_engine = index.as_chat_engine(verbose=True, postprocessor=[postprocessor])
st.set_page_config(
    page_title="Llama index docs",
    page_icon="",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("Chat w llama index")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about llama index docs"}
    ]



if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            pp = prompt or ""
            response = st.session_state.chat_engine.chat(message=pp)
            nodes = [node for node in response.source_nodes]
            #print("nies", nodes)
            for col, node, i in zip(st.columns(len(nodes)), nodes, range(len(nodes))):
                with col:
                    st.header(f"Source Node {i+1}: score = {node.score}")
                    st.write(node.text)
            st.write(response.response)
            message = {
                "role": "assistant",
                "content": response.response
            }
            st.session_state.messages.append(message)
