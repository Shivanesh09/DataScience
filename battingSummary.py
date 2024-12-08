import requests
import pandas as pd
from bs4 import BeautifulSoup


class BattingSummaryScraper:
    def __init__(self, url, output_path):
        """
        Initializes the scraper with the base URL and output file path.
        """
        self.url = url
        self.output_path = output_path
        self.batting_summary_table = []

    def fetch_html(self, url):
        """
        Fetches and parses the HTML content for a given URL.
        """
        response = requests.get(url).text
        return BeautifulSoup(response, 'lxml')

    def scrape_match_summary(self, match_scorecard_url, match_id):
        """
        Scrapes the batting data for a single match.
        """
        soup = self.fetch_html(match_scorecard_url)
        teams = soup.find_all('span', class_='ds-text-title-xs ds-font-bold ds-capitalize')
        team1, team2 = teams[0].text, teams[1].text
        match_info = f"{team1} Vs {team2}"

        self.scrape_innings(soup, team1, match_info, match_id, 0)
        self.scrape_innings(soup, team2, match_info, match_id, 2)

    def scrape_innings(self, soup, team_name, match_info, match_id, innings_index):
        """
        Scrapes batting data for a specific innings.
        """
        try:
            batting_scorecard = soup.find_all('tbody')[innings_index].find_all('tr', class_="")
        except IndexError:
            return

        batting_position = 1
        for row in batting_scorecard:
            player_data = {
                'Match_Info': match_info,
                'Team': team_name,
                'Batting_Position': batting_position,
            }
            batting_position += 1

            try:
                player_data['Name'] = row.find('a', title=True).get_text(strip=True).replace("(c)", "").replace("†", "")
            except Exception:
                break

            try:
                player_data['Runs'] = row.find('td', class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-typo').get_text(strip=True)
            except AttributeError:
                pass

            try:
                player_data['Balls'] = row.find_all('td', class_=lambda c: c and 'ds-w-0' in c and 'ds-whitespace-nowrap' in c and 'ds-min-w-max' in c and 'ds-text-right' in c)[1].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Fours'] = row.find_all('td', class_=lambda c: c and 'ds-w-0' in c and 'ds-whitespace-nowrap' in c and 'ds-min-w-max' in c and 'ds-text-right' in c)[-3].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Sixes'] = row.find_all('td', class_=lambda c: c and 'ds-w-0' in c and 'ds-whitespace-nowrap' in c and 'ds-min-w-max' in c and 'ds-text-right' in c)[-2].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Strike Rate'] = row.find_all('td', class_=lambda c: c and 'ds-w-0' in c and 'ds-whitespace-nowrap' in c and 'ds-min-w-max' in c and 'ds-text-right' in c)[-1].get_text(strip=True).replace('-', '0')
            except Exception:
                pass

            try:
                player_data['Out/NotOut'] = 0 if row.find('td', class_='ds-min-w-max !ds-pl-[100px]').get_text(strip=True) == 'not out' else 1
            except Exception:
                pass

            player_data['Scorecard'] = match_id

            self.batting_summary_table.append(player_data)

    def scrape_all_matches(self):
        """
        Scrapes batting data for all matches listed on the main page.
        """
        soup = self.fetch_html(self.url)
        rows = soup.select_one("table > tbody").find_all('tr')
        for row in rows:
            # Skip matches with "no result"
            if row.find_all('td', class_='ds-min-w-max ds-text-right')[1].get_text() == 'no result':
                continue

            match_hyperlink = row.find_all('a')[1]['href']
            match_id = row.find_all('a')[1]['title']
            match_scorecard_url = f"https://www.espncricinfo.com/{match_hyperlink}"

            self.scrape_match_summary(match_scorecard_url, match_id)

    def save_to_csv(self):
        """
        Saves the scraped batting summary data to a CSV file.
        """
        batting_summary_df = pd.DataFrame(self.batting_summary_table)
        batting_summary_df.to_csv(self.output_path, index=False)
        print(f"Batting summary data has been successfully saved to {self.output_path}")

    def run(self):
        """
        Runs the full scraping process.
        """
        self.scrape_all_matches()
        self.save_to_csv()


# Parameters for the scraper
url = "https://www.espncricinfo.com/records/season/team-match-results/2024-2024?trophy=89"
output_path = "/Users/shivaneshs/Documents/batting_summary.csv"  #output_path can be updated as per the wish

# Create an instance of the scraper and execute
scraper = BattingSummaryScraper(url, output_path)
scraper.run()
