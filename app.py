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
# Enhanced Function to Find Best Match
# -------------------------------
def find_best_match(query, df):
    # Ensure required columns exist
    required_cols = {"Business Name", "Business Category", "Location of Shop"}
    if df.empty or not required_cols.issubset(df.columns):
        return pd.DataFrame()

    df = df.fillna("")
    query_lower = query.lower().strip()

    # Determine service and location parts
    if " near " in query_lower:
        # e.g., "plumber near jetpur road"
        parts = query_lower.split(" near ")
        service_query = parts[0].strip()
        location_query = parts[1].strip()
    else:
        tokens = query_lower.split()
        if len(tokens) >= 3:
            # Assume last two tokens form location, rest form service
            service_query = " ".join(tokens[:-2])
            location_query = " ".join(tokens[-2:])
        elif len(tokens) == 2:
            service_query = tokens[0]
            location_query = tokens[1]
        elif len(tokens) == 1:
            service_query = ""
            location_query = tokens[0]
        else:
            service_query = ""
            location_query = ""

    # Define a function to check if a row matches both service and location criteria.
    def row_matches(row):
        # Combine business name and category for service matching.
        service_field = (row["Business Name"] + " " + row["Business Category"]).lower()
        location_field = row["Location of Shop"].lower()

        service_match = True
        if service_query:
            service_match = service_query in service_field

        location_match = True
        if location_query:
            location_match = location_query in location_field

        return service_match and location_match

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

    # Input: e.g., "plumber near jetpur road" or "plumber jetpur road"
    query = st.text_input("Search by area (e.g., plumber near jetpur road or plumber jetpur road)...",
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
    st.markdown("<p style='text-align: center;'>Made with ❤️ for local businesses!</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()