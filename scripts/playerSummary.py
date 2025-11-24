import requests
import pandas as pd
from bs4 import BeautifulSoup


class PlayerSummaryScraper:
    def __init__(self, base_url, output_path):
        """
        Initializes the scraper with the base URL and output file path.
        """
        self.base_url = base_url
        self.output_path = output_path
        self.player_summary_table = []

    def fetch_html(self, url):
        """
        Fetches and parses HTML content for a given URL.
        """
        response = requests.get(url).text
        return BeautifulSoup(response, 'lxml')

    def scrape_player_data(self, squad_hyperlink):
        """
        Scrapes player data for a specific team.
        """
        soup = self.fetch_html(squad_hyperlink)
        squad_data = soup.find_all('div', class_='ds-border-line odd:ds-border-r ds-border-b')

        for player in squad_data:
            player_data = {}
            try:
                player_data['Team'] = soup.find(
                    'span',
                    class_='ds-text-tight-m ds-font-regular ds-text-typo-inverse1'
                ).get_text(strip=True).replace("Squad", "")
            except Exception:
                pass

            try:
                player_data['Name'] = player.find(
                    'span',
                    class_='ds-text-compact-s ds-font-bold ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary ds-block ds-cursor-pointer'
                ).get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Playing Role'] = player.find(
                    'p',
                    class_='ds-text-tight-s ds-font-regular ds-mb-2 ds-mt-1'
                ).get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Batting Style'] = player.find_all(
                    'span',
                    class_='ds-text-compact-xxs ds-font-bold'
                )[1].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Bowling Style'] = player.find_all(
                    'span',
                    class_='ds-text-compact-xxs ds-font-bold'
                )[2].get_text(strip=True)
            except Exception:
                player_data['Bowling Style'] = ''

            try:
                player_data['Image'] = player.find(
                    'img',
                    class_='ds-block'
                ).get('src')
            except Exception:
                pass

            self.player_summary_table.append(player_data)

    def scrape_squads(self):
        """
        Scrapes all squads and collects player data.
        """
        soup = self.fetch_html(self.base_url)
        squads = soup.find_all(
            'div',
            class_='ds-flex lg:ds-flex-row sm:ds-flex-col lg:ds-items-center lg:ds-justify-between ds-py-2 ds-px-4 ds-flex-wrap odd:ds-bg-fill-content-alternate'
        )

        for row in squads:
            hyperlink = row.find('a')['href']
            squad_hyperlink = "https://www.espncricinfo.com" + hyperlink
            self.scrape_player_data(squad_hyperlink)

    def save_to_csv(self):
        """
        Saves the scraped player data to a CSV file.
        """
        player_summary_df = pd.DataFrame(self.player_summary_table)
        player_summary_df.to_csv(self.output_path, index=False)
        print(f"Player summary data has been successfully saved to {self.output_path}")

    def run(self):
        """
        Runs the entire scraping process: squad scraping, player data collection, and saving to CSV.
        """
        self.scrape_squads()
        self.save_to_csv()


# Parameters for the scraper
base_url = "https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2024-1411166/squads"
output_path = "/Users/shivaneshs/Documents/player_summary.csv"  #output_path can be updated as per the wish

# Create an instance of the scraper and execute
scraper = PlayerSummaryScraper(base_url, output_path)
scraper.run()
