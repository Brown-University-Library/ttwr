# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseServerError
from django.template import Context, loader, RequestContext
from django.core.paginator import Paginator
import urllib, urllib2
import json
import logging
logger = logging.getLogger(__name__)
from operator import itemgetter
import xml.etree.ElementTree as ET
import re # regular expressions
# from rome_app import settings_app
from models import About
import requests

# from rome_app import models
# from models import AboutPage

# git push https://ben_leveque@bitbucket.org/birkin/projects-rome_app.git
# update with efficiency fixes

BDR_SERVER = u'repository.library.brown.edu'

def std_context(style="rome/css/prints.css",title="The Theater that was Rome"):
	context={}
	context['usr_style']=style
	context['title']=title
	context['cpydate']=2013
	context['home_image']="rome/images/home.gif"
	context['brown_image']="rome/images/brown-logo.gif"
	context['stg_image']="rome/images/stg-logo.gif"
	return context

def index(request):
	template=loader.get_template('rome_templates/index.html') #built-in from django.template
	context=std_context(style="rome/css/home.css")
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def books(request,page=1,sort_by='authors'):
	template=loader.get_template('rome_templates/books.html')
	context=std_context()
	context['curr_page']=page
	context['page_documentation']='Click on "View" to see thumbnails of all the pages of a book. Click "BDR View" to see the default repository entry for a book.'
	context['sorting']='authors'
	if sort_by!='authors':
		context['sorting']=sort_by
	# load json for all books in the collection #
	num_books_estimate=6000 #should be plenty
	url1='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=object_type:implicit-set&fl=*&fq=discover:BDR_PUBLIC&rows='+str(num_books_estimate)
	books_json=json.loads(urllib2.urlopen(url1).read())
	num_books=books_json['items']['numFound']
	context['num_books']=num_books
	if num_books>num_books_estimate: #only reload if we need to find more books
		url2='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=object_type:implicit-set&fl=*&fq=discover:BDR_PUBLIC&rows='+str(num_books)
		books_json=json.loads(urllib2.urlopen(url2).read())
	books_set=books_json['items']['docs']
	book_list=[]

	# create list of books with information to display for each #
	for i in range(num_books):
		current_book={}
		book=books_set[i]
		title=book['primary_title'] #"<br />".join(book['primary_title'].split("\n"))
		pid=book['pid']
		current_book['pid']=book['pid'].split(":")[1]
		current_book['thumbnail_url_start']="../book_"+str(current_book['pid'])
		current_book['studio_uri']=book['uri']
		short_title=title
		current_book['title_cut']=0
		cutoff=80
		if len(title)>cutoff:
			short_title=title[0:cutoff-3]+"..."
			current_book['title_cut']=1
		current_book['title']=title
		current_book['short_title']=short_title
		# current_book['port_url']='https://repository.library.brown.edu/services/book_reader/portfolio/'+pid
		# current_book['book_url']='https://repository.library.brown.edu/services/book_reader/set/'+pid
		current_book['port_url']='https://repository.library.brown.edu/viewers/readers/portfolio/'+pid
		current_book['book_url']='https://repository.library.brown.edu/viewers/readers/set/'+pid
		try:
			current_book['date']=book['dateCreated'][0:4]
		except:
			try:
				current_book['date']=book['dateIssued'][0:4]
			except:
				current_book['date']="n.d."
		try:
			author_list=book['contributor_display']
			authors=""
			for i in range(len(author_list)):
				if i==len(author_list)-1:
					authors+=author_list[i]
				else:
					authors+=author_list[i]+"; "
			current_book['authors']=authors
		except:
			current_book['authors']="contributor(s) not available"
		book_list.append(current_book)
	book_list=sorted(book_list,key=itemgetter(sort_by,'authors','title','date')) # sort alphabetically
	for i, book in enumerate(book_list):
		book['number_in_list']=i+1
	context['book_list']=book_list

	# pagination #
	books_per_page=20
	context['books_per_page']=books_per_page
	PAGIN=Paginator(book_list,books_per_page);
	context['num_pages']=PAGIN.num_pages
	context['page_range']=PAGIN.page_range
	context['PAGIN']=PAGIN
	page_list=[]
	for i in PAGIN.page_range:
		page_list.append(PAGIN.page(i).object_list)
	context['page_list']=page_list

	# send to template #
	c=RequestContext(request,context)
	return HttpResponse(template.render(c))

