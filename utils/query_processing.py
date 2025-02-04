import pandas as pd
import re

def process_query(query, data):
    # Define service types & locations based on dataset
    service_types = data["Service"].unique()
    locations = data["Location"].unique()

    # Convert query to lowercase
    query = query.lower()

    # Find service type in query
    found_service = next((service for service in service_types if service.lower() in query), None)

    # Find location in query
    found_location = next((loc for loc in locations if loc.lower() in query), None)

    if found_service and found_location:
        # Filter dataset based on query
        results = data[(data["Service"].str.lower() == found_service) & (data["Location"].str.lower() == found_location)]

        if not results.empty:
            business_info = results.iloc[0]  # Take the first matching result
            return f"Name: {business_info['Business Name']}, Contact: {business_info['Phone Number']}"
        else:
            return "No matching business found."

    return "Could not understand your request. Try again with a service and location."
