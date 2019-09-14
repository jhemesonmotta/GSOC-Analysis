#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import re
import requests
import pandas as pd


# In[9]:


file_csv = 'gsoc_.csv'


# In[2]:


session = requests.session()
years = ['2016']


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
    
    #counter = 0 
    list_link_project = []
    url_master_gsof_ = 'https://summerofcode.withgoogle.com/archive/' + year + '/projects/'
    num_pages = get_num_pages(url_master_gsof_)

    
    for num in range(1,int(num_pages)):
        session = requests.session()
        url_master_gsof_ = 'https://summerofcode.withgoogle.com/archive/' + year + '/projects/?page=' + str(num)
        response_master = session.get(url_master_gsof_)
        lista_projetos = (BeautifulSoup(response_master.content, 'html.parser'))
        regex_classe = re.compile(r'\bmd-padding archive-project-card__header\b')
        list_projects_master = lista_projetos.findAll("div", {"class": regex_classe})
        url_archive = 'https://summerofcode.withgoogle.com'
        
        
        for i in list_projects_master:
            i = i.find('a', href=True)['href']
            url_project_specific = str(url_archive) + str(i)
            list_link_project.append(url_project_specific)
    return list_link_project


# In[5]:


def get_specific_project_data(year,url_specific_project):
    line = []
    global df_projects
    specific_project_page = session.get(url_specific_project)
    page_specific_project = (BeautifulSoup(specific_project_page.content, 'html.parser'))
    card_specific_project = page_specific_project.find('md-card')
    html_card_specific_project = (BeautifulSoup(str(card_specific_project), 'html.parser'))
    
    company = html_card_specific_project.find("a")["aria-label"]
    company_website = html_card_specific_project.find("a")["href"]
    
    student_name = re.findall('<h4 class="org__meta-heading">Student</h4>\n<div>(.*)</div>',str(card_specific_project),re.MULTILINE)
    github_project_url = html_card_specific_project.find("a", {"class": "md-button md-primary"})["href"]
    project_name = page_specific_project.find('title').get_text()
    
    line.append(year)
    line.append(company)
    
    line.append(str(student_name[0]))
    line.append(project_name)
    line.append('student')
    line.append(github_project_url)
    
    technology_and_topic = get_technologies_and_topics(company_website)
    
    line.append(technology_and_topic[0])
    line.append(technology_and_topic[1])

    print(line)
    
    df_projects = df_projects.append(pd.Series(line, index=None ), ignore_index=True)

    
    list_mentors = html_card_specific_project.findAll("li")
    for mentor in list_mentors:
        line = []
        line.append(year)
        line.append(company)
        
        line.append(mentor.get_text())
        line.append(project_name)
        line.append('mentor')
        line.append(github_project_url)
        line.append(technology_and_topic[0])
        line.append(technology_and_topic[1])

        print(line)
        df_projects = df_projects.append(pd.Series(line, index=None ), ignore_index=True)
    return df_projects

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

df_projects = pd.DataFrame(index=None)
for year in years:
    links_projects = get_procject_urls(year)
    for link in links_projects:
        get_specific_project_data(year,link)

#get_technologies_and_topics('/2017/organizations/6565611412914176/')

# In[8]:

df_projects.to_csv(file_csv,index=False)