def thumbnail_viewer(request, book_pid, page_num, book_num_on_page):
	template=loader.get_template('rome_templates/thumbnail_viewer.html')
	context=std_context()
	context['back_to_book_href']="../books_"+str(page_num)+"#"+str(page_num)+"_"+str(book_num_on_page)
	context['page_documentation']='Browse through the pages in this book. Click on an image to explore the page further.'
	context['pid']=book_pid
	thumbnails=[]
	json_uri='https://repository.library.brown.edu/api/pub/items/bdr:'+str(book_pid)+'/?q=*&fl=*'
	book_json=json.loads(urllib2.urlopen(json_uri).read())
	context['short_title']=book_json['brief']['title']
	context['title']=book_json['primary_title']
	try:
		author_list=book_json['contributor_display']
		authors=""
		for i in range(len(author_list)):
			if i==len(author_list)-1:
				authors+=author_list[i]
			else:
				authors+=author_list[i]+"; "
		context['authors']=authors
	except:
		context['authors']="contributor(s) not available"
	try:
		context['date']=book_json['dateIssued'][0:4]
	except:
		try:
			context['date']=book_json['dateCreated'][0:4]
		except:
			context['date']="n.d."
	pages=book_json['relations']['hasPart']
	for page in pages:
		curr_thumb={}
		curr_thumb['src']="https://repository.library.brown.edu/fedora/objects/"+page['pid']+"/datastreams/thumbnail/content"
		curr_thumb['det_img_view']="https://repository.library.brown.edu/viewers/image/zoom/bdr:"+page['pid']+"/"
		# page_url="https://repository.library.brown.edu/api/pub/items/"+page['pid']
		# page_json=json.loads(urllib2.urlopen(page_url).read())
		# 		annotations=page_json['relations']['hasAnnotation']
		# 		curr_thumb['has_metadata']=0
		# 		if len(annotations):
		# 			curr_thumb['has_metadata']=1
		
		curr_pid=page['pid'].split(":")[1]
		curr_thumb['page_view']="../page_"+str(book_pid)+"_"+str(curr_pid)+"_"+str(page_num)+"_"+str(book_num_on_page)
		thumbnails.append(curr_thumb)
	context['thumbnails']=thumbnails
	
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def page(request, book_pid, page_pid, page_num, book_num_on_page):
	#note: page_pid does not include 'bdr:'
	template=loader.get_template('rome_templates/page.html')
	context=std_context()

	context['book_mode']=1
	context['print_mode']=0

	context['back_to_book_href']="../books_"+str(page_num)+"#"+str(page_num)+"_"+str(book_num_on_page)
	context['back_to_thumbnail_href']="../book_"+str(book_pid)+"_"+str(page_num)+"_"+str(book_num_on_page)

	context['pid']=book_pid
	thumbnails=[]
	book_json_uri='https://repository.library.brown.edu/api/pub/items/bdr:'+str(book_pid)+'/?q=*&fl=*'
	#logger.error('json_uri = '+json_uri)
	book_json=json.loads(urllib2.urlopen(book_json_uri).read())
	context['short_title']=book_json['brief']['title']
	context['title']=book_json['primary_title']
	try:
		author_list=book_json['contributor_display']
		authors=""
		for i in range(len(author_list)):
			if i==len(author_list)-1:
				authors+=author_list[i]
			else:
				authors+=author_list[i]+"; "
		context['authors']=authors
	except:
		context['authors']="contributor(s) not available"
	try:
		context['date']=book_json['dateIssued'][0:4]
	except:
		try:
			context['date']=book_json['dateCreated'][0:4]
		except:
			context['date']="n.d."
	context['lowres_url']="https://repository.library.brown.edu/fedora/objects/bdr:"+str(page_pid)+"/datastreams/lowres/content"
	context['det_img_view_src']="https://repository.library.brown.edu/viewers/image/zoom/bdr:"+str(page_pid)

	page_json_uri='https://repository.library.brown.edu/api/pub/items/bdr:'+str(page_pid)+'/?q=*&fl=*'
	#logger.error('json_uri = '+json_uri)
	
	# annotations/metadata
	page_json=json.loads(urllib2.urlopen(page_json_uri).read())
	annotations=page_json['relations']['hasAnnotation']
	context['has_annotations']=len(annotations)
	context['annotation_uris']=[]
	context['annotations']=[]
	for i in range(len(annotations)):
		annot_pid=annotations[i]['pid']
		annot_studio_uri=annotations[i]['uri']
		annot_xml_uri='https://repository.library.brown.edu/fedora/objects/'+annot_pid+'/datastreams/content/content'
		context['annotation_uris'].append(annot_xml_uri)
		curr_annot={}
		curr_annot['xml_uri']=annot_xml_uri
		curr_annot['has_elements']={'inscriptions':0, 'annotations':0, 'annotator':0, 'origin':0, 'title':0, 'abstract':0}

		root=ET.fromstring(urllib2.urlopen(annot_xml_uri).read()) #root of our xml tree
		for title in root.getiterator('{http://www.loc.gov/mods/v3}titleInfo'):
			if title.attrib['lang']=='en':
				curr_annot['title']=title[0].text
				curr_annot['has_elements']['title']=1
				break
		curr_annot['names']=[]
		for name in root.getiterator('{http://www.loc.gov/mods/v3}name'):
			curr_annot['names'].append({
				'name':name[0].text,
				'role':name[1][0].text.capitalize(),
				'trp_id': name.attrib['{http://www.w3.org/1999/xlink}href'],
			})
		for abstract in root.getiterator('{http://www.loc.gov/mods/v3}abstract'):
			curr_annot['abstract']=abstract.text
			curr_annot['has_elements']['abstract']=1
		for origin in root.getiterator('{http://www.loc.gov/mods/v3}originInfo'):
			curr_annot['origin']=origin[0].text
			curr_annot['has_elements']['origin']=1
		curr_annot['notes']=[]
		curr_annot['inscriptions']=[]
		curr_annot['annotations']=[]
		curr_annot['annotator']=""
		for note in root.getiterator('{http://www.loc.gov/mods/v3}note'):
			curr_note={}
			for att in note.attrib:
				curr_note[att]=note.attrib[att]
			if note.text:
				curr_note['text']=note.text
			if curr_note['type'].lower()=='inscription' and note.text:
				curr_annot['inscriptions'].append(curr_note['displayLabel']+": "+curr_note['text'])
				curr_annot['has_elements']['inscriptions']=1
			elif curr_note['type'].lower()=='annotation' and note.text:
				curr_annot['annotations'].append(curr_note['displayLabel']+": "+curr_note['text'])
				curr_annot['has_elements']['annotations']=1
			elif curr_note['type'].lower()=='resp' and note.text:
				curr_annot['annotator']=note.text
				curr_annot['has_elements']['annotator']=1
			#curr_annot['notes'].append(curr_note)
		context['annotations'].append(curr_annot)
		
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def prints(request,page=1, sort_by="authors"):
	template=loader.get_template('rome_templates/prints.html')
	context=std_context(title="The Theater that was Rome - Prints")
	context['page_documentation']='Browse the prints in the Theater that was Rome collection. Click on "View" to explore a print further.'
	context['curr_page']=page
	context['sorting']='authors'
	if sort_by!='authors':
		context['sorting']=sort_by
	# url1='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=genre_aat:*prints*&fl=*'
	# url1='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=genre_aat:*(prints)&fl=*&fq=discover:BDR_PUBLIC';
	# num_prints=json.loads(urllib2.urlopen(url1).read())['items']['numFound']
	# load json for all prints in the collection #
	num_prints_estimate=6000
	url1='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=genre_aat:*prints*&fl=*&fq=discover:BDR_PUBLIC&rows='+str(num_prints_estimate)
	prints_json=json.loads(urllib2.urlopen(url1).read())
	num_prints=prints_json['items']['numFound']
	context['num_prints']=num_prints
	if num_prints>num_prints_estimate:
		url2='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=genre_aat:*prints*&fl=*&fq=discover:BDR_PUBLIC&rows='+str(num_prints)
		prints_json=json.loads(urllib2.urlopen(url2).read())
	
	# context['num_prints']=num_prints
	# 	url2=url1+'&rows='+str(num_prints)
	# 
	# 	prints_json=json.loads(urllib2.urlopen(url2).read())
	prints_set=prints_json['items']['docs']

	print_list=[]
	for i in range(len(prints_set)): #create list of prints to load
		current_print={}
		Print=prints_set[i]
		title=Print['primary_title'] #"<br />".join(Print['primary_title'].split("\n"))
		current_print['in_chinea']=0
		if re.search(r"chinea",title,re.IGNORECASE):
			current_print['in_chinea']=1
		pid=Print['pid']
		current_print['studio_uri']=Print['uri']
		short_title=title
		current_print['title_cut']=0
		current_print['thumbnail_url_start']="../sprint_"+pid.split(":")[1]
		if len(title)>60:
			short_title=title[0:57]+"..."
			current_print['title_cut']=1
		current_print['title']=title
		current_print['short_title']=short_title
		#print_json=json.loads(urllib2.urlopen(Print['json_uri']).read())
		current_print['det_img_viewer']='https://repository.library.brown.edu/viewers/image/zoom/bdr:'+str(pid)
		#print_json['links']['views']['Detailed Image Viewer']
		try:
			current_print['date']=Print['dateCreated'][0:4]
		except:
			try:
				current_print['date']=Print['dateIssued'][0:4]
			except:
				current_print['date']="n.d."
		try:
			author_list=Print['contributor_display']
		except KeyError:
			author_list=Print['contributor']
		authors=""
		for i in range(len(author_list)):
			if i==len(author_list)-1:
				authors+=author_list[i]
			else:
				authors+=author_list[i]+"; "
		current_print['authors']=authors
		current_print['pid']=pid.split(":")[1]
		print_list.append(current_print)

	
	print_list=sorted(print_list,key=itemgetter(sort_by,'authors','title','date'))
	for i, Print in enumerate(print_list):
		Print['number_in_list']=i+1
	context['print_list']=print_list

	prints_per_page=20
	context['prints_per_page']=prints_per_page
	PAGIN=Paginator(print_list,prints_per_page) #20 prints per page
	context['num_pages']=PAGIN.num_pages
	context['page_range']=PAGIN.page_range
	context['PAGIN']=PAGIN
	page_list=[]
	for i in PAGIN.page_range:
		page_list.append(PAGIN.page(i).object_list)
	context['page_list']=page_list

	c=RequestContext(request,context)
	return HttpResponse(template.render(c))

