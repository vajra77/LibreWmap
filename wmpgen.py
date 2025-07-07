import sys
import pwd
import grp
import os
from jinja2 import Environment, FileSystemLoader
from librewmap.map import Map


if __name__ == '__main__':
    this_map = Map.from_file(sys.argv[1])
    this_map.retrieve_data()

    env = Environment(loader=FileSystemLoader('./templates'))

    page_file = "maps/html/" + this_map.name + ".html"
    css_file = "maps/html/css/" + this_map.name + ".css"

    with open(page_file, 'w') as f:
        template = env.get_template('map.html.j2')
        html = template.render(map=this_map)
        f.write(html)

    with open(css_file, 'w') as f:
        template = env.get_template('style.css.j2')
        css = template.render(map=this_map)
        f.write(css)

    uid = pwd.getpwnam("www-data").pw_uid
    gid = grp.getgrnam("www-data").gr_gid
    os.chown(page_file, uid, gid)
    os.chown(css_file, uid, gid)
