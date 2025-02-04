import streamlit as st
import pandas as pd
from rapidfuzz import process

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
# Custom CSS Styling for Best UI
# -------------------------------
st.markdown("""
    <style>
        body { background-color: #121212; color: #ffffff; }
        .title { text-align: center; color: #1db954; font-size: 3em; font-weight: bold; margin-top: 20px; }
        .business-card {
            background: #1e1e1e; border-radius: 15px; padding: 20px; margin: 15px 0;
            box-shadow: 0 8px 16px rgba(0, 255, 0, 0.2);
            border-left: 5px solid #1db954;
            transition: transform 0.2s;
        }
        .business-card:hover { transform: scale(1.02); }
        .business-card h3 { color: #1db954; font-size: 1.8em; margin-bottom: 5px; }
        .business-card p { color: #ccc; margin: 2px 0; font-size: 1.1em; }
        .search-box { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Function to Find Best Match using AI-Powered NLP
# -------------------------------
def find_best_match(query, df):
    if df.empty or not {"Business Name", "Business Category"}.issubset(df.columns):
        return pd.DataFrame()

    df = df.fillna('')
    choices = df["Business Name"].astype(str).tolist() + df["Business Category"].astype(str).tolist()
    if "Location of Shop" in df.columns:
        choices += df["Location of Shop"].astype(str).tolist()
    if "Reviews of Shop" in df.columns:
        choices += df["Reviews of Shop"].astype(str).tolist()

    best_match = process.extract(query, choices, limit=5, score_cutoff=50)
    if best_match:
        best_matches = [match[0] for match in best_match]
        filtered_df = df[df.apply(lambda row: any(m.lower() in str(row).lower() for m in best_matches), axis=1)]

        if "Reviews of Shop" in filtered_df.columns:
            filtered_df["Reviews of Shop"] = pd.to_numeric(filtered_df["Reviews of Shop"], errors='coerce').fillna(0)
            filtered_df = filtered_df.sort_values(by="Reviews of Shop", ascending=False)

        return filtered_df
    return pd.DataFrame()

# -------------------------------
# Main App UI
# -------------------------------
def main():
    st.markdown("<h1 class='title'>🌟 Go Local Grow</h1>", unsafe_allow_html=True)

    st.sidebar.header("🔍 Quick Navigation")
    st.sidebar.info("Find top-rated local businesses instantly!")

    st.header("Find Your Local Business Effortlessly 🏪")

    query = st.text_input("Search for a business (e.g., bakery in downtown)...", placeholder="Type here...", key="query")

    if st.button("🚀 Search Now"):
        with st.spinner("Finding the best businesses for you..."):
            filtered = find_best_match(query, businesses_df)

        if filtered.empty:
            st.warning("No matching businesses found. Try refining your search.")
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
    st.markdown("<p style='text-align: center;'>Made with ❤️ for local businesses!</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
