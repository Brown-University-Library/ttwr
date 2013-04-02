# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.core.paginator import Paginator
import urllib2
import json
import logging
logger = logging.getLogger(__name__)

def stub( request ):
    return HttpResponse( u'under construction' )

def index(request):
	template=loader.get_template('books/index.html') #built-in from django.template
	context={}
	context['usr_style']="css/home.css"
	context['title']="The Theater that was Rome"
	context['cpydate']=2007
	context['home_image']="images/home.gif"
	context['brown_image']="images/brown-logo.gif"
	context['stg_image']="images/stg-logo.gif"
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def books(request):
	logger.error('in books!')
	template=loader.get_template('books/books.html')
	context={}
	context['usr_style']="css/prints.css"
	context['title']="The Theater that was Rome - Books"
	context['cpydate']=2007
	context['home_image']="images/home.gif"
	context['brown_image']="images/brown-logo.gif"
	context['stg_image']="images/stg-logo.gif"

	#books_text=BookPage.objects.create(books_text="hello! this is the book page");
	#context['books_text']=books_text

	# page1url='https://repository.library.brown.edu/bdr_apis/pub/items/bdr:240511/'
	# 	page1read=urllib2.urlopen(page1url).read()
	# 	page1json=json.loads(page1read)
	# 	page1viewer=page1json['links']['views']['Detailed Image Viewer'] #look at the image viewer for a particular page
	# 	context['page_example']=page1viewer
	# 	
	# 	book1url='https://repository.library.brown.edu/bdr_apis/pub/items/bdr:240510/'
	# 	book1read=urllib2.urlopen(book1url).read()
	# 	book1json=json.loads(book1read)
	# 	book1viewer=book1json['links']['views']['Portfolio View']
	# 	context['book_example']=book1viewer
	#
	#########################################

	url1='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=object_type:implicit-set'#'&rows=100'
	num_books=json.loads(urllib2.urlopen(url1).read())['items']['numFound']
	url2='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=object_type:implicit-set&rows='+str(num_books)
	books_json=json.loads(urllib2.urlopen(url2).read())
	#context['books_json']=books_json
	books_set=books_json['items']['docs']
	book_list=[]
	pview_list=[]
	bview_list=[]
	quick_and_wrong=0
	for i in range(len(books_set)): #create list of books to load
		current_book={}#[] #title, contributors, date
		book=books_set[i]
		title="<br />".join(book['primary_title'].split("\n"))
		#title=book['primary_title']
		pid=book['pid']
		current_book['studio_uri']=book['uri']
		short_title=title
		current_book['title_cut']=0
		if len(title)>60:
			short_title=title[0:57]+"..."
			current_book['title_cut']=1
		current_book['title']=title#.append(title)
		current_book['short_title']=short_title#.append(backup_title)
		if quick_and_wrong:
			current_book['port_url']="https://repository.library.brown.edu/services/book_reader/portfolio/"+pid+"/JP2/"
			current_book['book_url']="https://repository.library.brown.edu/services/book_reader/set/"+pid+"/JP2/"
			current_book['date']="TBD"
			current_book['authors']="TBD"
			#current_book.append(port_url)
		else:
			book_json=json.loads(urllib2.urlopen(book['json_uri']).read())
			current_book['port_url']=book_json['links']['views']['Portfolio View']
			current_book['book_url']=book_json['links']['views']['Book View']
			try:
				current_book['date']=book_json['dateIssued'][0].split("T")[0]
			except:
				current_book['date']="n.d."
			author_list=book_json['contributor_display']
			authors=""
			for i in range(len(author_list)):
				if i==len(author_list)-1:
					authors+=author_list[i]
				else:
					authors+=author_list[i]+"; "
			current_book['authors']=authors


	# 		except:
	# 			current_book.append("unable to load")
	# 			current_book.append("unable to load")
	# 			current_book.append("#")
		book_list.append(current_book)

	context['book_list']=book_list


	#collection1read=urllib2.urlopen(collection1url).read()
	#collection1json=json.loads(collection1read)
	#collection1=collection1json['items']['docs']

	# booktitlelist=[]
	# 	bookviewerurllist=[]
	# 	for elt in collection1:
	# 		if elt['object_type']=='implicit-set':
	# 			booktitlelist.append("<br />".join(elt['primary_title'].split("\n")))
	# 			bkjson=json.loads(urllib2.urlopen(elt['json_uri']).read())
	# 			bookviewerurllist.append(bkjson['links']['views']['Portfolio View'])
	# 
	# 	context['rnge'] = range(len(booktitlelist))
	# 	context['num_books'] = len(booktitlelist)
	# 	context['collection_book_titles'] = booktitlelist
	# 	context['collection_book_viewers'] = bookviewerurllist

	context['woo']='wooo'
	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def specific_book(request, book_id):
    return HttpResponse("You're looking at book %s" % book_id)