def specific_print(request, print_pid, page_num, print_num_on_page):
	template=loader.get_template('rome_templates/page.html')
	context=std_context()

	context['book_mode']=0
	context['print_mode']=1
	context['det_img_view_src']='https://repository.library.brown.edu/viewers/image/zoom/bdr:'+str(print_pid)#'https://repository.library.brown.edu/viewer/highres_viewer.html?pid=bdr:'+str(print_pid)+'&ds=highres_jp2'
	context['back_to_print_href']="../prints_"+str(page_num)+"#"+str(page_num)+"_"+str(print_num_on_page)

	context['pid']=print_pid

	json_uri='https://repository.library.brown.edu/api/pub/items/bdr:'+str(print_pid)+'/?q=*&fl=*'
	#logger.error('json_uri = '+json_uri)
	print_json=json.loads(urllib2.urlopen(json_uri).read())
	context['short_title']=print_json['brief']['title']
	context['title']=print_json['primary_title']
	try:
		author_list=print_json['contributor_display']
		authors=""
		for i in range(len(author_list)):
			if i==len(author_list)-1:
				authors+=author_list[i]
			else:
				authors+=author_list[i]+"; "
		context['authors']=authors
	except:
		context['authors']="contributor(s) not available"
	try:
		context['date']=print_json['dateIssued'][0:4]
	except:
		try:
			context['date']=print_json['dateCreated'][0:4]
		except:
			context['date']="n.d."
			
	
	# annotations/metadata
	annotations=print_json['relations']['hasAnnotation']
	context['has_annotations']=len(annotations)
	context['annotation_uris']=[]
	context['annotations']=[]
	for i in range(len(annotations)):
		annot_pid=annotations[i]['pid']
		annot_studio_uri=annotations[i]['uri']
		annot_xml_uri='https://repository.library.brown.edu/fedora/objects/'+annot_pid+'/datastreams/content/content'
		context['annotation_uris'].append(annot_xml_uri)
		curr_annot={}
		curr_annot['xml_uri']=annot_xml_uri

		root=ET.fromstring(urllib2.urlopen(annot_xml_uri).read()) #root of our xml tree
		for title in root.getiterator('{http://www.loc.gov/mods/v3}titleInfo'):
			if title.attrib['lang']=='en':
				curr_annot['title']=title[0].text
				break
		curr_annot['names']=[]
		for name in root.getiterator('{http://www.loc.gov/mods/v3}name'):
			curr_annot['names'].append({'name':name[0].text, 'role':name[1][0].text})
		for abstract in root.getiterator('{http://www.loc.gov/mods/v3}abstract'):
			curr_annot['abstract']=abstract.text
		for origin in root.getiterator('{http://www.loc.gov/mods/v3}originInfo'):
			curr_annot['origin']=origin[0].text
		curr_annot['notes']=[]
		for note in root.getiterator('{http://www.loc.gov/mods/v3}note'):
			curr_note=[]
			for att in note.attrib:
				curr_note.append(att+": "+note.attrib[att])
			if note.text:
				curr_note.append("text: "+note.text)
			curr_annot['notes'].append(curr_note)
		context['annotations'].append(curr_annot)
	

	c=RequestContext(request,context)
	#raise 404 if a certain print does not exist
	return HttpResponse(template.render(c))

