from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import glob
import jscrambler


class Command(BaseCommand):
    args = ''
    help = 'Run this command after collectstatic to apply jscrambler on javscript and html files found in STATIC_ROOT.  The files are replaced in-place with scrambled versions.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        staticroot = settings.STATIC_ROOT
        prevdir = os.getcwd()
        try:
            os.chdir(staticroot)
            config = settings.JSCRAMBLER_CONFIG
            filesSrc = config.get("filesSrc", ["**/*.js", "**/*.html"])
            files = set()
            for pattern in filesSrc:
                for src in glob.glob(pattern):
                    files.add(src)
            if not files:
                raise CommandError("Could not find any file to scramble!")
            self.stdout.write("Files to scramble:")
            for fname in files:
                self.stdout.write("\t" + fname)

            client = jscrambler.Client(config["keys"]["accessKey"], config["keys"]["secretKey"])
            result = client.upload_code(files, **config["params"])
            project_id = result['id']
        finally:
            os.chdir(prevdir)
            
        self.stdout.write("Upload successful, now polling project id {}".format(project_id))
        client.poll_project(project_id, maximum_poll_retries=50)
        self.stdout.write("Downloading project id {}".format(project_id))
        client.download_code(project_id, staticroot)
        self.stdout.write("Download successful.")
