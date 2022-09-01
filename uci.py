from bs4 import BeautifulSoup
import mechanicalsoup
import requests

session = requests.Session()

browser = mechanicalsoup.StatefulBrowser(session, soup_config={'features': 'lxml'})
browser.open('https://www.ics.uci.edu/ugrad/courses/index-course')

browser.select_form('#course_search') #selects the one only form
browser.page.find(value='Upper-Division')['selected'] = ''
browser.page.find(value='CS')['selected'] = ''
browser.submit_selected()
courses = browser.page.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['hidden'])
courseList = []
for i in range(0, len(courses), 2):
    courseList.append({'name': courses[i].text.strip()})

dates = browser.page.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['instruction'])

for i in range(0, len(dates), 4):
    fall, winter, spring, _ = dates[i].text.strip(), dates[i + 1].text.strip(), dates[i + 2].text.strip(), dates[i + 3].text
    if fall:
        courseList[i // 4]['Fall'] = fall.replace('(2)', '')
    if winter:
        courseList[i // 4]['Winter'] = winter.replace('(2)', '')
    if spring:
        courseList[i // 4]['Spring'] = spring.replace('(2)', '')

for course in courseList:
    print(course)


# print(browser.open('https://www.reg.uci.edu/access/student/transcript/'))
# browser.open('https://login.uci.edu/ucinetid/webauth')

# browser.select_form('#webauth_login_form_id') #selecting the form for the uci login
# browser.form['ucinetid'] = 'cbryan2'
# browser.form['password'] = 'Bunyan_211202'
# browser.submit_selected(btnName='login_button')

# cookies = browser.session.cookies.get_dict()
# browser.open('https://www.reg.uci.edu/access/student/transcript/')
# print(browser.session.cookies)


# browserStudent = mechanicalsoup.StatefulBrowser(session, soup_config={'features': 'lxml'})
# browserStudent.open('https://www.reg.uci.edu/access/student/transcript/')
# browserStudent.launch_browser(browserStudent.page)


# print(soup.find(id='webauth'))