def get_bio_list( bio_set):
	bio_list=[]
	for i in range(len(bio_set)):
		bio=bio_set[i]
		current_bio={}
		display=bio['contributor_display'][0]
		parts=display.split("(")
		if len(parts)>1:
			current_bio['role']=' ['+parts[1].split(')')[0]+']'
		else:
			current_bio['role']=''
		potentialDate = parts[0].split(',')[-1]
		if re.search('[0-9][0-9][0-9]',potentialDate):
			current_bio['date']=' '+potentialDate
		else:
			current_bio['date']=''
		current_bio['name']=bio['primary_title'].split(': ')[1]+'.';
		current_bio['pid']=bio['pid'].split(":")[1]
		current_bio['uri']='https://repository.library.brown.edu/studio/item/'+bio['pid']+'/'
                current_bio['trp_id'] = bio['mods_id_trp_ssim'][0][4:]
		
		bio_list.append(current_bio)

	bio_list=sorted(bio_list,key=itemgetter('name'))
	for i, bio in enumerate(bio_list):
		bio['number_in_list']=i+1
	return bio_list

def person_detail(request, trp_id):
    (pid, name) = _get_info_from_trp_id(trp_id)
    if not pid:
        return HttpResponseServerError('Internal Server error')
    context = std_context(title="The Theater that was Rome - Biography")
    context = RequestContext(request, context)
    template = loader.get_template('rome_templates/person_detail.html')
    context['pid'] = pid
    context['trp_id'] = trp_id
    context['books'] = _books_for_person(name)
    context['prints'] = _prints_for_person(name)
    return HttpResponse(template.render(context))


