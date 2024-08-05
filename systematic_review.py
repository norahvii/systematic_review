import datetime, os
from pymed import PubMed
import pandas as pd

def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%H_%M_%S"), now.strftime("%Y-%m-%d")

def write_csv(data, search_term):
    now, date = get_timestamp()
    search_term_spaces = search_term.replace(' ', '_')
    print(f'Writing {now}_{date}_{search_term_spaces}.csv...')
    data.to_csv(f'{now}_{date}_{search_term_spaces}.csv', index=True)

def combine_and_save():
    # Get the current working directory
    csv_directory = os.getcwd()

    # Get a list of all CSV files in the current working directory
    csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]

    # Combine all DataFrames into one
    combined_data = pd.concat([pd.read_csv(os.path.join(csv_directory, file)) for file in csv_files], ignore_index=True)

    # Remove duplicates based on all columns
    combined_data = combined_data.drop_duplicates()

    # Sort the DataFrame alphabetically by the 'title' column (adjust column name if needed)
    combined_data = combined_data.sort_values(by='title').reset_index(drop=True).iloc[:, 1:]

    # Save the combined and sorted data to a new CSV file
    combined_data.to_csv('combined_data.csv', index=False)
    print(f'Length of combined_data: {len(combined_data)}')

    # Read the combined data and remove duplicates based on 'pubmed_id'
    unduped_data = combined_data.drop_duplicates(subset='pubmed_id', keep='first')
    unduped_data = unduped_data.iloc[:, 1:]

    # Save the unduplicated data to a new CSV file
    unduped_data.to_csv('combined.csv', index=False)
    print(f'Length of unduped_data: {len(unduped_data)}')

    # Print titles from unduplicated data
    print('Titles from unduped_data:')
    for title in unduped_data['title']:
        print(title)

# Initialize PubMed tool
pubmed = PubMed(tool="MyTool", email="hellonorahvii@gmail.com")

# Read search terms from the search_list.txt file
with open('search_list.txt', 'r') as file:
    search_terms = file.read().splitlines()

for search_term in search_terms:
    # Query PubMed for each search term
    results = pubmed.query(search_term, max_results=500)
    articleList = [article.toDict() for article in results]

    # Create a Pandas DataFrame and write it to CSV
    df = pd.DataFrame(articleList)
    write_csv(df, search_term)

# Combine and save all data
combine_and_save()
