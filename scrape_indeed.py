import scraping_functions

#Your desired keywords to analyze for frequency
skills=["python","c","c++","java","php","ruby","c#","asp.net","sql","shell","javascript","perl","asp.net","scala",".net"]

#Your desired query URL from indeed.ca
job_postings = scraping_functions.getURLs('/jobs?q=developer&l=toronto')
jobs_dataframe = scraping_functions.scrapeJobs(job_postings)
scraping_functions.analyzeJobs(skills,jobs_dataframe)
