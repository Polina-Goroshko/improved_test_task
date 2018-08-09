import os
import paramiko
import pytest
import subprocess
import time

from logger_creation import log

global_path = os.path.expanduser("~/dirForTest/")
server_ip = "192.168.56.1"


def pytest_addoption(parser):
    parser.addoption("--clientIP", action="store")
    parser.addoption("--clientPort", action="store")
    parser.addoption("--clientName", action="store")
    parser.addoption("--clientPassword", action="store")


@pytest.fixture(scope='module')
def parser_of_command_line(request):
    return request.config.getoption("--clientIP"), \
           request.config.getoption("--clientPort"), \
           request.config.getoption("--clientName"), \
           request.config.getoption("--clientPassword"), \



@pytest.fixture(scope="function")
def dir_on_server_creation():
    log.info("I am in dir_on_server_creation")
    proc_2 = subprocess.Popen(["sudo", "mkdir", global_path], stdin=subprocess.PIPE)
    proc_2.communicate()
    return_code_2 = proc_2.wait()
    return return_code_2


@pytest.fixture(scope="function")
def dir_on_server_permission_change():
    log.info("I am in dir_on_server_permission_change")
    proc7 = subprocess.Popen(["sudo", "chmod", "ugo+rwx", global_path], stdin=subprocess.PIPE)
    proc7.communicate()
    return_code_7 = proc7.wait()
    return return_code_7


@pytest.fixture(scope="module")
def session_with_client_creation(parser_of_command_line):
    log.info("I am in session_with_client_creation")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=parser_of_command_line[0],
                   port=int(parser_of_command_line[1]),
                   username=parser_of_command_line[2],
                   password=parser_of_command_line[3])
    return client


@pytest.fixture(scope="function")
def dir_on_client_creation(session_with_client_creation):
    log.info("I am in dir_on_client_creation")
    log.info("client %s", session_with_client_creation)
    session_with_client_creation.exec_command('mkdir /home/$USER/dirForMount/')


@pytest.fixture(scope="function")
def file_with_permissions_on_server_clean():
    log.info("I am in file_with_permissions_on_server_clean")
    proc_8 = subprocess.Popen(["sudo", "cp", "/dev/null", "/etc/exports"], stdin=subprocess.PIPE)
    proc_8.communicate()
    return_code_8 = proc_8.wait()
    return return_code_8


@pytest.fixture(scope="function", params=["(rw)", "(ro)"])
def perm_for_export_creation(request, parser_of_command_line):
    dir_for_export_name = global_path
    log.info("I am in perm_for_export_creation")
    perm_for_export = dir_for_export_name + " " + parser_of_command_line[0] + request.param
    var = request.param
    return perm_for_export, var


@pytest.fixture(scope="function")
def file_with_perm_for_export_creation(perm_for_export_creation):
    log.info("I am in file_with_perm_for_export_creation")
    with open(os.path.join(global_path, "fileWithPermForExport"), "w") as f:
        f.write(perm_for_export_creation[0])
    return f


@pytest.fixture(scope="function")
def file_perm_export_copy(perm_for_export_creation):
    log.info("I am in file_perm_export_copy")
    proc_21 = subprocess.Popen(["sudo", "cp", os.path.join(global_path, "fileWithPermForExport"), "/etc/exports"],
                               stdin=subprocess.PIPE)
    proc_21.communicate()
    return_code_21 = proc_21.wait()
    return return_code_21


@pytest.fixture(scope="function")
def update_etc_exports(session_with_client_creation):
    log.info("I am in update_etc_exports")
    proc9 = subprocess.Popen(["sudo", "exportfs", "-a"], stdin=subprocess.PIPE)
    proc9.communicate()


@pytest.fixture(scope="function")
def mount_dir(session_with_client_creation, parser_of_command_line):
    log.info("I am in mount_dir")
    session_with_client_creation.exec_command(
        "echo %s | sudo -S mount %s:%s /home/$USER/dirForMount/" % (parser_of_command_line[3], server_ip, global_path))
    time.sleep(0.5)


@pytest.fixture(scope="function")
def main_setup_fixture(request, parser_of_command_line, dir_on_server_creation, dir_on_server_permission_change,
                       session_with_client_creation,
                       dir_on_client_creation, file_with_permissions_on_server_clean,
                       file_with_perm_for_export_creation, file_perm_export_copy, update_etc_exports, mount_dir,
                       perm_for_export_creation):
    log.info("I am in main_setup_fixture")

    def main_teardown_finilizer():
        log.info("I am in main_teardown_finilizer")
        proc_3 = subprocess.Popen(["sudo", "rm", "-rf", global_path])
        log.info("/home/polina/dirForTest/ is removed on server")
        proc_3.communicate()
        proc_3.wait()
        session_with_client_creation.exec_command('rmdir /home/$USER/dirForMount/')
        log.info("/home/$USER/dirForMount/ is removed on client")
        log.info("client %s", session_with_client_creation)
        if "(rw)" == perm_for_export_creation[1]:
            session_with_client_creation.exec_command('rm /home/$USER/dirForMount/cinema')
            log.info("/home/$USER/dirForMount/cinema is removed on client")

    def unmount_dir():
        log.info("I am in unmount_dir")
        session_with_client_creation.exec_command(
            "echo %s | sudo -S umount /home/$USER/dirForMount/" % (parser_of_command_line[3]))

    request.addfinalizer(main_teardown_finilizer)
    request.addfinalizer(unmount_dir)
    return 0
