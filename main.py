import libxml2
import sys
import os
import commands
import re
import sys
import MySQLdb
from xml.dom.minidom import parse, parseString
# for converting dict to xml 
from cStringIO import StringIO
from xml.parsers import expat

#def get_elms_for_atr_val(tag,atr,val):
def get_elms_for_atr_val(tag):
   lst=[]
   elms = dom.getElementsByTagName(tag)
   # ............
   
   lst=elms[2].childNodes
   
   lst = lst[1:]
   
   
   return lst
# get all text recursively to the bottom
def get_text(e):
   lst=[]
   for x in e.childNodes:
   		if x.nodeType in (3,4):
   			if x.data != "\n":
   				lst.append(replace_white_space(x.data)) 
   		else:
   				lst=lst + get_text(x)
   # ............
   return lst

# replace whitespace chars
def replace_white_space(str):
   p = re.compile(r'\s+')
   new = p.sub(' ',str)   # a lot of \n\t\t\t\t\t\t
   return new.strip()

# replace but these chars including ':'
def replace_non_alpha_numeric(s):
   p = re.compile(r'[^a-zA-Z0-9:-]+')
   #   p = re.compile(r'\W+') # replace whitespace chars
   new = p.sub(' ',s)
   return new.strip()

# convert to xhtml
# use: java -jar tagsoup-1.2.jar --files html_file
def html_to_xml(fn):
   # ............
   lst=[]
   s = commands.getoutput('java -jar tagsoup-1.2.jar --files '+fn)
   lst = s.split('dst: ')
   xhtml_file = lst[-1]
   return xhtml_file

def extract_values(dm):
   lst = []
   l = get_elms_for_atr_val('table')
   
   # ............
   for i in l:
   		lst.append(get_text(i))
   
   # ............
   return lst

# mysql> describe most_active;
def insert_to_db(l,tbl):
	conn=MySQLdb.connect (host="localhost",db="stock_market",user='root',passwd='')
	cursor = conn.cursor()
	s='create table '+tbl+' (symbol varchar(10),name varchar(80),price float,chng float,pchng float,volum int	);'
	
	rslt=cursor.execute(s)
	
	for x in l:
		s="insert into "+tbl+" (symbol,name,price,chng,pchng,volum) values ('"+x[0]+"','"+x[1]+"','"+x[3][1:]+"','"+x[4]+"','"+x[5]+"','"+x[2].replace(",",'')+"');"
		rslt=cursor.execute(s)
		
	
# to save our data, commit. 
	conn.commit()
   
	return cursor

def main():
	html_fn = sys.argv[1]
   	fn = html_fn.replace('.html','')
   	xhtml_fn = html_to_xml(html_fn)
 
   	global dom
   	dom = parse(xhtml_fn)
   	lst = extract_values(dom)
  	cursor = insert_to_db(lst,fn) 
  	
   	return 


if __name__ == "__main__":
    main()


