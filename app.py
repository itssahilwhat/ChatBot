# import streamlit as st
# import pandas as pd

# # -------------------------------
# # Load CSV Data Safely
# # -------------------------------
# @st.cache_data(show_spinner=False)
# def load_data(language):
#     try:
#         if language == "English":
#             return pd.read_csv("local_businesses_rajkot_services.csv", encoding="utf-8")
#         elif language == "Gujarati":
#             return pd.read_csv("local_businesses_rajkot_services_gujarati.csv", encoding="utf-8")
#     except Exception as e:
#         st.error(f"❌ Error loading CSV file: {e}")
#         return pd.DataFrame()

# # -------------------------------
# # UI: Language Selection
# # -------------------------------
# st.sidebar.header("🌐 Select Language / ભાષા પસંદ કરો")
# language = st.sidebar.selectbox("Choose your preferred language / તમારી પ્રિય ભાષા પસંદ કરો:", ["English", "Gujarati"])

# # Load the correct dataset
# businesses_df = load_data(language)

# # -------------------------------
# # Function to Find Best Match
# # -------------------------------
# def find_best_match(query, df):
#     if language == "English":
#         required_cols = {"Business Name", "Business Category", "Location of Shop", "Reviews of Shop"}
#     else:  # Gujarati CSV assumed to have same structure but in Gujarati
#         required_cols =  {"Business Name", "Business Category", "Location of Shop", "Reviews of Shop"}
    
#     if df.empty or not required_cols.issubset(df.columns):
#         return pd.DataFrame()
    
#     df = df.fillna("")
#     query_lower = query.lower().strip()

#     stopwords = {"near", "at", "in", "only", "the", "a", "an"} if language == "English" else {"ની નજીક", "માં", "માત્ર", "એ", "એક"}
#     tokens = [token for token in query_lower.split() if token not in stopwords]

#     def row_matches(row):
#         if language == "English":
#             combined_field = (row["Business Name"] + " " + row["Business Category"] + " " + row["Location of Shop"]).lower()
#         else:
#             combined_field = (row["Business Name"] + " " + row["Business Category"] + " " + row["Location of Shop"]).lower()
#         return all(token in combined_field for token in tokens)
    
#     filtered_df = df[df.apply(row_matches, axis=1)].copy()

#     reviews_column = "Reviews of Shop" if language == "English" else "Reviews of Shop"
#     if reviews_column in filtered_df.columns:
#         filtered_df[reviews_column] = pd.to_numeric(filtered_df[reviews_column], errors='coerce').fillna(0)
#         filtered_df = filtered_df.sort_values(by=reviews_column, ascending=False)

#     return filtered_df

# # -------------------------------
# # Main App UI
# # -------------------------------
# def main():
#     title_text = "🌟 Go Local Grow" if language == "English" else "🌟 Go Local Grow"
#     search_placeholder = "Search (e.g., plumber at rajkot, barber only, patel home services)..." if language == "English" else "શોધો (ઉદાહરણ: રાજકોટમાં પ્લમ્બર, ફક્ત બાર્બર, પટેલ હોમ સર્વિસિસ)..."
#     search_button_text = "🚀 Search Now" if language == "English" else "🔍 શોધો"

#     st.markdown(f"<h1 class='title'>{title_text}</h1>", unsafe_allow_html=True)
#     st.sidebar.info("Find top-rated local businesses instantly!" if language == "English" else "ટોચના સ્થાનિક વ્યવસાયોને તરત શોધો!")
#     st.header("Find Your Local Business by Area 🏪" if language == "English" else "તમારા વિસ્તારમાં વ્યવસાય શોધો 🏪")

#     query = st.text_input(search_placeholder, placeholder="Type here...", key="query")

#     if st.button(search_button_text):
#         with st.spinner("Finding businesses in your area..." if language == "English" else "તમારા વિસ્તારના વ્યવસાય શોધી રહ્યા છીએ..."):
#             filtered = find_best_match(query, businesses_df)

#         if filtered.empty:
#             st.warning("No businesses found matching your search. Try refining your query." if language == "English" else "તમારા શોધ માટે કોઈ વ્યવસાય મળ્યા નથી. કૃપા કરી વધુ સ્પષ્ટતાથી શોધો.")
#         else:
#             st.success("🎯 Here are the best results!" if language == "English" else "🎯 અહીં શ્રેષ્ઠ પરિણામો છે!")
#             for _, business in filtered.iterrows():
#                 if language == "English":
#                     st.markdown(f"""
#                         <div class='business-card'>
#                             <h3>{business.get("Business Name", "N/A")}</h3>
#                             <p><strong>Category:</strong> {business.get("Business Category", "N/A")}</p>
#                             <p><strong>Location:</strong> {business.get("Location of Shop", "N/A")}</p>
#                             <p><strong>Reviews:</strong> ⭐ {business.get("Reviews of Shop", "No reviews")}</p>
#                         </div>
#                     """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"""
#                         <div class='business-card'>
#                             <h3>{business.get("Business Name", "N/A")}</h3>
#                             <p><strong>કેટેગરી:</strong> {business.get("Business Category", "N/A")}</p>
#                             <p><strong>સ્થાન:</strong> {business.get("Location of Shop", "N/A")}</p>
#                             <p><strong>સમીક્ષાઓ:</strong> ⭐ {business.get("Reviews of Shop", "કોઈ સમીક્ષા નથી")}</p>
#                         </div>
#                     """, unsafe_allow_html=True)

#     st.markdown("<hr>", unsafe_allow_html=True)
#     footer_text = "Made with ❤️ for local businesses!<br>© 2025 Go Local Grow" if language == "English" else "સ્થાનિક વ્યવસાય માટે પ્રેમથી બનાવવામાં આવ્યું છે!<br>© 2025 સ્થાનિક વ્યવસાય શોધો"
#     st.markdown(f"""
#         <div class='footer'>
#             {footer_text}
#         </div>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()