def person_detail_tei(request, trp_id):
    pid, name = _get_info_from_trp_id(trp_id)
    if not pid:
        return HttpResponseServerError('Internal Server error')
    r = requests.get(u'https://%s/fedora/objects/%s/datastreams/TEI/content' % (BDR_SERVER, pid))
    if r.ok:
        return HttpResponse(r.text)


def _get_info_from_trp_id(trp_id):
    trp_id = u'trp-%s' % trp_id
    r = requests.get(u'http://%s/api/pub/search?q=mods_id_trp_ssim:%s+AND+display:BDR_PUBLIC&fl=pid,name' % (BDR_SERVER, trp_id))
    if r.ok:
        data = json.loads(r.text)
        if data['response']['numFound'] > 0:
            return (data['response']['docs'][0]['pid'], data['response']['docs'][0]['name'])


def _books_for_person(name):
    num_books_estimate = 6000
    query_uri = 'https://%s/api/pub/collections/621/?q=object_type:implicit-set+AND+name:"%s"&rows=%s' % (BDR_SERVER, name[0], num_books_estimate)
    books_json = json.loads(requests.get(query_uri).text)
    books_set = books_json['items']['docs']
    return books_set


def _prints_for_person(name):
    num_prints_estimate = 6000
    query_uri = 'https://%s/api/pub/collections/621/?q=genre_aat:*prints*+AND+name:"%s"&rows=%s' % (BDR_SERVER, name[0], num_prints_estimate)
    prints_json = json.loads(requests.get(query_uri).text)
    prints_set = prints_json['items']['docs']
    return prints_set


