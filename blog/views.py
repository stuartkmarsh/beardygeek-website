from django.shortcuts import render_to_response
from django.template import RequestContext
from beardygeek.blog.models import Tag, Post, Category
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from xml.etree import ElementTree as ET

def index(request):
    return render_to_response('blog/index.html')

def importer(request):
    #create shortcuts for namespaces
    wp_ns = '{http://wordpress.org/export/1.0/}'
    content_ns = '{http://purl.org/rss/1.0/modules/content/}'
    
    #select a user to be used as author for the posts
    u = User.objects.get(username='admin')
    
    #get content type id for blog posts
    ct = ContentType.objects.get(model='post')
    
    #get site object, we'll assume there is only 1 site installed
    site = Site.objects.get(pk=1)
    
    tree = ET.parse('c:/wordpress.xml')
    chan = tree.find('channel')
    cats = chan.findall(wp_ns + 'category')
    tags = chan.findall(wp_ns + 'tag')
    items = chan.findall('item')
    
    #add categories
    for cat in cats:
        c = Category(text=cat.find(wp_ns + 'cat_name').text, slug=cat.find(wp_ns + 'category_nicename').text)
        c.save()
        
    #add tags
    for tag in tags:
        t = Tag(text=tag.find(wp_ns + 'tag_name').text, slug=tag.find(wp_ns + 'tag_slug').text)
        t.save()
        
    #add items
    for item in items:
        #find published items
        if item.find(wp_ns + 'status').text == 'publish' and item.find(wp_ns + 'post_type').text == 'post':
            i = Post(title=item.find('title').text, slug=item.find(wp_ns + 'post_name').text, 
                     content=item.find(content_ns + 'encoded').text, author=u, post_date=item.find(wp_ns + 'post_date').text,
                     status='P')
            i.save()
            #find all categories and tags for this post
            post_cats = item.findall('category')
            
            for pc in post_cats:
                #check for attributes
                if pc.get('nicename'):
                    if pc.attrib['domain'] == 'category':
                        c2 = Category.objects.get(slug=pc.attrib['nicename'])
                        i.categories.add(c2)
                    elif pc.attrib['domain'] == 'tag':
                        t2 = Tag.objects.get(slug=pc.attrib['nicename'])
                        i.tags.add(t2)
                        
            #find all comments for this post
            comments = item.findall(wp_ns + 'comment')
            
            for comm in comments:
                if not comm.find(wp_ns + 'comment_author_email').text:
                    comm_email = ''
                else:
                    comm_email = comm.find(wp_ns + 'comment_author_email').text
                    
                if not comm.find(wp_ns + 'comment_author_url').text:
                    comm_url = ''
                else:
                    comm_url = comm.find(wp_ns + 'comment_author_url').text
                    
                db_comm = Comment(comment=comm.find(wp_ns + 'comment_content').text, ip_address=comm.find(wp_ns + 'comment_author_IP').text,
                                  object_pk=i.id, submit_date=comm.find(wp_ns + 'comment_date').text,
                                  user_email=comm_email,
                                  user_name=comm.find(wp_ns + 'comment_author').text[:50],
                                  user_url=comm_url,
                                  content_type=ct, site=site)
                db_comm.save()
                        
    return render_to_response('blog/importer.html')

