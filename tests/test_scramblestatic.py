import json
import pytest
import shutil
import os
from jscrambler import Client
from jscrambler.management.commands.scramblestatic import Command
from django.conf import settings
from django.core.management.base import CommandError

settings.configure()


@pytest.mark.parametrize("files_src", ["*.js", ""])
def test_scramblestatic(monkeypatch, tmpdir, files_src):
    tmpdir = str(tmpdir)
    shutil.copy("tests/test1.js", tmpdir)
    settings.STATIC_ROOT = tmpdir
    with open('tests/test_config.json') as jfile:
        settings.JSCRAMBLER_CONFIG = json.loads(jfile.read())
    settings.JSCRAMBLER_CONFIG['filesSrc'] = files_src
    del settings.JSCRAMBLER_CONFIG['filesDest']
    print(settings.JSCRAMBLER_CONFIG)
    os.system("ls -l " + tmpdir)

    def upload_code(self, files, **params):
        return {"id": 123}
    monkeypatch.setattr(Client, "upload_code", upload_code)

    def poll_project(self, project_id, maximum_poll_retries=10):
        pass
    monkeypatch.setattr(Client, "poll_project", upload_code)

    def download_project(self, project_id, destdir):
        pass
    monkeypatch.setattr(Client, "download_code", download_project)

    cmd = Command()
    if files_src:
        cmd.handle()
    else:
        with pytest.raises(CommandError):
            cmd.handle()