def people(request):
	template=loader.get_template('rome_templates/people.html')
	num_bios_estimate=6000
	url1='https://repository.library.brown.edu/api/pub/search/?q=ir_collection_id:621+AND+object_type:tei+AND+display:BDR_PUBLIC&rows='+str(num_bios_estimate)
	bios_json=json.loads(urllib2.urlopen(url1).read())
	
	num_bios=bios_json['response']['numFound']
	if num_bios>num_bios_estimate:
		url2='https://repository.library.brown.edu/api/pub/search/?q=ir_collection_id:621+AND+object_type:tei+AND+display:BDR_PUBLIC&rows='+str(num_bios)
		bios_json=json.loads(urllib2.urlopen(url2).read())

	bio_set=bios_json['response']['docs']
	bio_list = get_bio_list(bio_set)

	bios_per_page=20
	PAGIN=Paginator(bio_list,bios_per_page)
	page_list=[]
	for i in PAGIN.page_range:
		page_list.append(PAGIN.page(i).object_list)
	context=std_context(title="The Theater that was Rome - Biographies")
	context['page_documentation']='Browse the biographies of artists related to the Theater that was Rome collection.'
	context['num_bios']=num_bios
	context['bio_list']=bio_list
	context['bios_per_page']=bios_per_page
	context['num_pages']=PAGIN.num_pages
	context['page_range']=PAGIN.page_range
	context['curr_page']=1
	context['PAGIN']=PAGIN
	context['page_list']=page_list

	c=RequestContext(request,context)
	return HttpResponse(template.render(c))

def about(request):
	template=loader.get_template('rome_templates/about.html')
	context=std_context(style="rome/css/links.css")
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))	

def links(request):
	template=loader.get_template('rome_templates/links.html')
	context=std_context(style="rome/css/links.css")

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))	

def essays(request):
	template=loader.get_template('rome_templates/essays.html')
	context=std_context(style="rome/css/links.css")
	context['page_documentation']='Listed below are essays on topics that relate to the Theater that was Rome collection of books and engravings. The majority of the essays were written by students in Brown University classes that used this material, and edited by Prof. Evelyn Lincoln.'
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def specific_essay(request, essay_auth):
	template=loader.get_template('rome_templates/essays/book-essay-'+essay_auth+'.html')
	context=std_context(style="rome/css/links.css")
	context['usr_essays_style']="rome/css/essays.css"
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def stub(request):
    return HttpResponse( u'still under construction' )
