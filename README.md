# Best World XI – ICC T20 Cricket Data Engineering Project

## Overview
This repository showcases an automated data pipeline to objectively select the Best World XI cricket team from ICC T20 Cricket World Cup 2024 data. The solution demonstrates practical data engineering skills: web scraping, ETL, modular code architecture, data modeling, and role-based analytics, all leading to downstream Tableau visualizations.

## Data Engineering Workflow

- **Data Ingestion:** Python scripts systematically scrape match, player, batting, and bowling data from ESPNcricinfo.
- **ETL Pipeline:** Utilizes pandas for cleaning, transformation, and aggregation of raw data into structured CSV files optimized for analytics.
- **Role-Based Modeling:** Player statistics are mapped to cricket team roles (Opener, Middle Order, Finisher, All-rounder, Fast Bowler) using quantifiable, rule-driven metrics.
- **Modular Architecture:** Code is organized into independent, reusable modules for scalable extraction, transformation, and storage across various tournaments.
- **Data Delivery:** Final processed datasets are stored for direct use in business intelligence (BI) tools such as Tableau.

## Repository Structure

```
/data        # Cleaned and aggregated cricket CSV files
/scripts     # Python modules for web scraping and ETL
/tableau     # Tableau workbooks (.twb) for team analytics
/images      # Dashboard previews and flow diagrams
README.md    # Project summary, workflow, setup instructions
```

## How to Run

1. **Clone the repository**  
2. **Install dependencies:**  
   `pip install requests beautifulsoup4 pandas`
3. **Run scripts in `/scripts`** to generate updated CSV summaries (batting, bowling, match, player).
4. **Open generated CSVs in Tableau** (see `/tableau/Best_World_XI.twb`).
5. **Explore analytics and team selection dashboards**  
   *(Add visuals to `/images` and link them once available.)*

## Roles & Selection Criteria

- **Openers** – High batting average, strike rate, boundary count
- **Middle Order** – Stable average, innings played, consistent scoring
- **Finisher** – High strike rate, runs scored in closing overs
- **All-rounder** – Balanced batting and bowling contributions
- **Fast Bowler** – Effective strike rate, economy, dot ball count

Each role is programmatically evaluated; only top performers meeting or exceeding defined criteria are selected for the final team.

## Tableau Analytics

- Interactive dashboards displaying player statistics, role assignments, and selection criteria
- Objective, transparent team composition using quantified cricket metrics

*(Add dashboard images here once available)*
<img width="2577" height="1555" alt="image" src="https://github.com/user-attachments/assets/0c14d5d4-6786-47c5-97c6-71561b41be45" />


## Data Sources

- [ESPNcricinfo](https://www.espncricinfo.com/records/season/team-match-results/2024-2024?trophy=89)
- [pandas documentation](https://www.geeksforgeeks.org/pandas-tutorial/)

## References

- ESPNcricinfo for raw cricket data
- Tableau for analytics and visualization
- pandas for Python data wrangling

---

*This project demonstrates end-to-end data engineering capabilities: from automated data extraction to structured storage and business intelligence integration.*
