# -*- coding:utf-8 -*-
import os
import sys
import time

from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
GIT_REPO = 'git@github.com:hellhound/dentexchange.git'

env.hosts = [
    'dentexchange@127.0.0.1',
]
env.key_filename = [
    os.path.realpath(os.path.join(BASE_DIR, 'etc', 'dentexchange_keyfile'))
]


def deploy(commit_hash):
    print blue('Today is a good day to deploy.')
    run('sudo rabbitmqctl stop_app')
    run('sudo rabbitmqctl reset')
    run('sudo rabbitmqctl start_app')
    with prefix('source `which virtualenvwrapper.sh`'):
        print red('Preparing the environment.')
        with cd('~/projects'):
            if exists('dentexchange'):
                with cd('dentexchange'), prefix('workon dentexchange'), \
                        settings(warn_only=True):
                    print green('Removing the current crontab')
                    run('crontab -r')
                    print green('Cleaning Haystack index')
                    run('dentexchange/project/manage.py clear_index --noinput '
                        '-v 3')
                    print green('Stopping the supervisor daemon.')
                    result = run('supervisorctl -c etc/supervisord.ini ' \
                        'stop dentexchange:*')
                    if result.succeeded:
                        run('supervisorctl -c etc/supervisord.ini shutdown')
                    else:
                        run('pkill supervisord')
                print green('Removing the virtual environment.')
                run('rmvirtualenv dentexchange')
            else:
                print red('Cloning repository.')
                run('git clone %s dentexchange' % GIT_REPO)
        with cd('~/projects/dentexchange'):
            print green('Performing housekeeping on the working copy.')
            run('git checkout -- .')
            run('git reset HEAD .')
            print green('Puling las changes from upstream.')
            run('git checkout master')
            run('git pull origin master')
            print green('Checking out commit %s.' % commit_hash)
            run('git checkout  %s' % commit_hash)
            run('git clean -df')
            run('mkvirtualenv dentexchange')
            print red('Configuring environment and dependencies.')
            with prefix('workon dentexchange'):
                print green('Installing requirements.')
                run('bin/install_requirements')
                print green('Rebuilding the database.')
                run('bin/init_db')
                run('dentexchange/project/manage.py syncdb --noinput')
                run('dentexchange/project/manage.py migrate')
                #run('bin/createsuperuser')
                run('bin/load_fixture')
                print green('Generate Solr schema.')
                run('bin/build_solr_schema')
                print green('Collecting static files.')
                run('dentexchange/project/manage.py collectstatic --noinput')
                print green('starting the supervisor daemon.')
                run('supervisord -c etc/supervisord.ini')
                time.sleep(30)
                print green('Rebuilding Haystack index.')
                run('dentexchange/project/manage.py rebuild_index --noinput '
                    '-v 3')
                time.sleep(15)
                print green('Creating the crontab')
                run('crontab < etc/crontab')
        print green('Smoke testing /: hopefully we would get a response ' \
            'different from 500')
        host = env.host_string.split('@')[-1]
        result = run('curl --write-out "%%{http_code}\n" --silent ' \
            '--output /dev/null http://%s' % host)
        if result.startswith('5'):
            print red('The smoke test failed.')
            sys.exit(-1)
        print blue('All done.')
