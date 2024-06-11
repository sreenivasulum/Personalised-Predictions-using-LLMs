import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

def main():
    st.title("Word Cloud Generator")
    
    # Input text
    input_text = st.text_area("Enter words separated by spaces:", "")
    
    if st.button("Generate Word Cloud"):
        if input_text:
            wordcloud = generate_wordcloud(input_text)
            
            # Display the word cloud
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)
        else:
            st.warning("Please enter some words to generate the word cloud.")

if __name__ == "__main__":
    main()
