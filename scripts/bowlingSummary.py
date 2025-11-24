import requests
import pandas as pd
from bs4 import BeautifulSoup


class BowlingSummaryScraper:
    def __init__(self, url, output_path):
        """
        Initializes the scraper with the base URL and output file path.
        """
        self.url = url
        self.output_path = output_path
        self.bowling_summary_table = []

    def fetch_html(self, url):
        """
        Fetches and parses the HTML content for a given URL.
        """
        response = requests.get(url).text
        return BeautifulSoup(response, 'lxml')

    def scrape_match_summary(self, match_scorecard_url, match_id):
        """
        Scrapes the bowling data for a single match.
        """
        soup = self.fetch_html(match_scorecard_url)
        teams = soup.find_all('span', class_='ds-text-title-xs ds-font-bold ds-capitalize')
        team1, team2 = teams[0].text, teams[1].text
        match_info = f"{team1} Vs {team2}"

        self.scrape_innings(soup, team2, match_info, match_id, 1)
        self.scrape_innings(soup, team1, match_info, match_id, 3)

    def scrape_innings(self, soup, team_name, match_info, match_id, innings_index):
        """
        Scrapes bowling data for a specific innings.
        """
        try:
            bowling_scorecard = soup.find_all('tbody')[innings_index].find_all('tr', class_="")
        except IndexError:
            return

        for row in bowling_scorecard:
            player_data = {
                'Match_Info': match_info,
                'Team': team_name,
            }

            try:
                player_data['Name'] = row.find('span', class_ = 'ds-text-tight-s ds-font-medium ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary ds-block ds-cursor-pointer').get_text(strip = True).replace("(c)", "")
            except Exception:
                break

            try:
                player_data['Overs'] = row.find_all('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[0].get_text(strip = True)
            except AttributeError:
                pass

            try:
                player_data['Maidens'] = row.find_all('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[1].get_text(strip=True)
            except Exception:
                pass
            
            try:
                player_data['Runs'] = row.find_all('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[2].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Wickets'] = row.find('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-text-right').get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Economy'] = row.find_all('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[3].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Dot balls'] = row.find_all('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[4].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Fours'] = row.find_all('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[5].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Sixes'] = row.find_all('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[6].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['Wides'] = row.find_all('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[7].get_text(strip=True)
            except Exception:
                pass

            try:
                player_data['No balls'] = row.find_all('td', class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')[8].get_text(strip=True)
            except Exception:
                pass

            player_data['Scorecard'] = match_id

            self.bowling_summary_table.append(player_data)
    
    def scrape_all_matches(self):
        """
        Scrapes bowling data for all matches listed on the main page.
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
        Saves the scraped bowling summary data to a CSV file.
        """
        bowling_summary_df = pd.DataFrame(self.bowling_summary_table)
        bowling_summary_df.to_csv(self.output_path, index=False)
        print(f"Bowling summary data has been successfully saved to {self.output_path}")

    def run(self):
        """
        Runs the full scraping process.
        """
        self.scrape_all_matches()
        self.save_to_csv()



# Parameters for the scraper
url = "https://www.espncricinfo.com/records/season/team-match-results/2024-2024?trophy=89"
output_path = "/Users/shivaneshs/Documents/bowling_summary.csv" #output_path can be updated as per the wish

# Create an instance of the scraper and execute
scraper = BowlingSummaryScraper(url, output_path)
scraper.run()
