"""Script to generate upcoming training pages.

This should be executed from _includes/ directory.
"""
import os

import yaml
from jinja2 import Template

SOURCE = "upcoming.yml"
TEMPLATE_ROOT = "src/templates"

def parse_upcoming():
    d = yaml.load(open(SOURCE).read())
    upcoming = d.pop('upcoming') or {}

    for key in d:
        course = d[key]
        course['key'] = key
        course['upcoming'] = key in upcoming

        course['url'] = "/trainings/%s.html" % key
        course['doattend_url'] = "http://%s.doattend.com/" % course['doattend']

    courses = d
    upcoming_courses = [courses[key] for key in upcoming]

    return courses, upcoming_courses

def render_template(_name, **vars):
    path = os.path.join(TEMPLATE_ROOT, _name)
    t = Template(open(path).read())
    return t.render(**vars)

def write_registration_page(course):
    content = render_template("registration.html", **course)

    os.system("mkdir -p register")
    with open("register/%s.md" % course['key'], 'w') as f:
        f.write(content)

def main():
    courses, upcoming_courses = parse_upcoming()

    with open("upcoming.html", "w") as f:
        f.write(render_template("upcoming.html", courses=upcoming_courses))

    for c in courses.values():
        write_registration_page(c)
        

if __name__ == "__main__":
    main()
    
    

