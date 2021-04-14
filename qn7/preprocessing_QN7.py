#!/usr/bin/env python
# coding: utf-8



import pandas as pd
from faculty import get_xml_link,load_faculty_xml,Faculty
from bs4 import BeautifulSoup
from math import log
import lxml
import networkx as nx
import matplotlib.pyplot as plt
import collections 
import xml.etree.ElementTree as ET

def find_name_with_pid(pid):
    faculty_list = []
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])
    file = open("pid.txt","r")
    pid_list = file.readlines()
    pid_list_rstrip = [pid.replace("_",'/').rstrip() for pid in pid_list]
    for idx, df_line in df.iterrows():
        faculty = Faculty(df_line["Faculty"],pid_list_rstrip[idx],df_line["Position"],df_line["Gender"],df_line["Management"],df_line["Area"])
        faculty_list.append(faculty)
    for faculty in faculty_list:
        print(faculty)
        if(faculty.pid == pid):
            return faculty.name


def find_all_coauthors():
    faculty_list = []
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])
    file = open("pid.txt","r")
    pid_list = file.readlines()
    pid_list_rstrip = [pid.replace("_",'/').rstrip() for pid in pid_list]
    for idx, df_line in df.iterrows():
        faculty = Faculty(df_line["Faculty"],pid_list_rstrip[idx],df_line["Position"],df_line["Gender"],df_line["Management"],df_line["Area"])
        faculty_list.append(faculty)
        
    coauthor_dict = {}
    pid_strings = [faculty.pid for faculty in faculty_list]
    for pid_string in pid_strings:
        xmlDoc = open(f'faculty_xml/{pid_string.replace("/","_")}.xml','r',encoding='utf-8')
        xmlDocData = xmlDoc.read()
        xmlDocTree = ET.XML(xmlDocData)
                      
        coauthor_pid_list = []
                      
        for CA in xmlDocTree.iter('author'):
            
            if CA.attrib['pid'] not in pid_list_rstrip:     #not in NTU
                coauthor_pid_list.append(CA.attrib['pid'])         #repetition allowed for the question
        xmlDoc.close()             
        coauthor_dict[pid_string] = coauthor_pid_list
        
                      
    return(coauthor_dict)





def name_with_pid():
    faculty_list = []
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])
    file = open("pid.txt","r")
    pid_list = file.readlines()
    pid_list_rstrip = [pid.replace("_",'/').rstrip() for pid in pid_list]
    for idx, df_line in df.iterrows():
        faculty = Faculty(df_line["Faculty"],pid_list_rstrip[idx],df_line["Position"],df_line["Gender"],df_line["Management"],df_line["Area"])
        faculty_list.append(faculty)
        
    coauthor_dict = {}
    pid_strings = [faculty.pid for faculty in faculty_list]
    for pid_string in pid_strings:
        xmlDoc = open(f'faculty_xml/{pid_string.replace("/","_")}.xml','r',encoding='utf-8')
        xmlDocData = xmlDoc.read()
        xmlDocTree = ET.XML(xmlDocData)
                      
        coauthor_name_with_pid = []
        temp = []            
        for CA in xmlDocTree.iter('author'):
            
            if CA.attrib['pid'] not in pid_list_rstrip:     #not in NTU
                temp = [CA.attrib['pid'],CA.text]
                coauthor_name_with_pid.append(temp)   
                temp=[]                                 #repetition allowed for the question
        xmlDoc.close()
        coauthor_dict[pid_string] =  coauthor_name_with_pid
    ll=[]
    for g in coauthor_dict:
        for i in coauthor_dict[g]:
            if i not in ll:
                ll.append(i)
    df = pd.DataFrame(ll)
    return ll
        
                      


def keys_return():
    faculty_list = []
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])
    file = open("pid.txt","r")
    pid_list = file.readlines()
    pid_list_rstrip = [pid.replace("_",'/').rstrip() for pid in pid_list]
    return pid_list_rstrip




