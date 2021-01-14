from flask import request, make_response
import time
import datetime
import calendar
from user_agents import parse
import random
import string
import pymysql
import json
from ast import literal_eval

from secrets import secrets

sql_host = secrets['sql']['host']
sql_port = secrets['sql']['port']
sql_username = secrets['sql']['username']
sql_password = secrets['sql']['password']
sql_db = secrets['sql']['db']
sql_table = secrets['sql']['table']

# this function looks to see if the visitor has a cookie.
# if the visitor has a cookie it will return the webpage.
# if the visitor does not have a cookie it will make one and return the webpage.
# will call log_visit to log the visit of the visitor.


def set_cookie(html):
    cookie = request.cookies.get('x')
    domain = request.host
    # calulates epcohtime using utc time for consistency incase server and local time are different
    date_now = datetime.datetime.utcnow()
    epoch_time = str(round(calendar.timegm(date_now.timetuple())))
    if cookie != None:
        resp = html
    else:
        randomchars = ''.join(
            [random.choice(string.ascii_letters + string.digits) for n in range(32)])
        cookie = epoch_time + randomchars
        resp = make_response(html)
        resp.set_cookie("x", cookie, domain=domain, httponly=True)
    log_visit(cookie, epoch_time, domain)
    return resp


def log_visit(cookie, epoch_time, domain):
    if domain in request.url:
        db = pymysql.connect(host=sql_host, port=sql_port,
                             user=sql_username, passwd=sql_password, db=sql_db)
        c = db.cursor()
        # escape fields to prevent sql injection
        # note that when you use .escape it puts ' ' around the variable so ' ' is not required in the sql statement
        user_agent = db.escape(request.user_agent.string)
        referer = db.escape(request.headers.get("Referer"))
        url = db.escape(request.url)
        visitorip = request.remote_addr
        c.execute("INSERT INTO " + sql_table + " (USER_AGENT, REFERER, URL, IP, EPOCHTIME, COOKIE) VALUES(" + user_agent +
                  ", " + referer + ", " + url + ", '" + visitorip + "', '" + epoch_time + "', '" + cookie + "');")
        db.commit()
        db.close()
        message = 'Visit added to the database.'
    else:
        message = 'Site domain is not in the url. Not adding visit to the database.'
    return json.dumps({'message': message})


def return_epoch_time(num_days):
    # calulates epcohtime using utc time for consistency incase server and local time are different
    date_now = datetime.datetime.utcnow()
    epoch_time_now = calendar.timegm(date_now.timetuple())
    epoch_time_x_days_ago = str(round(epoch_time_now - num_days * 86400))
    return epoch_time_x_days_ago


def get_data_from_table(query):
    # get data from table and if num_days is not 0 then use it as a filter
    # return a list to the user
    db = pymysql.connect(host=sql_host, port=sql_port,
                         user=sql_username, passwd=sql_password, db=sql_db)
    c = db.cursor()
    sqlquery = query + ';'

    try:
        c.execute(sqlquery)
        data = c.fetchall()
    except:
        data = "Failed to gather data for your query."

    db.close()
    return str(data)


# Get the number of unique ip addresses.
# Call get_total_num_unique_ips(0) for all time unique visits by ip.
# Call get_total_num_unique_ips(1) to get unique number of ips for one visit.
def get_total_num_unique_ips(num_days):
    query = 'SELECT COUNT(DISTINCT IP) AS x FROM ' + sql_table
    if num_days != 0:
        query = query + ' WHERE EPOCHTIME > ' + \
            return_epoch_time(num_days)
    num_ips = get_data_from_table(query)
    return num_ips[2:-4]


# Get the number of unique visits by cookie.
# Call get_total_num_unique_cookies(0) for all time unique visits by cookies.
# Call get_total_num_unique_cookies(1) to get unique number cookies.
def get_total_num_unique_cookies(num_days):
    query = 'SELECT COUNT(DISTINCT COOKIE) AS x FROM ' + sql_table
    if num_days != 0:
        query = query + ' WHERE EPOCHTIME > ' + \
            return_epoch_time(num_days)
    num_cookies = get_data_from_table(query)
    return num_cookies[2:-4]


def listify(string):
    # strip unneeded ( and )
    string = string[1:-1]
    string = '[' + string + ']'
    string = literal_eval(string)
    return string


def get_unique_ip_addresses(num_days):
    # list unique ip addresses
    query = 'SELECT DISTINCT IP FROM ' + sql_table
    if num_days != 0:
        query = query + ' WHERE EPOCHTIME > ' + \
            return_epoch_time(num_days)
    list_of_ips = get_data_from_table(query)
    return listify(list_of_ips)


def get_unique_urls(num_days):
    # list unique ip addresses
    query = 'SELECT URL, COUNT(*) AS "#" FROM ' + \
        sql_table + ' GROUP BY URL ORDER BY 2'
    if num_days != 0:
        query = 'SELECT URL, COUNT(*) AS "#" FROM ' + sql_table + ' WHERE EPOCHTIME > ' + \
            return_epoch_time(num_days) + ' GROUP BY URL ORDER BY 2'
    list_of_urls = get_data_from_table(query)
    return listify(list_of_urls)


