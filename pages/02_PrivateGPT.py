import streamlit as st
from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import Html2TextTransformer

urls = ["https://python.langchain.com/docs/integrations/document_transformers/html2text"]
loader = AsyncHtmlLoader(urls)
docs = loader.load()

html2text = Html2TextTransformer()
docs_transformed = html2text.transform_documents(docs)

docs_transformed[0].page_content[1000:2000]