def prints(request):
	template=loader.get_template('books/prints.html')
	context={}
	context['usr_style']="css/prints.css"
	context['title']="The Theater that was Rome - Prints"
	context['cpydate']=2007
	context['home_image']="images/home.gif"
	context['brown_image']="images/brown-logo.gif"
	context['stg_image']="images/stg-logo.gif"

	# prints_q='https://repository.library.brown.edu/bdr_apis/pub/collections/621/?q=object_type:image-compound&rows=100'
	# 	books_json=json.loads(urllib2.urlopen(prints_q).read())
	# 	books_set=books_json['items']['docs']
	# 	book_list=[]
	# 	pview_list=[]
	# 	bview_list=[]
	# 	
	# 	for i in range(len(books_set)): #create list of books to load
	# 		current_book=[]
	# 		book=books_set[i]
	# 		try:
	# 			title=book['primary_title']
	# 			backup_title=title
	# 			if len(title)>60:
	# 				backup_title=title[0:57]+"..."
	# 			current_book.append(title)
	# 			current_book.append(backup_title)
	# 			book_json=json.loads(urllib2.urlopen(book['json_uri']).read())
	# 			book_viewers=book_json['links']['views']
	# 			port_url=book_viewers['Portfolio View']
	# 			book_url=book_viewers['Book View']
	# 			current_book.append(port_url)
	# 			current_book.append(book_url)
	# 		except:
	# 			current_book.append("unable to load")
	# 			current_book.append("unable to load")
	# 			current_book.append("#")
	# 			current_book.append("#")
	# 		book_list.append(current_book)
	# 		
	# 	context['book_list']=book_list

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def about(request):
	template=loader.get_template('books/about.html')
	context={}
	context['usr_style']="css/links.css"
	context['title']="The Theater that was Rome - About"
	context['cpydate']=2007
	context['home_image']="images/home.gif"
	context['brown_image']="images/brown-logo.gif"
	context['stg_image']="images/stg-logo.gif"

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))	

def links(request):
	template=loader.get_template('books/links.html')
	context={}
	context['usr_style']="css/links.css"
	context['title']="The Theater that was Rome - Links"
	context['cpydate']=2007
	context['home_image']="images/home.gif"
	context['brown_image']="images/brown-logo.gif"
	context['stg_image']="images/stg-logo.gif"

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))	

def essays(request):
	template=loader.get_template('books/essays.html')
	context={}
	context['usr_style']="css/links.css"
	context['title']="The Theater that was Rome - Essays"
	context['cpydate']=2007
	context['home_image']="images/home.gif"
	context['brown_image']="images/brown-logo.gif"
	context['stg_image']="images/stg-logo.gif"

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))

def specific_essay(request, essay_auth):
	#a=urllib2.urlopen('./essays/book-essay-'+essay_auth+".html").read()
	template=loader.get_template('./essays/book-essay-'+essay_auth+'.html')
	context={}
	context['usr_style']="css/links.css"
	context['usr_essays_style']="css/essays.css"
	context['title']="The Theater that was Rome - Essays"
	context['cpydate']=2007
	context['home_image']="images/home.gif"
	context['brown_image']="images/brown-logo.gif"
	context['stg_image']="images/stg-logo.gif"
	context['txt_path']="essays/aldini.txt"
	#context['cont']=f.read()
	#r.close()

	#return HttpResponse("You're looking at book %s" % essay_auth)

	c=RequestContext(request,context)
	#raise 404 if a certain book does not exist
	return HttpResponse(template.render(c))