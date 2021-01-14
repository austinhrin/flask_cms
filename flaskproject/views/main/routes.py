# dependancies
from flask import Flask, render_template, Markup, request, escape, make_response, session, send_from_directory

# local
from flaskproject.views import main
from flaskproject.analytics import *
from settings import *
#from flaskproject.models import User, Post


def get_folder(website, path):
    # default to domain as website folder
    folder = './websites/' + request.host + '/'
    # check and override if folder is specified
    for site in websites:
        if site['domain'] == website and 'folder' in site:
            folder = './websites/' + site['folder'] + '/'
            break
    if path != None and path != 'None':
        folder += path + '/'
    return folder


def split_url(path):
    parts_of_path = path.split('/')
    # get the file
    requested_file = parts_of_path[len(parts_of_path)-1]
    # get everything but the requested file
    parts_of_path.remove(requested_file)
    folder = '/'.join(parts_of_path)
    return [folder, requested_file]


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    # dont allow bad referers
    if any(referer.lower() in str(request.referrer).lower() for referer in bad_referers) == True:
        return json.dumps({'error': 'The webpage refering you was black listed. If you wish to visit this website please do so by visting the website directly instead of clicking a link from an outside source.'}), 401

    # make sure there are no "bad" user agents
    if any(bad_user_agent.lower() in str(request.user_agent).lower() for bad_user_agent in bad_user_agents) == True:
        return json.dumps({'error': 'The user agent your web browser is using has been blacklisted due to spam'}), 401

    # dont allow bad things in url
    if any(part.lower() in str(request.url).lower() for part in not_allowed_in_url) == True:
        return json.dumps({'error': 'We have found blacklisted text in your url please remove it to visit this website.'}), 401

    # dont allow blank user agents
    if "".join(str(request.user_agent).split()) == '':
        return json.dumps({'error': 'The user agent your web browser is using is blank. We have found users that are using blank user agents are spam. Please visit this website with a user agent that is not blank.'}), 401

    # check if the requesting host is in the list of website domains
    if any(site['domain'] == request.host for site in websites):
        # if no path or path is / go to index.html
        if path == '' or path == '/':
            requested_file = 'index.html'
        else:
            requested_file = split_url(path)[1]

        folder = get_folder(request.host, split_url(path)[0])
        # check if .html is in requested file name
        # and if not 127.0.0.1:5000
        # dont track certian user agents
        if '.html' in requested_file and request.host != '127.0.0.1:5000' and any(user_agent.lower() in str(request.user_agent).lower() for user_agent in dont_track) == False:
            return set_cookie(send_from_directory(folder, requested_file))
        else:
            return send_from_directory(folder, requested_file)
    else:
        # prevent people visiting the ip or spoofing the domain
        # from visiting the websites
        return json.dumps({'error': 'Why are you here?'}), 401


@main.route("/viewanalytics")
def view_analytics():
    visits_by_ip = 'Number of unique ips: ' + str(get_total_num_unique_ips(0)) + '<br>\nNumber of unique ips in the last 24 hours: ' + str(get_total_num_unique_ips(
        1)) + '<br>\nNumber of unique ips in the last week: ' + str(get_total_num_unique_ips(7)) + '<br>\n'

    visits_by_cookie = 'Number of unique cookies: ' + str(get_total_num_unique_cookies(0)) + '<br>\nNumber of unique cookies in the last 24 hours: ' + str(get_total_num_unique_cookies(
        1)) + '<br>\nNumber of unique cookies in the last week: ' + str(get_total_num_unique_cookies(7)) + '<br>\n'

    unique_ips = get_unique_ip_addresses(1)
    unique_ips_html = ''
    for tuple in unique_ips:
        unique_ips_html += str(tuple[0]) + '<br>'

    unique_urls = get_unique_urls(1)
    unique_urls_html = ''
    for tuple in unique_urls:
        unique_urls_html += str(tuple[0]) + ' Total: ' + str(tuple[1]) + '<br>'

    unique_user_agents = get_unique_user_agents(1)
    unique_user_agents_html = ''
    for tuple in unique_user_agents:
        unique_user_agents_html += str(tuple[0]) + \
            ' Total: ' + str(tuple[1]) + '<br>'

    unique_referers = get_unique_referers(1)
    unique_referers_html = ''
    for tuple in unique_referers:
        unique_referers_html += str(tuple[0]) + \
            ' Total: ' + str(tuple[1]) + '<br>'

    html = visits_by_ip + '<br>\n' + \
        visits_by_cookie + "<br>\n" + \
        get_unique_cookies_chart_data() + '<br>\n' + \
        '<h3>Unique IP addresses in the last day:</h3>' + \
        str(unique_ips_html) + \
        '<h3>Unique URLs in the last day:</h3>' + \
        str(unique_urls_html) + \
        '<h3>Unique user agents in the last day:</h3>' + \
        str(unique_user_agents_html) + \
        '<h3>Unique Referers in the last day:</h3>' + \
        str(unique_referers_html)

    return html