def get_unique_user_agents(num_days):
    # list unique ip addresses
    query = 'SELECT user_agent, COUNT(*) AS "#" FROM ' + \
        sql_table + ' GROUP BY user_agent ORDER BY 2'
    if num_days != 0:
        query = 'SELECT user_agent, COUNT(*) AS "#" FROM ' + sql_table + ' WHERE EPOCHTIME > ' + \
            return_epoch_time(num_days) + ' GROUP BY user_agent ORDER BY 2'
    list_user_agents = get_data_from_table(query)
    return listify(list_user_agents)


def get_unique_referers(num_days):
    # list unique ip addresses
    query = 'SELECT REFERER, COUNT(*) AS "#" FROM ' + \
        sql_table + ' GROUP BY REFERER ORDER BY 2'
    if num_days != 0:
        query = 'SELECT REFERER, COUNT(*) AS "#" FROM ' + sql_table + ' WHERE EPOCHTIME > ' + \
            return_epoch_time(num_days) + ' GROUP BY REFERER ORDER BY 2'
    list_referers = get_data_from_table(query)
    return listify(list_referers)


def get_unique_cookies_chart_data():
    db = pymysql.connect(host=sql_host, port=sql_port,
                         user=sql_username, passwd=sql_password, db=sql_db)
    c = db.cursor()

    # http://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime

    # calulates epcohtime using utc time for consistency incase server and local time are different
    date_now = datetime.datetime.utcnow()
    epoch_time_now = calendar.timegm(date_now.timetuple())

    yesterday_midnight = datetime.datetime(
        date_now.year, date_now.month, date_now.day, 0, 0)
    epoch_yesterday_midnight = calendar.timegm(yesterday_midnight.timetuple())

    epoch_midnight_1day_ago = epoch_yesterday_midnight - 86400
    epoch_midnight_2day_ago = epoch_yesterday_midnight - 2 * 86400
    epoch_midnight_3day_ago = epoch_yesterday_midnight - 3 * 86400
    epoch_midnight_4day_ago = epoch_yesterday_midnight - 4 * 86400
    epoch_midnight_5day_ago = epoch_yesterday_midnight - 5 * 86400
    epoch_midnight_6day_ago = epoch_yesterday_midnight - 6 * 86400
    epoch_midnight_7day_ago = epoch_yesterday_midnight - 7 * 86400

    # WTF is going on with this sql query?
    # needs organized.
    # are we getting today yesterday, 2 days ago, etc correctly?
    # why are they "AS" names not correct.
    #

    sqlquery = """SELECT COUNT(DISTINCT COOKIE) AS TODAY FROM """ + sql_table + """ WHERE EPOCHTIME > """ + str(epoch_yesterday_midnight) + \
        """ UNION ALL SELECT COUNT(DISTINCT COOKIE) AS YDAY FROM """ + sql_table + """ WHERE EPOCHTIME < """ + str(epoch_yesterday_midnight) + """ AND EPOCHTIME > """ + str(epoch_midnight_1day_ago) + \
        """ UNION ALL SELECT COUNT(DISTINCT COOKIE) AS YESTERDAY FROM """ + sql_table + """ WHERE EPOCHTIME < """ + str(epoch_midnight_1day_ago) + """ AND EPOCHTIME > """ + str(epoch_midnight_2day_ago) + \
        """ UNION ALL SELECT COUNT(DISTINCT COOKIE) AS TWODAYSAGO FROM """ + sql_table + """ WHERE EPOCHTIME < """ + str(epoch_midnight_2day_ago) + """ AND EPOCHTIME > """ + str(epoch_midnight_3day_ago) + \
        """ UNION ALL SELECT COUNT(DISTINCT COOKIE) AS THREEDAYSAGO FROM """ + sql_table + """ WHERE EPOCHTIME < """ + str(epoch_midnight_3day_ago) + """ AND EPOCHTIME > """ + str(epoch_midnight_4day_ago) + \
        """ UNION ALL SELECT COUNT(DISTINCT COOKIE) AS FOURDAYSAGO FROM """ + sql_table + """ WHERE EPOCHTIME < """ + str(epoch_midnight_4day_ago) + """ AND EPOCHTIME > """ + str(epoch_midnight_5day_ago) + \
        """ UNION ALL SELECT COUNT(DISTINCT COOKIE) AS FIVEDAYSAGO FROM """ + sql_table + """ WHERE EPOCHTIME < """ + str(epoch_midnight_5day_ago) + """ AND EPOCHTIME > """ + str(epoch_midnight_6day_ago) + \
        """ UNION ALL SELECT COUNT(DISTINCT COOKIE) AS SIXDAYSAGO FROM """ + sql_table + """ WHERE EPOCHTIME < """ + str(
            epoch_midnight_6day_ago) + """ AND EPOCHTIME > """ + str(epoch_midnight_7day_ago) + """;"""

    try:
        c.execute(sqlquery)
        data = c.fetchall()

        data_list = listify(str(data))
        unique_cookies_chart_data = []
        for tuple in data_list:
            unique_cookies_chart_data.append(str(tuple[0]))
        unique_cookies_chart_data = str(unique_cookies_chart_data)
    except:
        unique_cookies_chart_data = "Failed to gather the unique cookies chart data."

    db.close()
    return unique_cookies_chart_data
