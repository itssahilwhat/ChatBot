import streamlit as st
import pandas as pd

# -------------------------------
# Load CSV Data Safely
# -------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    try:
        df_en = pd.read_csv("local_businesses_rajkot_services.csv", encoding="utf-8")
    except Exception as e:
        st.error(f"❌ Error loading CSV file: {e}")
        df_en = pd.DataFrame()
    return df_en

businesses_df = load_data()

# -------------------------------
# Custom CSS Styling for the Best UI Ever!
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
        .css-1d391kg {  /* Use the generated sidebar class from Streamlit */
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
# Enhanced Function to Find Best Match
# -------------------------------
def find_best_match(query, df):
    # Ensure required columns exist
    required_cols = {"Business Name", "Business Category", "Location of Shop"}
    if df.empty or not required_cols.issubset(df.columns):
        return pd.DataFrame()

    df = df.fillna("")
    query_lower = query.lower().strip()

    # Remove common stopwords to make the query flexible.
    stopwords = {"near", "at", "in", "only", "the", "a", "an"}
    tokens = [token for token in query_lower.split() if token not in stopwords]

    # Define a row matcher that requires all tokens to appear in the combined field.
    def row_matches(row):
        combined_field = (row["Business Name"] + " " + row["Business Category"] + " " + row["Location of Shop"]).lower()
        return all(token in combined_field for token in tokens)

    filtered_df = df[df.apply(row_matches, axis=1)].copy()

    # Optionally, sort by "Reviews of Shop" if available.
    if "Reviews of Shop" in filtered_df.columns:
        filtered_df["Reviews of Shop"] = pd.to_numeric(filtered_df["Reviews of Shop"], errors='coerce').fillna(0)
        filtered_df = filtered_df.sort_values(by="Reviews of Shop", ascending=False)

    return filtered_df

# -------------------------------
# Main App UI
# -------------------------------
def main():
    st.markdown("<h1 class='title'>🌟 Go Local Grow</h1>", unsafe_allow_html=True)
    st.sidebar.header("🔍 Quick Navigation")
    st.sidebar.info("Find top-rated local businesses instantly!")
    st.header("Find Your Local Business by Area 🏪")

    # Input: Users can type any query
    query = st.text_input("Search (e.g., plumber at rajkot, barber only, patel home services)...",
                          placeholder="Type here...", key="query")

    if st.button("🚀 Search Now"):
        with st.spinner("Finding businesses in your area..."):
            filtered = find_best_match(query, businesses_df)

        if filtered.empty:
            st.warning("No businesses found matching your search. Try refining your query.")
        else:
            st.success("🎯 Here are the best results!")
            for _, business in filtered.iterrows():
                st.markdown(f"""
                    <div class="business-card">
                        <h3>{business.get("Business Name", "N/A")}</h3>
                        <p><strong>Category:</strong> {business.get("Business Category", "N/A")}</p>
                        <p><strong>Location:</strong> {business.get("Location of Shop", "N/A")}</p>
                        <p><strong>Reviews:</strong> ⭐ {business.get("Reviews of Shop", "No reviews")}</p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            Made with ❤️ for local businesses!<br>
            © 2025 Go Local Grow
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
