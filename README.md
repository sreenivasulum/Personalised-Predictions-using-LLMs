# Neohumans-Personalised-Predictions-using-LLMs

**Aim**

Determine what a user is likely to buy on Amazon based on all available data about the user, as opposed to merely building a personalized chatbot that understands user queries better.

**Input:**

    Tweets
    Watched Movies
    Beauty Items
    Amazon Fashion
    Cell Phones
    Book Titles

**Output:**

    Top 5 Recommended Products for the specified domains
    Best Product with an explanation
    In-depth analysis of user purchase history

**Components:**

    ReactJS Code for UI:
        Check the Google Drive link for the code (https://drive.google.com/drive/u/0/folders/1CxnJUX7nLqTGmjTT-u3yyH0zG_tv75re) or github link:https://github.com/sreenivasulum/Reactcode-PersonalisationLLM
    Tweets Extraction API:
    Check the given Link (https://github.com/sreenivasulum/heroku-persona)

    WordCloud API:
        [Check the given Link.] (https://github.com/sreenivasulum/wordcloud)

    Single Domain Product Recommendation:
      Utilizes a targeted approach for specific domains without RAG Approach.please check given [link] (https://github.com/sreenivasulum/productrecommendationllm).

   Multiple Product Recommendation Using RAG Approach:
        Employs Retrieval-Augmented Generation for enhanced product suggestions.
        Developed code:- (https://github.com/yesh-neo/Research-Project/tree/main/api)
         Deployment code: (1.https://github.com/yesh-neo/Research-Project/tree/feature/deployment 2. https://github.com/sreenivasulum/deploymentLLM/tree/simplefunction)

   Datasets folder contains datasets for the mentioned domains

  ** Instructions to run the UI code locally**
  
      1. First download reactjs code from the google drive (https://drive.google.com/drive/u/0/folders/1CxnJUX7nLqTGmjTT-u3yyH0zG_tv75re) or github link:https://github.com/sreenivasulum/Reactcode-PersonalisationLLM.
      2. Install nodejs which is greater than 18+ or 20 +.
      3. Change the path to downloaded file "cd path/vite-project"
      4.  Install npm. (i.e) 1. npm init  2. npm install . Run this two commands after installing nodejs.
      5. Install vite cmd:**npm create vite@latest** (optional if it is not exists).
      6. There is a need to run flask API on the new terminal locally.
         (i). For multiple products, download the deployment code (https://github.com/yesh-neo/Research-Project/tree/feature/deployment). And install the packages from requirements.txt
          (ii). Run the flask api program by using cmd: python3 api.py.
          (iii). After running the program successfully, then it will give url.
          (iv). Copy the URL.
      7. Open RecommendationDashboard.jsx file in the path of vite-project/src/components and paste the url in the .jsx file at the axis.post("https://localhost:6005/getRecommendation"). In the local host url append "/getRecommendation" and place this one.
      8. Then run cmd: **npm run dev**

  **Deployed for Book domain**:
  Please check this link: https://productrecommend.netlify.app/llm
 (i). You will get the recommendations for book domain by clicking on **Book domain** after entering all the details.

**Deployment for multiproduct recommendation**
https://multidomainproductrecommendation.netlify.app/
**Usage:** User can enter all the required for the mentioned domains and twitter username and Check the Recommendations tab to get the insights and recommended products.
 
   
    
