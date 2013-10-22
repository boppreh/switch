from subprocess import Popen as start
from os import path
from requests import get, exceptions

class Application(object):
    def __init__(self, project, executable, port):
        self.project = project
        self.project_dir = path.join('..', self.project)
        self.executable = path.join(self.project_dir, executable)
        self.port = port

    def is_running(self):
        try:
            url = 'http://localhost:' + str(self.port)
            return 200 <= get(url, timeout=0.001).status_code < 300
        except (exceptions.ConnectionError, exceptions.Timeout):
            return False

    def exists(self):
        return path.isdir(self.project_dir) and path.isfile(self.executable)

applications = [Application('scheduler', 'schedule_notifier.pyw', 2340),
                Application('typist', 'typist.pyw', 2341),
                Application('activity', 'watcher_daemon.pyw', 2342),
                Application('network_status', 'netstat.pyw', 2343),
                Application('j', 'global_j.pyw', 2344),
                Application('doorman', 'doorman.pyw', 2345),
                Application('pycalc', 'calc.pyw', 2346),
                Application('gitstatus', 'gitstatus.pyw', 2347),
               ]

project_url_template = 'https://github.com/boppreh/{}.git'

if __name__ == '__main__':
    from git import Repo
    for application in applications:
        if not application.exists():
            print application.project
            project_url = project_url_template.format(application.project)
            Repo.clone_from(project_url, application.project_dir)
