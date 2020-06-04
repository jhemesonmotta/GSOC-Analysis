#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import re
import requests
import pandas as pandas


# In[9]:


file_csv = 'gsoc_2019.csv'


# In[2]:


session = requests.session()
years = ['2019']


# In[3]:


def get_num_pages(url):
    session = requests.session()
    page_pagination = session.get(url)
    page_pagination = (BeautifulSoup(page_pagination.content, 'html.parser'))
    pagination = page_pagination.find('span', {'class': 'paginator__pages'})
    pagination = pagination.get_text()
    num_pages = pagination.split()
    
    return num_pages[-1]


# In[4]:


def get_procject_urls(year):
    
    # declares an empty list
    list_link_project = []
    
    # generates URL for the year
    url_master_gsoc_ = 'https://summerofcode.withgoogle.com/archive/' + year + '/projects/'
    
    # scrapes the number of pages of projects for that year
    num_pages = get_num_pages(url_master_gsoc_)

    # iterates all the pages of projects
    for num in range(1,int(num_pages)):
        # request and store the whole html page of projects
        session = requests.session()
        url_master_gsoc_ = 'https://summerofcode.withgoogle.com/archive/' + year + '/projects/?page=' + str(num)
        response_master = session.get(url_master_gsoc_)
        html_page = (BeautifulSoup(response_master.content, 'html.parser'))
        
        # regex to identify elements representing projects
        regex_classe = re.compile(r'\bmd-padding archive-project-card__header\b')
        
        # find projects according to the regex
        list_projects_master = html_page.findAll("div", {"class": regex_classe})
        url_archive = 'https://summerofcode.withgoogle.com'
        
        # iterates the list of project to get internal specific links
        for i in list_projects_master:
            i = i.find('a', href=True)['href']
            url_project_specific = str(url_archive) + str(i)
            list_link_project.append(url_project_specific)
            
    # returns the list of project specific urls
    return list_link_project


def html_to_line(specific_project_page, person_type, person_name):
    line = []
    page_specific_project = (BeautifulSoup(specific_project_page.content, 'html.parser'))
    card_specific_project = page_specific_project.find('md-card')
    html_card_specific_project = (BeautifulSoup(str(card_specific_project), 'html.parser'))

    # scrapes student information from the content
    project_name = page_specific_project.find('title').get_text()
    company = html_card_specific_project.find("a")["aria-label"]
    company_website = html_card_specific_project.find("a")["href"]
    github_project_url = html_card_specific_project.find("a", {"class": "md-button md-primary"})["href"]
    student_name = re.findall('<h4 class="org__meta-heading">Student</h4>\n<div>(.*)</div>',str(card_specific_project),re.MULTILINE)
    # gets main technology and main topic of the project
    technology_and_topic = get_technologies_and_topics(company_website)
    # stores the retrieved information on the "line"
    line.append(year)
    line.append(company)
    if person_type == 'mentor':
        line.append(person_name)
    else:
        line.append(str(student_name[0]))
    line.append(project_name)
    line.append(person_type)
    line.append(github_project_url)
    line.append(technology_and_topic[0])
    line.append(technology_and_topic[1])
    return line
    
def get_specific_project_data(year,url_specific_project):
    # declares a new array for the line
    line = []
    global contributors_li
    
    # request and store the whole html
    project_page = session.get(url_specific_project)
    
    # sends raw data and receives the data formated in an array
    # Param 1: raw data
    # Param 2: person type (student or mentor)
    # Param 3: person name (in case it's mentor)
    line = html_to_line(specific_project_page, 'student', '')
    
    # appends the line on the global list
    contributors_list = contributors_list.append(pandas.Series(line, index=None), ignore_index=True)
    
    # converts
    page_parsed = (BeautifulSoup(project_page.content, 'html.parser'))
    card = page_parsed.find('md-card')
    card_parsed = (BeautifulSoup(str(card), 'html.parser'))
    
    # scrapes mentors information from the content
    list_mentors = card_parsed.findAll("li")
    for mentor in list_mentors:
        # sends raw data and receives the data formated in an array
        line = html_to_line(page_parsed, 'mentor', mentor.get_text())
        # appends the line on the global list
        contributors_list = contributors_list.append(pandas.Series(line, index=None ), ignore_index=True)
    # returns the whole list
    return contributors_list

# In[6]:


def get_technologies_and_topics(company_link):
    line = []

    specific_company_page = session.get('https://summerofcode.withgoogle.com' + company_link)
    page_specific_object = (BeautifulSoup(specific_company_page.content, 'html.parser'))
    card_specific_text = page_specific_object.find('md-card')
    html_card_specific_object = (BeautifulSoup(str(card_specific_text), 'html.parser'))
    main_tecnology_html = html_card_specific_object.findAll("li", {"class": "organization__tag organization__tag--technology"})
    main_tecnology = (main_tecnology_html[0]).get_text()
    main_topic_html = html_card_specific_object.findAll("li", {"class": "organization__tag organization__tag--topic"})
    main_topic = (main_topic_html[0]).get_text()

    line.append(main_tecnology)
    line.append(main_topic)

    return line

# In[7]:

# declare a new pandas DataFrame
contributors_list = pandas.DataFrame(index=None)

# iterates the list of years in which we want to extract data from
for year in years:
    
    # the first part of the mining is storing the URL of
    # all the projects of the referred year
    links_projects = get_procject_urls(year)
    
    # the second part is iterating the list of projects
    # and retrieving specific data for each project
    for link in links_projects:
        get_specific_project_data(year,link)

# after all the information is extracted,
# it is transformed into a csv file
contributors_list.to_csv(file_csv,index=False)





