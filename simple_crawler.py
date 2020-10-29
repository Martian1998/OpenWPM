from automation import CommandSequence, TaskManager
import tempfile
import time
import os
import copy
import json

NUM_BROWSERS = 3

# The list of sites that we wish to crawl
sites = ['http://www.example.com',
         'https://princeton.edu',
         'https://citp.princeton.edu/']

# Loads the default manager preferences and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    browser_params[i]['disable_flash'] = False #Enable flash for all three browsers
browser_params[0]['headless'] = True #Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
for site in sites:
    command_sequence = CommandSequence.CommandSequence(site)
    command_sequence.get(sleep=0, timeout=60)
    command_sequence.screenshot_full_page()
    manager.execute_command_sequence(command_sequence) # ** = synchronized browsers
    # ** = not synchronized browsers, it gives an error that index should not be an integer
    # on base level function index is checked for none or an integer value 
    

# Shuts down the browsers and waits for the data to finish logging
manager.close()