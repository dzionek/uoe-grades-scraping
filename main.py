# Selenium WebDriver
from statistics import mean

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Web Scraping
from bs4 import BeautifulSoup
import re

import json

def take_login_data():
    login = input('Give me your login: ')
    password = input('Give me your password: ')
    return login, password

def login_user(driver, login, password):
    driver.get("https://www.myed.ed.ac.uk")

    login_button = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_id("login-btn"))
    login_button.click()

    login_input = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_name('login'))
    login_input.send_keys(login)
    login_input.send_keys(Keys.ENTER)

    password_input = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_name('password'))
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

def go_to_grades(driver):
    accounts_tab = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_id('myed-nav-tab-2'))
    accounts_tab.click()

    driver.find_element_by_xpath("//*[text()='My student record']").click()

    assessment_tab = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_id('nav-UTCMPSI-assessment'))
    assessment_tab.click()

def get_name_uun(soup):
    info_div = soup.find_all("div", class_="padded")
    if len(info_div) != 1:
        raise LookupError("There is no unique div with user's data.")

    info_h = info_div[0].find('h2').text
    pattern = re.compile(r'\w[a-zA-Z0-9 ]*')
    return re.findall(pattern, info_h)

def get_course_name(course):
    """
    >>> get_course_name("\\n\\nProofs and Problem Solving\\n\\n– MATH08059\\n\\n\\n")
    "Proofs and Problem Solving"
    """
    pattern = re.compile(r'[a-zA-Z\-0-9 ]+\n')
    return re.findall(pattern, course)[0].strip()

def get_course_code(course):
    pattern = re.compile(r'[a-zA-Z0-9 ]+\n')
    return re.findall(pattern, course)[1].strip()

def get_grades(soup):
    grades_container = soup.find_all("div", class_='uoe-selfservice-assessment-container')
    if len(grades_container) != 1:
        raise LookupError("There is no unique div with user's grades.")
    grades_container = grades_container[0]

    courses = []
    for child in [child for child in grades_container.children if child.name is not None]:
        course_h = child.find("h2", class_="panel-title")

        if 'Pass' not in str(course_h):
            course, grade, grade_unit, grade_symbol = [tag.text for tag in course_h.find_all("span")]
        else:
            grade = 'Pass'
            grade_unit = ''
            course, grade_symbol = [tag.text for tag in course_h.find_all("span")]

        course_name = get_course_name(course)
        course_code = get_course_code(course)

        course = dict(
            name=course_name, code=course_code,
            grade=dict(
                exact=grade.strip()+grade_unit.strip(),
                symbol=grade_symbol.strip()
            )
        )
        courses.append(course)

    return courses

def grades_to_json(driver):

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "uoe-selfservice-assessment-unit"), '%')
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    name, uun = get_name_uun(soup)
    courses = get_grades(soup)
    return json.dumps({
        'name': name,
        'uun': uun,
        'average': str(round(mean([
            int(course['grade']['exact'][:-1])
            for course in courses
            if course['grade']['exact'].endswith('%')
        ]), 2)) + '%',
        'courses': courses
    })


def main():
    login, password = take_login_data()
    driver = webdriver.Chrome('drivers/chromedriver')
    login_user(driver, login, password)
    go_to_grades(driver)
    grades_json = grades_to_json(driver)
    grades_json_parsed = json.loads(grades_json)
    print(json.dumps(grades_json_parsed, indent=4))
    with open('grades.json', 'w', encoding='utf-8') as f:
        json.dump(grades_json_parsed, f, ensure_ascii=False, indent=4)

    print('\nThe JSON output with the grades was successfully saved in grades.json!')
    driver.quit()


if __name__ == '__main__':
    main()