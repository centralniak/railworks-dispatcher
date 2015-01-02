#!/usr/bin/env python

import datetime
import glob
import os
import random
import string
import sys
from xml.etree import ElementTree


IGNORED_SCENARIO_CLASSES = (
    'eTemplateScenarioClass',
    'eFreeRoamScenarioClass',
)
TEMPLATE = """
<html>
    <head>
        <title>${scenario_name}</title>
        <style type="text/css">
            body {
                font-family: monospace;
                margin: 0 auto;
                padding-top: 2cm;
                width: 15cm;
            }
        </style>
    </head>
    <body>
        <!-- ${scenario_class} -->
        <h1>${scenario_name}</h1>
        <h3>${scenario_description}</h3>
        <p>${scenario_briefing}</p>
        <hr>
        <date>Printed ${date} at ${scenario_start_location}</p>
    </body>
    <script type="text/javascript">
        //window.print()
    </script>
</html>
"""


def render_html(context):
    return string.Template(TEMPLATE).safe_substitute(**context)


def main():
    railworks_folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    dispatcher_folder = os.path.join(railworks_folder, 'Dispatcher')
    work_orders_folder = os.path.join(dispatcher_folder, 'WorkOrders')
    scenario_folders = os.path.join(railworks_folder,
                                    'Content', 'Routes', '*', 'Scenarios', '*', 'ScenarioProperties.xml')

    all_scenarios = glob.glob(scenario_folders)

    while True:
        todays_work_order = random.choice(all_scenarios)

        xml = ElementTree.parse(todays_work_order)

        scenario_name = xml.find('./DisplayName/Localisation-cUserLocalisedString/English').text
        scenario_description = xml.find('./Description/Localisation-cUserLocalisedString/English').text
        scenario_briefing = xml.find('./Briefing/Localisation-cUserLocalisedString/English').text
        scenario_start_location = xml.find('./StartLocation/Localisation-cUserLocalisedString/English').text
        scenario_class = xml.find('./ScenarioClass').text
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        if scenario_class in IGNORED_SCENARIO_CLASSES:
            continue

        # @TODO: get route name from respective parent folder
        # @TODO: if not present, assume we don't own this route

        break

    html = render_html({
        'scenario_name': scenario_name,
        'scenario_description': scenario_description,
        'scenario_briefing': scenario_briefing,
        'scenario_start_location': scenario_start_location or 'Depot',
        'scenario_class': scenario_class,
        'date': date
    })

    html_path = os.path.join(railworks_folder, 'WorkOrder.html')
    open(html_path, 'w').write(html.encode('utf8'))

    # @TODO: detect system and run created WorkOrder.html


if __name__ == '__main__':
    main()
