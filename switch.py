from subprocess import Popen as start
from os import path
from requests import get, exceptions
from git import Repo

class Application(object):
    def __init__(self, project, executable, port):
        self.project = project
        self.project_dir = path.join('..', self.project)
        self.executable = path.join(self.project_dir, executable)
        self.port = port
        self.process = None

    def is_running(self):
        try:
            url = 'http://localhost:' + str(self.port)
            return 200 <= get(url, timeout=0.001).status_code < 300
        except (exceptions.ConnectionError, exceptions.Timeout):
            return False

    def is_started(self):
        return self.process is not None

    def start(self):
        self.process = start(['pythonw', self.executable], cwd=self.project_dir)

    def kill(self):
        self.process.kill()
        self.process = None

    def is_installed(self):
        return path.isdir(self.project_dir) and path.isfile(self.executable)

    def install(self):
        project_url = project_url_template.format(application.project)
        Repo.clone_from(project_url, application.project_dir)

    def status(self):
        if self.is_started():
            return 'Started'
        elif self.is_running():
            return 'Already running'
        elif self.is_installed():
            return 'Stopped'
        else:
            return 'Not installed'


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

def install_all():
    for application in applications:
        if not application.is_installed():
            application.install()

def start_all():
    install_all()

    for application in applications:
        if not application.is_running():
            print 'Starting', application.project
            application.start()


if __name__ == '__main__':
    from simpleserver import serve

    get_services = {}
    post_services = {'start_all': start_all, 'install_all': install_all}
    for application in applications:
        sub_service = {'start': application.start,
                       'stop': application.kill}
        post_services[application.project] = sub_service
        get_services[application.project] = application.status

    serve(get_services, post_services, port=2348)
