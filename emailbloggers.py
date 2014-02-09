import re
import mechanize
import sys
from bs4 import BeautifulSoup
import urllib2
import webbrowser
from urllib import urlencode
import csv
import smtplib
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import time

SMTPserver = 'smtp.gmail.com'
sender =     'xxx@gmail.com'
text_subtype = 'html'

USERNAME = "xxx@gmail.com"
PASSWORD = "xyz"

for i in range(0, 1000, 1):

    name = None
    last_name = None

    with open('handles.csv', 'rbU') as f:
        reader = csv.reader(f)
        list_of_handles = []
        for row in reader:
            list_of_handles.append(str(row[0]))

    twitter_handle = raw_input("Enter twitter handle: ")

    if twitter_handle in list_of_handles:
        print "\nYou have already contacted this person\n"
        break

    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.set_handle_refresh(False)

    my_url = "http://www.twitter.com/" + str(twitter_handle)
    html_body = mechanize.urlopen(my_url)
    html_body = BeautifulSoup(html_body)

    name = html_body.findAll('span', attrs={'class':'profile-field'})
    name = str(name[0])
    name = name.replace('<span class="profile-field">', '')
    name = name.replace('</span>', '')
    print name
    name = name.replace(' ', '+')
    name_plus_3d = "'" + name + "'" + "+fashion blog"

    try:
        href = html_body.findAll('a', attrs={'rel':'me nofollow'})
        blog_link = href[0]['title']
        who_is = "http://www.whois.com/whois/" + blog_link
    except:
        href="NA"

    google_url = "https://www.google.co.uk/search?q="+ name_plus_3d + "&oq=" + name_plus_3d + "&aqs=chrome..69i57j69i60j69i65l2j69i61j0.725j0&sourceid=chrome&ie=UTF-8"
    linkedin_search = "http://www.linkedin.com/vsearch/f?type=all&keywords=" + name + "&orig=GLHD&pageKey=member-home&search=Search"

    # webbrowser.open(google_url)
    # webbrowser.open(linkedin_search, new=1)

    if href != "NA":
        webbrowser.open(who_is, new=1)
        webbrowser.open(blog_link, new=1)

    webbrowser.open(my_url)

    # time.sleep(10)

    name = raw_input("Enter the person's FIRST NAME now. Else, type 'pass' if you couldn't find an email address:")

    if name != "pass":
        last_name = raw_input("Enter their SURNAME:")
        total_name = name + " " + last_name
        find_email_address = raw_input("Enter their EMAIL ADDRESS:")
        blog = raw_input("Does this person have a blog? y or n")
        if blog == "y":
            blog_name = raw_input("Enter Blog Name:")
        else:
            blog_name = ""
            profession = raw_input("Put in description of person, finish sentence: I saw that you were a ......")
        destination = [find_email_address]
        tracking_id = raw_input("Enter their URL TRACKING ID:")
        location = raw_input("Enter their LOCATION:")
        follower_count = raw_input("Enter number of Twitter Followers:")
        if blog == "y":
            content1="</br><p>My girlfriend really loves " + blog_name +". She told me that you would be perfect to message and ask whether the app I've started building is any good or not.The app is called, <a href='http://www.weaveuk.com/?U=" + tracking_id + "'> Weave Fashion</a>. It lets people quickly review what's &quot;New In&quot; at shops like Topshop, Zara, Anthropology &amp; Other Stories. </p><p>You can get version 1 of the app <a href='https://itunes.apple.com/gb/app/weave-fashion/id725215782?mt=8&ign-mpt=uo%3D4'>here</a>. I'd really love to know what you think, good or bad!  I'm trying to spend my evenings learning as much as I can about fashion so that I end up making something girls really love. If you fancy a chat instead my skype handle is Brownie3003. </p><p>Cheers,</p><p>Andy</p><p><img src='https://s3.amazonaws.com/uploads.hipchat.com/64166/445207/8M1YpXiLqwYFCZK/Andy.png'></p>"
        else:
            content1="</br><p>I saw that you were a " + profession + " and I'd really value your opinion on something. This is super random but basically my name is Andy, i'm a developer and i've just started making a fashion app, <a href='http://www.weaveuk.com/?U=" + tracking_id + "'> Weave Fashion</a>. The idea is it lets people quickly review what's &quot;New In&quot; at shops like Topshop, Zara, Anthropology &amp; Other Stories. I'd really love to know what you think, good or bad! </p><p>Version 1 is now in the app store. You can download it <a href='https://itunes.apple.com/gb/app/weave-fashion/id725215782?mt=8&ign-mpt=uo%3D4'>here</a>.  I'm trying to spend my evenings learning as much as I can about fashion at the moment so that I end up making something girls really love. If you fancy a chat instead my skype handle is Brownie3003. </p><p>Cheers,</p><p>Andy</p><p><img src='https://s3.amazonaws.com/uploads.hipchat.com/64166/445207/8M1YpXiLqwYFCZK/Andy.png'></p>"
        content2="<p><a href='http://www.weaveuk.com/?U=" + tracking_id + "'>www.weaveuk.com</a></p><p><a href='http://www.twitter.com/weaveuk'>@weaveuk</a></p>"
        email_content = "<p>Hi "+ name + ", </p>" + content1 + content2 + "<p><a href='https://itunes.apple.com/gb/app/weave-fashion/id725215782?mt=8&ign-mpt=uo%3D4'><img src='https://s3.amazonaws.com/uploads.hipchat.com/64166/445207/JZQY28KGUprCfMH/Screen+Shot+2013-10-23+at+12.25.53.png'></a></p>"
        msg = MIMEText(email_content, text_subtype)
        msg['Subject'] = "Hey"
        msg['From'] = sender
        msg['To'] = find_email_address
        conn = SMTP_SSL(SMTPserver, '465')
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
            writer = csv.writer(open("handles.csv", 'a'))
            twitter_handle = [twitter_handle, follower_count, blog_name, location, find_email_address, total_name, tracking_id]
            writer.writerow(twitter_handle)
            print "\n----------Email Sent-------------\n"
        finally:
            conn.close()
            
        name = None
