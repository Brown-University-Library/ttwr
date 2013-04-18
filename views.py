# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.core.paginator import Paginator
import urllib, urllib2
import json
import logging
logger = logging.getLogger(__name__)
from operator import itemgetter

def stub( request ):
    return HttpResponse( u'under construction' )

def std_context(style="css/prints.css",title="The Theater that was Rome"):
	context={}
	context['usr_style']=style
	context['title']=title
	context['cpydate']=2007
	context['home_image']="images/home.gif"
	context['brown_image']="images/brown-logo.gif"
	context['stg_image']="imagse/stg-logo.gif"
	return context

def index(request):
	template=loader.get_template('index.html') #built-in from django.template
	context=std_context(style="css/home.css")
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def search(request):
	template=loader.get_template('search.html')
	context=std_context()

	# if args and length(args)>0:
	# 		logger.error("got args")
	# 		context['got_args']=1
	# 	else:
	# 		context['got_args']=0

	# if request.method=='POST':
	# 		form=SearchForm(request.POST)
	# 		if form.is_valid():
	# 			data=form.cleaned_data
	# 			q=urllib.urlencode({'q':data['query']})
	# 			logger.error('form data submitted: '+q)
	# 			return HttpResponseRedirect(reverse('search',args=[data['query']])
	# 	else:
	# 		form=SearchForm()
	# 	context['form']=form
	# 	
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def search_results(request, query):
	logger.error("in search_results, query = "+query)



