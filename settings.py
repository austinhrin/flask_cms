
# settings
websites = [
    {
        'domain': '127.0.0.1:5000',
        'folder': 'js_cms',
        'cms': {
            'theme': 'default'
        }
    },
    {
        'domain': 'indexdothtml.com',
        'jinja2_templates': 'true'
    },
    {'domain': 'austinhrin.com'},
    {
        'domain': '67skylark.com',
        'folder': '67skylark.com'
    },
    {
        'domain': '1967skylark.com',
        'folder': '67skylark.com'
    },
    {
        'domain': '1967buickskylark.com',
        'folder': '67skylark.com'
    },
    {
        'domain': '67buickskylark.com',
        'folder': '67skylark.com'
    },
    {
        'domain': '340buick.com',
        'folder': '67skylark.com'
    },
    {'domain': 'losijrx.com'},
    {'domain': 'losiminit.com'},
    {'domain': 'losixx.com'},
    {'domain': 'onpageseo.solutions'},
    {'domain': 'pontiacaztek.com'}
]

bad_user_agents = [
    'crawler',
    'curl',
    'Go-http-client',
    'baidu',
    'Dataprovider.com',
    'megaindex',
    'seekport',
    'netcraft',
    '.ru',
    'builtwith.com',
    'panscient.com',
    'bsalsa.com',
    'sysscan',
    'LinkWalker',
    'gdnplus',
    'Typhoeus',
    'hubspot',
    'sindresorhus',
    'spyonweb',
    'research',
    'scan',
    'project',
    'github.com',
    'evestigator.com.au',
    'tweezler.com',
    'GTmetrix',
    'python',
    'wget',
    'perl',
    'java',
    'orgprobe',
    'cisco',
    'scrapy',
    'boost.beast',
    'httpclient',
    'the knowledge ai',
    'microsoft office',
    'print(',
    'bitcoin',
    'hewwo',
    'meow',
    'urltester',
    'honeybee',
    'banner detection',
    'ineturl',
    'axios',
    'coffee maker',
    'bit.ly/',
    'zgrab',
    'HeadlessChrome',
    'headless',
    'masscan/1.0 (https://github.com/robertdavidgraham/masscan)',
    'NetSystemsResearch studies the availability of various services across the internet. Our website is netsystemsresearch.com',
    'Mozilla/5.0 (compatible; Nimbostratus-Bot/v1.3.2; http://cloudsystemnetworks.com)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)',
]

# user agents that arent in the above list but we dont want to track
dont_track = [
    'facebookexternalhit',
    'bot',
    'spider',
    'google',
    'seo',
]

# anything not allowed in url
not_allowed_in_url = [
    '<php>',
    'login.destroy',
    'cpanel',
    'q=semalt.com'
]

# bad referers aka referer spam
bad_referers = [
    'anti-crisis-seo'
]
