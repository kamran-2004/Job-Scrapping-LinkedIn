# LinkedIn Job Scraper

This project is a Python-based web scraping tool designed to extract job postings and application links from LinkedIn. It automates the process of collecting job-related data and stores it in a structured CSV file for further analysis.

## Features
- Scrapes job details such as company name, job title, seniority level, number of applicants, posted date, and job description.
- Fetches application links for each job posting.
- Saves the collected data into a CSV file (`jobs_with_application_links.csv`).

## Prerequisites
- Python 3.7 or higher
- Install the required Python libraries:
  ```bash
  pip install requests pandas beautifulsoup4
  ```

## How to Use
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/Job-Scrapping-LinkedIn.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Job-Scrapping-LinkedIn
   ```
3. Run the script:
   ```bash
   python Final.py
   ```
4. The script will scrape job postings for the specified position and location and save the data to `jobs_with_application_links.csv` in the project directory.

## Customization
- You can modify the `position`, `location`, and `geo_id` variables in the `main()` function of `Final.py` to scrape jobs for different roles or locations.

## Notes
- Ensure you have a stable internet connection while running the script.
- LinkedIn's structure may change over time, so some selectors in the script might need to be updated accordingly.
