from langchain_community.document_loaders import PyPDFLoader
import pprint
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
# from langchain_aws import BedrockEmbeddings
import getpass
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma





def load_document(data_path="../data/monopoly.pdf"):
    document_loader = PyPDFLoader(data_path)
    return document_loader

def split_documents (documents: list[Document]):
    text_splitter =  RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap =20,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def openAIEmbedding():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return embeddings

def add_to_chroma(chunks : list[Document], db:Chroma):
    # Used for Checking whether chunk remained in same page
    last_page_id = None
    # Used for Chunk id for chunks remain in same page
    current_chunk_index = 0

    # Database Oprimization and Preparation
    existing_items = db.get(include=[])
    # Get all Ids from Chroma Database
    existing_ids = set(existing_items["ids"])
    # Print out Infomation
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    chunks_with_ids = []

    for chunk in chunks:
        # Chunk MetaData Important For Chunk Id
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")+1
        current_page_id = f"{source}:{page}"

        # Add diff ids for chunks from same page
        if last_page_id == current_page_id:
            current_chunk_index += 1
        else:
            # Initial chunk Index id To 0, New Chunk in this page
            current_chunk_index = 0
            # Update page id to Current page
            last_page_id = current_page_id
        # Full id (Unique) and add it to Meta data
        current_page_id = f"{current_page_id}:{current_chunk_index}"
        chunk.metadata['id'] = current_page_id
        chunks_with_ids.append(chunk)

    # Gather Chunks for Adding to Database by checking whether having
    # Existing Id
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata.get(id) not in existing_ids:
            new_chunks.append(chunk)

    # Gather all Ids for new adding Chunks
    new_chunk_ids = [ chunk.metadata["id"] for chunk in new_chunks]
    # Adding to Database
    db.add_documents(documents=new_chunks, ids=new_chunk_ids)


        # db.add_documents(document=chunk.page_content,ids = current_page_id)

def getChromaDb(embeddings):
    vector_store = Chroma(
        collection_name="game_collection",
        embedding_function=embeddings,
        persist_directory="../chroma_db",  # Where to save data locally, remove if not necessary
    )
    return vector_store






def main():
    documents = load_document().load()
    #==============Document Load==============
    # print(documents[0])
    # print()
    # pprint.pp(documents[0].metadata)
    # print()
    # print(len(documents))
    #=============Chunks Size=================
    chunks = split_documents(documents)
    # print(chunks[4].page_content)
    # print()
    # print(len(chunks))
    #==============Embedding Models============
    embeddings = openAIEmbedding()
    db = getChromaDb(embeddings)
    add_to_chroma(chunks,db)
main()