import streamlit as st
import pandas as pd

# -------------------------------
# Add Custom CSS for Styling
# -------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #141E30, #243B55);
            color: #ffffff;
            margin: 0;
            padding: 0;
        }
        .title {
            text-align: center;
            color: #1db954;
            font-size: 3.5em;
            font-weight: 600;
            margin-top: 20px;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }
        .business-card {
            background: rgba(30, 30, 30, 0.85);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            border-left: 5px solid #1db954;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .business-card:hover {
            transform: scale(1.03);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
        }
        .business-card h3 {
            color: #1db954;
            font-size: 1.8em;
            margin-bottom: 10px;
        }
        .business-card p {
            color: #cccccc;
            margin: 4px 0;
            font-size: 1.1em;
        }
        .search-box {
            text-align: center;
            margin: 30px 0;
        }
        .stButton>button {
            background: #1db954;
            border: none;
            color: #fff;
            padding: 10px 25px;
            font-size: 1.1em;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .stButton>button:hover {
            background: #17a54d;
        }
        /* Sidebar styling */
        .css-1d391kg {  
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: #ffffff;
        }
        .css-1d391kg .sidebar-content {
            font-size: 1.1em;
        }
        /* Footer styling */
        .footer {
            text-align: center;
            padding: 2rem 0;
            color: #b0bec5;
            font-size: 0.9em;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Load CSV Data Safely
# -------------------------------
@st.cache_data(show_spinner=False)
def load_data(language):
    try:
        if language == "English":
            return pd.read_csv("local_businesses_rajkot_services.csv", encoding="utf-8")
        elif language == "Gujarati":
            return pd.read_csv("local_businesses_rajkot_services_gujarati.csv", encoding="utf-8")
    except Exception as e:
        st.error(f"❌ Error loading CSV file: {e}")
        return pd.DataFrame()

# -------------------------------
# UI: Language Selection
# -------------------------------
st.sidebar.header("🌐 Select Language / ભાષા પસંદ કરો")
language = st.sidebar.selectbox("Choose your preferred language / તમારી પ્રિય ભાષા પસંદ કરો:", ["English", "Gujarati"])

# Load the correct dataset
businesses_df = load_data(language)

# -------------------------------
# Function to Find Best Match
# -------------------------------
def find_best_match(query, df):
    required_cols = {"Business Name", "Business Category", "Location of Shop", "Reviews of Shop"}
    
    if df.empty or not required_cols.issubset(df.columns):
        return pd.DataFrame()
    
    df = df.fillna("")
    query_lower = query.lower().strip()

    stopwords = {"near", "at", "in", "only", "the", "a", "an"} if language == "English" else {"ની નજીક", "માં", "માત્ર", "એ", "એક"}
    tokens = [token for token in query_lower.split() if token not in stopwords]

    def row_matches(row):
        combined_field = (row["Business Name"] + " " + row["Business Category"] + " " + row["Location of Shop"]).lower()
        return all(token in combined_field for token in tokens)
    
    filtered_df = df[df.apply(row_matches, axis=1)].copy()

    reviews_column = "Reviews of Shop"
    if reviews_column in filtered_df.columns:
        filtered_df[reviews_column] = pd.to_numeric(filtered_df[reviews_column], errors='coerce').fillna(0)
        filtered_df = filtered_df.sort_values(by=reviews_column, ascending=False)

    return filtered_df

# -------------------------------
# Main App UI
# -------------------------------
def main():
    title_text = "🌟 Go Local Grow"
    search_placeholder = "Search (e.g., plumber at rajkot, barber only, patel home services)..." if language == "English" else "શોધો (ઉદાહરણ: રાજકોટમાં પ્લમ્બર, ફક્ત બાર્બર, પટેલ હોમ સર્વિસિસ)..."
    search_button_text = "🚀 Search Now" if language == "English" else "🔍 શોધો"

    st.markdown(f"<h1 class='title'>{title_text}</h1>", unsafe_allow_html=True)
    st.sidebar.info("Find top-rated local businesses instantly!" if language == "English" else "ટોચના સ્થાનિક વ્યવસાયોને તરત શોધો!")
    st.header("Find Your Local Business by Area 🏪" if language == "English" else "તમારા વિસ્તારમાં વ્યવસાય શોધો 🏪")

    query = st.text_input(search_placeholder, placeholder="Type here...", key="query")

    if st.button(search_button_text):
        with st.spinner("Finding businesses in your area..." if language == "English" else "તમારા વિસ્તારના વ્યવસાય શોધી રહ્યા છીએ..."):
            filtered = find_best_match(query, businesses_df)

        if filtered.empty:
            st.warning("No businesses found matching your search. Try refining your query." if language == "English" else "તમારા શોધ માટે કોઈ વ્યવસાય મળ્યા નથી. કૃપા કરી વધુ સ્પષ્ટતાથી શોધો.")
        else:
            st.success("🎯 Here are the best results!" if language == "English" else "🎯 અહીં શ્રેષ્ઠ પરિણામો છે!")
            for _, business in filtered.iterrows():
                st.markdown(f"""
                    <div class='business-card'>
                        <h3>{business.get("Business Name", "N/A")}</h3>
                        <p><strong>Category:</strong> {business.get("Business Category", "N/A")}</p>
                        <p><strong>Location:</strong> {business.get("Location of Shop", "N/A")}</p>
                        <p><strong>Reviews:</strong> ⭐ {business.get("Reviews of Shop", "No reviews")}</p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    footer_text = "Made with ❤️ for local businesses!<br>© 2025 Go Local Grow"
    st.markdown(f"<div class='footer'>{footer_text}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
