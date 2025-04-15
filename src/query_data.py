from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import argparse
from core import getChromaDb

PROMPT_TEMPLATE_RAG = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """

def main():
    # Create CLI
    parse = argparse.ArgumentParser()
    parse.add_argument("query_text", type=str,help="The query text")
    args = parse.parse_args()
    query_text = args.query_text
    query_rag(query_text)

def get_local_embedding_function():
    embeddings =  OllamaEmbeddings(
        model="llama3.2",
    )
    return embeddings

def query_rag(query_text: str):
    embedding = get_local_embedding_function()
    db = getChromaDb(embedding)
    results = db.similarity_search_with_score(query_text, k=5)

    # Context : all the chunks from our database, that best match the query
    # question: the actual question that we want to ask

    context_text = "\n\n---\n\n".join([doc.page_content for doc, score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_RAG)
    prompt = prompt_template.format(context=context_text, question=query_text)
    sources = [ doc.metadata.get("id", None) for doc, score in results]

    print(prompt)

    model = OllamaLLM(model="llama3.2")
    responses = model.invoke(prompt)
    print(responses)
    print(sources)
    return responses



if __name__ == '__main__':
    main()