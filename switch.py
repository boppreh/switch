from subprocess import Popen as start
from os import path

class Application(object):
    def __init__(self, project, executable, port):
        self.project = project
        self.executable = executable
        self.port = port

    def exists(self):
        project_dir = path.join('..', self.project)
        executable = path.join(project_dir, self.executable)
        return path.isdir(project_dir) and path.isfile(executable)

applications = [Application('scheduler', 'schedule_notifier.pyw', 2340),
                Application('typist', 'typist.pyw', 2341),
                Application('activity', 'watcher_daemon.pyw', 2342),
                Application('network_status', 'netstat.pyw', 2343),
                Application('j', 'global_j.pyw', 2344),
                Application('doorman', 'doorman.pyw', 2345),
                Application('pycalc', 'calc.pyw', 2346),
                Application('gitstatus', 'gitstatus.pyw', 2347),
               ]

if __name__ == '__main__':
    for application in applications:
        if not application.exists():
            print application.project
