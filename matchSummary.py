import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


class MatchSummaryScraper:
    def __init__(self, url, output_path):
        """
        Initializes the scraper with the URL and output file path.
        """
        self.url = url
        self.output_path = output_path
        self.soup = None
        self.matches = None

    def fetch_html(self):
        """
        Fetches the HTML content of the page and parses it with BeautifulSoup.
        """
        response = requests.get(self.url).text
        self.soup = BeautifulSoup(response, 'lxml')

    def extract_table(self):
        """
        Locates and extracts the HTML table containing match summaries.
        """
        if not self.soup:
            raise Exception("HTML content not fetched. Call fetch_html() first.")
        
        matches_summary = self.soup.find('table')
        if matches_summary is None:
            raise Exception("No table found on the page.")
        
        # Convert the table HTML to a pandas DataFrame
        matches_summary_html = str(matches_summary)
        matches_summary_io = StringIO(matches_summary_html)
        matches_summary_table = pd.read_html(matches_summary_io)
        
        # Select the first table
        self.matches = matches_summary_table[0]

    def save_to_csv(self):
        """
        Saves the extracted match summaries to a CSV file.
        """
        if self.matches is None:
            raise Exception("No table data available. Call extract_table() first.")
        
        self.matches.to_csv(self.output_path, index=False)
        print(f"Match summary data has been successfully saved to {self.output_path}")

    def run(self):
        """
        Executes the entire process: fetching HTML, extracting table, and saving to CSV.
        """
        self.fetch_html()
        self.extract_table()
        self.save_to_csv()


# Parameters for the scraper
url = "https://www.espncricinfo.com/records/season/team-match-results/2024-2024?trophy=89"
output_path = "/Users/shivaneshs/Documents/matches_summary.csv"  #output_path can be updated as per the wish

# Create an instance of the scraper and run it
scraper = MatchSummaryScraper(url, output_path)
scraper.run()
