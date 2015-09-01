import requests, re
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd 
from pandas import DataFrame
pd.options.display.width = 150
import matplotlib.pyplot 

class JobPosting:
	def __init__(self,job_title,href,company,location):
		self.job_title=job_title
		self.href=href
		self.company=company
		self.location=location

removable_words = ["jobs","apply","email","password","new","please","required",
					"opportunities","skills","sign","talent","follow",
					"job","work","click","home","next","us","start","take","enter"
					,"date","people","career","hours","week","type","attach","resume","search","advanced","privacy","terms",
					"find","years","experience","find","title","keywords","company","indeed","help","centre","cookies",
					"post","(free)","industry","employment","ago","save","forums","browse","employer","browse","city",
					"province","title","api","review","application","help","instructions","applying","full","time","opportunity",
					"team","join","resumes","employers","rights","reserved","create","north","america","toronto","interview","cover","letter",
					"30+","days","inc","trends"]

#Define function to scrape and process text of a given URL
def scrapeText(url):
	html = requests.get(url).text
	text = BeautifulSoup(html,'html.parser')
	iframe = text.iframe
	if iframe:
		try:
			extra = scrapeText(iframe['src'])
		except:
			extra=[]
	else:
		extra = []
	for garbage in text(["head","script","style","input"]):
		garbage.extract()
	text = " ".join(text.strings)
	text = text.replace(u'\xa0', ' ').encode('utf-8')
	text = re.sub(r'(\.+ )|,|\||:|/|\'|\-|;|\*|(\s\d+\s)|(\s\W\s)',' ',text)
	text = re.sub(r'(\s+)|(\s+\d+\s+)',' ',text)
	arr = text.lower().split()
	arr = [word for word in arr if word not in stopwords.words("english") and word.encode('string-escape')[0]!='\\']
	arr = [word for word in arr if word not in removable_words]
	return arr + extra

#Create a list of job URLs called 'job_postings' from indeed
def getURLs(search_query):
	job_postings=[]
	while True:
		html = requests.get('http://www.indeed.ca'+search_query).text
		soup = BeautifulSoup(html,'html.parser')

		for job in soup.find_all("a",class_="turnstileLink"):
			if job.parent.name == 'h2':
				title = job.text.strip()
				href = job['href']
				try:
					company = job.parent.parent.find_all('span','company')[0].text.strip()
				except:
					company = "No Company"
				location = job.parent.parent.find_all('span','location')[0].text.strip()
				job_postings.append(JobPosting(title,href,company,location))

		if not 'Next' in soup.find_all("span","np")[0].text:
			try:
				soup.find_all("span","np")[1]
				search_query = soup.find_all("span","np")[1].parent.parent['href']
			except:
				break
		else:
			search_query = soup.find_all("span","np")[0].parent.parent['href']
	print "Found %d job URLs" % len(job_postings)
	return job_postings

#Create dataframe of job information from given job URLs by scraping the HTML off each URL
def scrapeJobs(job_postings):
	print "Scraping text from URLs..."
	for job,num in zip(job_postings,range(len(job_postings))):
		try:
			job.words = scrapeText('http://www.indeed.ca'+job.href)
		except: 
			job.words = "null"
			print "Failed scraping job %d" % num

	df = DataFrame({'Title':[],'Company':[],'Location':[],'Description':[]})
	df = df[['Title','Company','Location','Description']]
	for i in range(len(job_postings)):
		df.loc[i] = [job_postings[i].job_title,job_postings[i].company,
		job_postings[i].location,job_postings[i].words]
	df=df[df.Description!="null"]
	print "Successfully scraped text from %d jobs." % len(df)
	return df 

#Create plots for keyword frequency and bigram frequency
def analyzeJobs(skills,df):
	skills_series = pd.Series()
	for skill in skills:
		df[skill]=df.Description.apply(lambda x: 1 if skill in x else 0)
		skills_series[skill] = int(df[skill].sum()/float(len(df))*100)
	skills_series.sort(ascending=False)
	for skill,count in zip(skills_series.index,skills_series):
		print "%s in %d%% of jobs" % (skill, count)

	def find_bigrams(input_list):
	  bigram_list = []
	  for i in range(len(input_list)-1):
	      bigram_list.append(input_list[i] + " " + input_list[i+1])
	  return bigram_list

	df['bigrams']=df['Description'].apply(find_bigrams)

	bigram_series = pd.Series()
	for bigrams in df['bigrams']:
		bigram_counter = pd.Series()
		for bigram in set(bigrams):
			if bigram in bigram_counter:
				bigram_counter[bigram]+=1
			else:
				bigram_counter[bigram]=1
		bigram_series=bigram_series.add(bigram_counter,fill_value=0)

	bigram_series.sort(ascending=False)

	print "Top 25 Most Frequent Bigrams, % of Postings with Bigram"
	for x,y in zip(bigram_series.index,bigram_series[:25]):
	    print x + ": " + str(int(y/len(df)*100)) + "%"
    
	skills_plot = skills_series.plot(kind='bar',title='Percent of Jobs with Programming Language, Indeed Query: Developer Toronto')
	skills_plot.set_ylabel('% of Jobs')
	matplotlib.pyplot.tight_layout()
	matplotlib.pyplot.savefig('skills_plot.png')
	matplotlib.pyplot.close()
	bigrams_plot = bigram_series[:20].plot(kind='barh',title='Percent of Jobs with Bigram, Indeed Query: Developer Toronto')
	matplotlib.pyplot.gca().invert_yaxis()
	matplotlib.pyplot.tight_layout()
	matplotlib.pyplot.savefig('bigrams_plot.png')
	matplotlib.pyplot.close()