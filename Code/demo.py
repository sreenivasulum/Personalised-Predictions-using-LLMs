
# libraries 
import streamlit as st
import time
import pandas as pd
import json
import tqdm
from datasets import load_dataset
import random
## Calling to OpenAI
from openai import OpenAI

# api keys
openai_api_key = "sk-proj-Re7WpnPtgygJewBx6cNdT3BlbkFJdnVWCv1sGZhbmcmqOGJv"
client = OpenAI(api_key=openai_api_key)

# helpers

# calling open ai
def callOpenAI(prompt):
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are an expert in recommending products to user based on his preferences and past reviews to other products.You were given users past reviews over cross domain products. Analyze user preferrences accross cross domain product reviews  "},
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message.content

 

path = "D:/ai/LLMs/NeoCorp/data/amazon/commonusers/CommonUsers_Product_checkpoint_24-may.csv"
df = pd.read_csv(path)
df_ = df.dropna(subset= ['title_product'])

columns = [
    'user_id',
    'domain',
    'asin',
    'parent_asin',
    'rating', 
    'title_review', 
    'text', 
    'timestamp', 
    'verified_purchase', 
    'title_product',
    'description', 
    'features', 
    'main_category', 
    'average_rating', 
    'rating_number', 
    'price',  
    'details'
    ]
data = df_[columns]

path = "../data/twitter/tweets.csv"
tweets = pd.read_csv(path,nrows=7500)
tweets.columns = [
    "id",
    "timestamp",
    "datetime",
    "type",
    "user",
    "text"
]



def app(user):
    global movies, softwares, tweets, recommendation, actual_product, client
    global data, tweets

    user_df = data[data['user_id'] == user]
    from_domains = [
            "Movies_and_TV",
            "Software"
        ]
    
    to_domains = [
        "Cell_Phones_and_Accessories"
    ]
    
    domain_data = ""
    for d in from_domains:
        domain_data += "#### Domain :: " + d 
        domain_data += " \n"
        for i in range(4):
            domain_df = user_df[user_df['domain'] == d]
            obj = domain_df.iloc[i].to_dict()
            domain_data += "## Product :: " + obj['title_product'] +  " \n"
            domain_data += "## Product Description :: "+ obj['description']+  " \n"
            domain_data += "## User Review :: " + obj['title_review'] + " " + obj['text']  +  " \n"
            domain_data += " \n "

            if d == "Movies_and_TV":
                movies.append(obj['title_product'])

            if d == "Software":
                softwares.append(obj['title_product'])

    tweets = [
        "my lymph nodes are as massive as rahm emanuel's balls right now ",
        "@moony394 omg i can't believe this. i want to cry. freaking fb spoiled me!!! how could this happen?? ",
        '@moony394 i think i will be even more in denial after i watch ',
        'in which episode did house and cuddy hook up?? APO MEETINGS THIS IS ALL YOUR FAULT ',
        "@moony394 i'll miss him too, bb  the episode seemed unimportant after foreteen found kutner, so i stopped watching.",
    ]
    user_tweets_str = ""
    for t in tweets:
        user_tweets_str += "Tweet :: " + t + "\n"
        

    domain_df = user_df[user_df['domain'] == "Cell_Phones_and_Accessories"]
    actual_product = domain_df.title_product.values[0]
    
    d_data = data[data['domain'] == "Cell_Phones_and_Accessories"]
    other_choices = random.sample(list(d_data.title_product.values),3)
    total_choices = [
        actual_product
        ]
    total_choices.extend(other_choices)

    total_choices_str = ""
    for c in total_choices:
        total_choices_str += "Product :: " + c + "\n"
    print(total_choices_str)

    # recommendation :: 
    prompt_template = f"""Role: You are an expert in recommending products to user based on his preferences and past reviews to other products.\
        You were given users past reviews over cross domain products and twitter tweets. Analyze them carefully.

        #### Below are the user previous reviews for products across domains:
        {domain_data}

        #### Here are the User's tweets 
        {user_tweets_str}

        Finaly, here are the choices. Analyze the following choices and select best product from below which user might purchase. 
        #### Product choices
        {total_choices}

        Select one among the above four options. Don't give any explanation just provide me the recommended product name.  
        """
    response = callOpenAI(prompt_template)
    recommendation = response
    return None






users = ('AFZUK3MTBIBEDQOPAK3OATUOUKLA',
    'AHFZUNQFXSVVT6Z6BYKE5CLBX3KQ',
    'AFW2PDT3AMT4X3PYQG7FJZH5FXFA',
    'AHFZUNQFXSVVT6Z6BYKE5CLBX3KQ',
    'AGCI7FAH4GL5FI65HYLKWTMFZ2CQ')


movies = [
]
softwares = [
]
tweets = [
]
recommendation = ""

actual_product = ""

def main():
    st.sidebar.title("Select User")
    option = st.sidebar.selectbox(
    "Select the user.",
    users)

    
    if st.sidebar.button("Get Recomendation"):
        app(option)

    col1, col2 = st.columns(2)
    col1.header("Movies Reviews")
    col1.write(movies)


    col2.header("Software Reviews")
    col2.write(softwares)

    st.header("User Tweets")
    st.write(tweets)

    st.header("Product Recommendation :: ")
    st.write(recommendation)

    st.header("Actual Product :: ")
    st.write(recommendation)
    
if __name__ == "__main__":
   main()