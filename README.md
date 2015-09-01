# job-keyword-analysis-python
Web scraper built in Python(requests, BeautifulSoup4, pandas)  to analyze keyword frequency for any given Indeed.ca query. The script collects URLs from an indeed.ca search query, visits each URL to scrape its text, and then stores job info in a pandas dataframe for analysis. Two resulting plots are created: percent of jobs with certain keywords and most frequent two word bigrams. 

Usage: Edit 'scrape_indeed.py' to change desired keywords and desired query and then run 'scrape_indeed.py'. 

Example Query: Developer jobs in Toronto, resulting in 1000 jobs 

<b>Percent of Jobs with Certain Keyword</b>
![skills_plot](https://cloud.githubusercontent.com/assets/10667203/9595487/e42af7ce-5034-11e5-8145-b78fba785e5f.png)

<b>Most Frequent Two Word Bigrams</b> 
![bigrams_plot](https://cloud.githubusercontent.com/assets/10667203/9595488/e42c246e-5034-11e5-835a-aab20f9c30cb.png)