def books(request,page=1):
	logger.error('in books!')
	template=loader.get_template('books.html')
	context=std_context()
	context['curr_page']=page

	url1='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=object_type:implicit-set&fl=*&fq=discover:BDR_PUBLIC'#'&rows=100'
	num_books=json.loads(urllib2.urlopen(url1).read())['items']['numFound']
	context['num_books']=num_books
	url2='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=object_type:implicit-set&fl=*&fq=discover:BDR_PUBLIC&rows='+str(num_books)
	books_json=json.loads(urllib2.urlopen(url2).read())
	#context['books_json']=books_json
	books_set=books_json['items']['docs']
	book_list=[]
	pview_list=[]
	bview_list=[]
	quick_and_wrong=1
	for i in range(len(books_set)): #create list of books to load
		current_book={}#[] #title, contributors, date
		book=books_set[i]
		title="<br />".join(book['primary_title'].split("\n"))
		pid=book['pid']
		current_book['pid']=book['pid'].split(":")[1]
		current_book['thumbnail_url_start']="../book_"+str(current_book['pid'])
		current_book['studio_uri']=book['uri']
		short_title=title
		current_book['title_cut']=0
		if len(title)>60:
			short_title=title[0:57]+"..."
			current_book['title_cut']=1
		current_book['title']=title#.append(title)
		current_book['short_title']=short_title#.append(backup_title)
		if quick_and_wrong:
			current_book['port_url']='https://repository.library.brown.edu/services/book_reader/portfolio/'+pid+'/highres_jp2/'
			#current_book['port_url']="https://repository.library.brown.edu/services/book_reader/portfolio/"+pid+"/JP2/"
			current_book['book_url']='https://repository.library.brown.edu/services/book_reader/set/'+pid+'/highres_jp2/'
			#"https://repository.library.brown.edu/services/book_reader/set/"+pid+"/JP2/"
			try:
				current_book['date']=book['dateCreated'][0].split("T")[0]
			except:
				try:
					current_book['date']=book['dateIssued'][0].split("T")[0]
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
				current_book['authors']="not available"

		else:
			book_json=json.loads(urllib2.urlopen(book['json_uri']).read())
			try:
				current_book['port_url']=book_json['links']['views']['Portfolio View']
			except:
				current_book['port_url']=""
			try:
				current_book['book_url']=book_json['links']['views']['Book View']
			except:
				current_book['book_url']=""
			try:
				current_book['date']=book_json['dateIssued'][0].split("T")[0]
			except:
				try:
					current_book['date']=book_json['dateCreated'][0].split("T")[0]
				except:
					current_book['date']="n.d."
			try:
				author_list=book_json['contributor_display']
				authors=""
				for i in range(len(author_list)):
					if i==len(author_list)-1:
						authors+=author_list[i]
					else:
						authors+=author_list[i]+"; "
				current_book['authors']=authors
			except:
				current_book['authors']="not available"
		book_list.append(current_book)

	book_list=sorted(book_list,key=itemgetter('authors'))
	context['book_list']=book_list

	books_per_page=20
	context['books_per_page']=books_per_page
	PAGIN=Paginator(book_list,books_per_page); #20 prints per page
	context['num_pages']=PAGIN.num_pages
	context['page_range']=PAGIN.page_range
	context['PAGIN']=PAGIN
	page_list=[]
	for i in PAGIN.page_range:
		page_list.append(PAGIN.page(i).object_list)
	context['page_list']=page_list

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def thumbnail_viewer(request, book_pid, page_num, book_num_on_page):
	template=loader.get_template('thumbnail_viewer.html')
	context=std_context()

	context['back_to_book_href']="../books_"+str(page_num)+"#"+str(page_num)+"_"+str(book_num_on_page)

	context['pid']=book_pid
	thumbnails=[]
	json_uri='https://repository.library.brown.edu/api/pub/items/bdr:'+str(book_pid)+'/?q=*&fl=*'
	logger.error('json_uri = '+json_uri)
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
		context['authors']="not available"
	try:
		context['date']=book_json['dateIssued'][0].split("T")[0]
	except:
		try:
			context['date']=book_json['dateCreated'][0].split("T")[0]
		except:
			context['date']="n.d."
	pages=book_json['relations']['hasPart']
	for page in pages:
		curr_thumb={}
		curr_thumb['src']="https://repository.library.brown.edu/fedora/objects/"+page['pid']+"/datastreams/thumbnail/content"
		curr_thumb['det_img_view']="https://repository.library.brown.edu/viewer/highres_viewer.html?pid="+page['pid']+"&ds=highres_jp2"
		curr_pid=page['pid'].split(":")[1]
		curr_thumb['page_view']="../page_"+str(book_pid)+"_"+str(curr_pid)+"_"+str(page_num)+"_"+str(book_num_on_page)
		thumbnails.append(curr_thumb)
	context['thumbnails']=thumbnails
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def page(request, book_pid, page_pid, page_num, book_num_on_page):
	#note: page_pid does not include 'bdr:'
	template=loader.get_template('page.html')
	context=std_context()

	context['book_mode']=1
	context['print_mode']=0

	context['back_to_book_href']="../books_"+str(page_num)+"#"+str(page_num)+"_"+str(book_num_on_page)
	context['back_to_thumbnail_href']="../book_"+str(book_pid)+"_"+str(page_num)+"_"+str(book_num_on_page)

	context['pid']=book_pid
	thumbnails=[]
	json_uri='https://repository.library.brown.edu/api/pub/items/bdr:'+str(book_pid)+'/?q=*&fl=*'
	logger.error('json_uri = '+json_uri)
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
		context['authors']="not available"
	try:
		context['date']=book_json['dateIssued'][0].split("T")[0]
	except:
		try:
			context['date']=book_json['dateCreated'][0].split("T")[0]
		except:
			context['date']="n.d."
	context['det_img_view_src']="http://repository.library.brown.edu/viewer/highres_viewer.html?pid=bdr:"+str(page_pid)+"&ds=highres_jp2"

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))


