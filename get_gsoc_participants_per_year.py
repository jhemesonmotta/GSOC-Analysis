#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
#import urllib.request
import re
import requests
import pandas as pd


# In[9]:


file_csv = '/tmp/gsoc_.csv'


# In[2]:


session = requests.session()
years = ['2018', '2017', '2016']


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


def get_links_projects(year):
    
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
            #print(url_project_specific)
            list_link_project.append(url_project_specific)
            #counter = counter + 1
            #print (str(num) + '-' + str(counter))
    return list_link_project


# In[5]:


def get_specific_project_data(year,url_specific_project):
    line = []
    global df_projects 
    #df_projects = pd.DataFrame(index=None)
    #global specific_project_page
    specific_project_page = session.get(url_specific_project)
    page_specific_project = (BeautifulSoup(specific_project_page.content, 'html.parser'))
    card_specific_project = page_specific_project.find('md-card')
    html_card_specific_project = (BeautifulSoup(str(card_specific_project), 'html.parser'))
    
    company = html_card_specific_project.find("a")["aria-label"]
    student_name = re.findall('<h4 class="org__meta-heading">Student</h4>\n<div>(.*)</div>',str(card_specific_project),re.MULTILINE)
    github_project_url = html_card_specific_project.find("a", {"class": "md-button md-primary"})["href"]
    project_name = page_specific_project.find('title').get_text()
    
    line.append(year)
    line.append(company)
    
    line.append(str(student_name[0]))
    line.append(project_name)
    line.append('student')
    line.append(github_project_url)
    print(line)
    df_projects = df_projects.append(pd.Series(line, index=None ), ignore_index=True)
    #df_projects.append(line)
    list_mentors = html_card_specific_project.findAll("li")
    for mentor in list_mentors:
        line = []
        line.append(year)
        line.append(company)
        
        #print(company + ';' + github_project_url + ';' + mentor.get_text())
        line.append(mentor.get_text())
        line.append(project_name)
        line.append('mentor')
        line.append(github_project_url)
        print(line)
        df_projects = df_projects.append(pd.Series(line, index=None ), ignore_index=True)
    return df_projects
        #df = df_projects.append(pd.DataFrame(line, columns=None),ignore_index=True)
        #df_projects.append(line)
    
    
    


# In[6]:


df_projects = pd.DataFrame(index=None)
for year in years:
    links_projects = get_links_projects(year)
    for link in links_projects:
        get_specific_project_data(year,link)


# In[8]:


df_projects.to_csv(file_csv,index=False)


# In[ ]:




