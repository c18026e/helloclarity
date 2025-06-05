import streamlit as st
from langchain.chains import RetrievalQA
from langchain.llms.bedrock import BedrockLLM
from langchain.vectorstores import FAISS
from langchain.embeddings import BedrockEmbeddings
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType

# Initialize LLM and embeddings
@st.cache_resource
def load_llm_and_embeddings():
    llm = BedrockLLM(model_id="anthropic.claude-v2")  # Or claude-3-sonnet, etc.
    embedding = BedrockEmbeddings()
    return llm, embedding

# Load knowledge bases
@st.cache_resource
def load_kbs(embedding):
    kb_tech_docs = FAISS.load_local("kb_tech_docs_index", embeddings=embedding)
    kb_product_faqs = FAISS.load_local("kb_product_faqs_index", embeddings=embedding)
    return kb_tech_docs, kb_product_faqs

# Create tools
def create_tools(llm, kb_tech_docs, kb_product_faqs):
    qa_tech = RetrievalQA.from_chain_type(llm=llm, retriever=kb_tech_docs.as_retriever())
    qa_faqs = RetrievalQA.from_chain_type(llm=llm, retriever=kb_product_faqs.as_retriever())

    tools = [
        Tool(name="TechDocsQA", func=qa_tech.run, description="Technical documentation queries."),
        Tool(name="ProductFAQsQA", func=qa_faqs.run, description="Product-related FAQs."),
    ]
    return tools

# Initialize agent
@st.cache_resource
def initialize_agentic_system(tools, llm):
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

# Streamlit UI
st.title("🔍 Bedrock Agentic Knowledge Base Assistant")
st.markdown("Ask a question and the agent will decide which knowledge base(s) to use.")

query = st.text_input("Enter your query:")

if query:
    with st.spinner("Thinking..."):
        llm, embedding = load_llm_and_embeddings()
        kb_tech_docs, kb_product_faqs = load_kbs(embedding)
        tools = create_tools(llm, kb_tech_docs, kb_product_faqs)
        agent = initialize_agentic_system(tools, llm)

        response = agent.run(query)
        st.markdown("### 🧠 Agent Response")
        st.write(response)