def prints(request,page=1):
	template=loader.get_template('prints.html')
	context=std_context(title="The Theater that was Rome - Prints")
	context['curr_page']=page

	# url1='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=genre_aat:*prints*&fl=*'
	url1='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=genre_aat:*(prints)&fl=*&fq=discover:BDR_PUBLIC';
	num_prints=json.loads(urllib2.urlopen(url1).read())['items']['numFound']
	context['num_prints']=num_prints
	url2=url1+'&rows='+str(num_prints)

	prints_json=json.loads(urllib2.urlopen(url2).read())
	prints_set=prints_json['items']['docs']

	print_list=[]
	for i in range(len(prints_set)): #create list of prints to load
		current_print={}
		Print=prints_set[i]
		title="<br />".join(Print['primary_title'].split("\n"))
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
		current_print['det_img_viewer']='https://repository.library.brown.edu/viewer/highres_viewer.html?pid='+str(pid)+'&ds=highres_jp2'
		#print_json['links']['views']['Detailed Image Viewer']
		try:
			current_print['date']=Print['dateCreated'][0].split("T")[0]
		except:
			try:
				current_print['date']=Print['dateIssued'][0].split("T")[0]
			except:
				current_print['date']="n.d."
		author_list=Print['contributor_display']
		authors=""
		for i in range(len(author_list)):
			if i==len(author_list)-1:
				authors+=author_list[i]
			else:
				authors+=author_list[i]+"; "
		current_print['authors']=authors
		print_list.append(current_print)

	print_list=sorted(print_list,key=itemgetter('authors'))
	context['print_list']=print_list

	prints_per_page=20
	context['prints_per_page']=prints_per_page
	PAGIN=Paginator(print_list,prints_per_page); #20 prints per page
	context['num_pages']=PAGIN.num_pages
	context['page_range']=PAGIN.page_range
	context['PAGIN']=PAGIN
	page_list=[]
	for i in PAGIN.page_range:
		page_list.append(PAGIN.page(i).object_list)
	context['page_list']=page_list
	# I=request.GET.get('page')
	# 	try:
	# 		curr_page=PAGIN.page(I)
	# 	except PageNotAnInteger:
	# 		curr_page=PAGIN.page(1)
	# 	except EmptyPage:
	# 		curr_page=PAGIN.page(PAGIN.num_pages)
	# 	context['curr_page']=curr_page	


	c=RequestContext(request,context)
	#raise 404 if a certain print does not exist
	return HttpResponse(template.render(c))

def specific_print(request, print_pid, page_num, print_num_on_page):
	template=loader.get_template('page.html')
	context=std_context()

	context['book_mode']=0
	context['print_mode']=1
	context['det_img_view_src']='https://repository.library.brown.edu/viewer/highres_viewer.html?pid=bdr:'+str(print_pid)+'&ds=highres_jp2'
	context['back_to_print_href']="../prints_"+str(page_num)+"#"+str(page_num)+"_"+str(print_num_on_page)

	context['pid']=print_pid

	json_uri='https://repository.library.brown.edu/api/pub/items/bdr:'+str(print_pid)+'/?q=*&fl=*'
	logger.error('json_uri = '+json_uri)
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
		context['authors']="not available"
	try:
		context['date']=print_json['dateIssued'][0].split("T")[0]
	except:
		try:
			context['date']=print_json['dateCreated'][0].split("T")[0]
		except:
			context['date']="n.d."

	c=RequestContext(request,context)
	#raise 404 if a certain print does not exist
	return HttpResponse(template.render(c))

def about(request):
	template=loader.get_template('about.html')
	context=std_context(style="css/links.css")

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))	

def links(request):
	template=loader.get_template('links.html')
	context=std_context(style="css/links.css")

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))	

def essays(request):
	template=loader.get_template('essays.html')
	context=std_context(style="css/links.css")
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def specific_essay(request, essay_auth):
	#a=urllib2.urlopen('./essays/book-essay-'+essay_auth+".html").read()
	template=loader.get_template('./essays/book-essay-'+essay_auth+'.html')
	context=std_context(style="css/links.css")
	context['usr_essays_style']="css/essays.css"
	context['txt_path']="essays/aldini.txt"
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))