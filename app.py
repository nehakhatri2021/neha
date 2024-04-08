import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Recipe Finder", page_icon="🍴")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #add8e6; /* Light blue */
    }}
    .stTextInput>div>div>input {{
        background-color: #f4c2c2; /* Pastel pink */
    }}
    .stButton>button {{
        background-color: #c9e4e7; /* Pastel mint green */
    }}
    .stSelectbox>div>div>div>div {{
        background-color: #e6e6fa; /* Lavender */
    }}
    .stText>div>div>div>div {{
        color: #ffc0cb; /* Pink */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Recipe Finder")

# Define a function for login
def login():
    # Assuming a predefined username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if username == "neha" and password == "1234":
        return True
    else:
        return False

def get_recipes(ingredients, diet):
    # api_key = "<your-api-key"
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": st.secrets["api_key"],
        "query": ingredients,
        "diet": diet,
        "number": 10,
        "addRecipeInformation": True
    }
    response = requests.get(url, params=params)
    return response.json()

def main():
    # Check if user is logged in
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    # If not logged in, show login page
    if not st.session_state.is_logged_in:
        if login():
            st.session_state.is_logged_in = True
        else:
            st.error("Incorrect username or password. Please try again.")
            return

    ingredients = st.text_input("Enter comma-separated ingredients (e.g. chicken, rice, broccoli): ")
    diet = st.selectbox("Dietary restrictions", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Ketogenic"])

    if st.button("Find Recipes"):
        if ingredients:
            response = get_recipes(ingredients, diet)
            results = response["results"]
            if len(results) == 0:
                st.write("No recipes found.")
            else:
                df = pd.DataFrame(results)
                df = df[["title", "readyInMinutes", "servings", "sourceUrl"]]
                st.write(df)
        else:
            st.write("Enter at least one ingredient")

if __name__ == "__main__":
    main()
