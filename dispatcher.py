#!/usr/bin/env python

import datetime
import glob
import os
import random
import string
import sys
from xml.etree import ElementTree


IGNORED_SCENARIO_CLASSES = (
    'eFreeRoamScenarioClass',
    'eTemplateScenarioClass',
    'eTutorialScenarioClass',
)
TEMPLATE = """<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>${scenario_name}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="file://${dispatcher_artwork_folder}/main.css">
    </head>
    <body>
        <article class="${scenario_class}">
            <img class="logo" src="file://${dispatcher_artwork_folder}/${logo}" alt="">
            <div>Driver ${username}</div>
            <div class="larger">Shift ${shift_number}</div>
            <h1>${scenario_name}</h1>
            <div class="larger">${scenario_description}</div>
            <div class="with-margin">${scenario_briefing}</div>
            <div class="with-margin">Printed ${date} at ${scenario_start_location}</div>
        </article>
    </body>
</html>"""


def ensure_folder(path):
    try:
        os.makedirs(path)
        return True
    except OSError:
        return False


def int_to_time(int_time):
    HOUR = 3600
    hours = int(int_time / HOUR)
    minutes = (int_time % HOUR) / 60
    return hours, minutes


def launch_html(path):
    try:
        os.startfile(path)
    except AttributeError:
        os.system('xdg-open \'%s\'' % path)


def render_html(context):
    return string.Template(TEMPLATE).safe_substitute(**context)


def main():
    railworks_folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    scenario_folders = os.path.join(railworks_folder,
                                    'Content', 'Routes', '*', 'Scenarios', '*', 'ScenarioProperties.xml')
    work_orders_folder = os.path.join(railworks_folder, 'WorkOrders')

    dispatcher_folder = os.path.abspath(os.path.dirname(sys.argv[0]))
    dispatcher_data_folder = os.path.join(dispatcher_folder, 'Dispatcher')

    all_scenarios = glob.glob(scenario_folders)

    while True:
        todays_work_order = random.choice(all_scenarios)

        # only allow scenarios from existing unpacked routes
        scenario_folder_suffix = os.path.join(*todays_work_order.split(os.sep)[-3:])
        route_folder = todays_work_order.replace(scenario_folder_suffix, '')
        route_description = os.path.join(route_folder, 'RouteProperties.xml')
        if not os.path.exists(route_description):
            continue

        xml = ElementTree.parse(todays_work_order)

        scenario_class = xml.find('./ScenarioClass').text
        if scenario_class in IGNORED_SCENARIO_CLASSES:
            continue

        scenario_name = xml.find('./DisplayName/Localisation-cUserLocalisedString/English').text
        scenario_description = xml.find('./Description/Localisation-cUserLocalisedString/English').text
        scenario_briefing = xml.find('./Briefing/Localisation-cUserLocalisedString/English').text
        scenario_start_location = xml.find('./StartLocation/Localisation-cUserLocalisedString/English').text
        scenario_start_time = xml.find('./StartTime').text
        scenario_start_day = xml.find('./StartDD').text
        scenario_start_month = xml.find('./StartMM').text
        scenario_start_year = xml.find('./StartYYYY').text

        time = int_to_time(int(scenario_start_time))
        time_adjust = random.randrange(15, 45)
        date = datetime.datetime(
            int(scenario_start_year), int(scenario_start_month), int(scenario_start_day),
            *time
        ) - datetime.timedelta(minutes=time_adjust)

        break

    ensure_folder(work_orders_folder)

    html = render_html({
        'date': date,
        'dispatcher_artwork_folder': os.path.join(dispatcher_data_folder, 'Artwork'),
        'logo': 'BR.jpg',
        'scenario_name': scenario_name,
        'scenario_description': scenario_description,
        'scenario_briefing': scenario_briefing,
        'scenario_start_location': scenario_start_location or 'Depot',
        'scenario_class': scenario_class,
    })

    # @TODO: bump numbers - 0001.html, 0002.html etc.

    html_path = os.path.join(work_orders_folder, 'WorkOrder.html')
    open(html_path, 'w').write(html.encode('utf8'))
    launch_html(html_path)


if __name__ == '__main__':
    main()
