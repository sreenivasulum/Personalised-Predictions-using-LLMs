import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.schema.runnable import RunnableLambda
import pandas as pd
st.title('Product Recommendation')

OPENAI_API_KEY ="sk-proj-Re7WpnPtgygJewBx6cNdT3BlbkFJdnVWCv1sGZhbmcmqOGJv"
model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")


template = """Task: Generate a product recommendation based on the user's purchase history.

Input Data:

   1. User Purchase History:
        Columns: user_id, product_review, product_title, rating, timestamp
       for different Categories such as  movies, cds, music, etc.
        {context}
   2. Question: Contains user_id and different options (choices) of different domains {question}.

   Desired Output: Recommended product title from the choices that best matches the user's history.
  Note: Don't give any other information other than product title in the output
   Recommendation Logic:

To generate a relevant product title recommendation for the given user, follow these steps:

    Retrieve User History: Identify the user's past purchases, reviews, and ratings.

    Analyze Preferences: Determine the user's preferred categories and products based on high ratings and positive reviews.

    Match Choices: Compare the user's preferences with the provided choices.

    Recommend Product: Select the product title from the choices that best aligns with the user's historical preferences.

"""

prompt = ChatPromptTemplate.from_template(template)
loader = CSVLoader("Alldomain_data")
text_documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
documents = text_splitter.split_documents(text_documents)


embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore2 = DocArrayInMemorySearch.from_documents(documents, embeddings)



parser = StrOutputParser()
retriever=vectorstore2.as_retriever()

chain = (
    #{"context":retriever,"data":lambda x : ["Paradoxical Commandments","Creative Thoughts About A Challenging Life","A Cozy Read filled with Wisdom","Tap into Secret Wealth"],"question": RunnablePassthrough() }
     {"context":retriever,"question": RunnablePassthrough() }
    # {"context":retriever,"data":{"text1":itemgetter("text1"),"text2":itemgetter("text2"),"text3":itemgetter("text3"),"text4":itemgetter("text4")}|RunnableLambda(create_list),"question": itemgetter("question") }
    #  {"context":retriever,"data":{"text1":"Paradoxical Commandments","text2":"Creative Thoughts About A Challenging Life","text3": "A Cozy Read filled with Wisdom","text4":"Tap into Secret Wealth"}|RunnableLambda(create_list),"question": RunnablePassthrough() }
    | prompt
    | model
    | parser )

# Initialize an empty DataFrame or load an existing one
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['user_id', 'selected_items'])

# Input for user ID
user_id = st.text_input("Enter User ID:")

# Multiselect for items
items = ["Hope's Peak (Harper and Lane)", "Mother Knows Best: The Natural Way to Train Your Dog", "Witch Is When The Floodgates Opened", "Wonderment in Death (In Death Series)", "Blood Red Syrah: A Gruesome California Wine Country Thriller"]
selected_items = st.multiselect("Select items (up to 4):", items, max_selections=4)


# Button to submit the selection
if st.button("Submit"):
    if user_id and selected_items:
        # Store the data in a new DataFrame row
        new_row = pd.DataFrame([[user_id, selected_items]], columns=['user_id', 'selected_items'])
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.success(f"Data submitted for user {user_id}")
    else:
        st.error("Please enter a User ID and select at least one item.")

# Display the current DataFrame
st.write("Current Data:")
st.dataframe(st.session_state.data)
# Button to make predictions
if st.button("Predict"):
    if not st.session_state.data.empty:
        predictions = chain.invoke(str(st.session_state.data))
        st.write("Predictions:")
        st.dataframe(predictions)
    else:
        st.error("No data to predict.")


#for i in range(20):
  #print (f"Prediction{i}.{chain.invoke(str(df3.iloc[i]))}")
  #print (f" Actual{i}.{result_df['ground_truth'].iloc[i]}")