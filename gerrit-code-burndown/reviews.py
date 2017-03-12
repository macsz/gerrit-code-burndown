import configparser
import json

import requests
from requests.auth import HTTPDigestAuth


def reviews(file, debug=False):
    project_site = "https://review.openstack.org/changes/"
    query = "q=project:openstack/nova+file:{0}+topic:{1}".format(file, 'bp/remove-mox-pike')
    attrs = ("&o=CURRENT_REVISION&o=ALL_COMMITS&o=ALL_FILES&o=LABELS"
             "&o=DETAILED_LABELS&o=DETAILED_ACCOUNTS")
    url = "%s?%s" % (project_site, query)

    config = configparser.ConfigParser()
    config.read('config.ini')
    user = config.get(config.default_section, 'user')
    password = config.get(config.default_section, 'password')
    auth = HTTPDigestAuth(user, password)
    resp = requests.get(url, auth=auth)

    if debug:
        print('GET URL', url)
        print('Status code:', resp.status_code)
        print('Encoding:', resp.encoding)

    # slice out the "safety characters"
    content = resp.text[5:]
    if debug:
        print("Response from Gerrit:\n")
        print(content)
    content = json.loads(content)
    return content
