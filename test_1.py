from logger_creation import log


def test_1(main_setup_fixture, perm_for_export_creation, session_with_client_creation, parser_of_command_line):
	log.info("I am in a test_1: file creation")
	log.info("Here is what now is in /etc/exports %s", perm_for_export_creation[0])
	stdin, stdout, stderr = session_with_client_creation.exec_command("echo %s | sudo -S touch /home/$USER/dirForMount/cinema" % (parser_of_command_line[3]))
	log.info("%s", stderr.read())
	log.info("permForExportCreation[1] in test_1: %s", perm_for_export_creation[1])
	if "(ro)" == perm_for_export_creation[1]:
		log.info("exit status of creation a file with RO: %s", stdout.channel.recv_exit_status())
		assert stdout.channel.recv_exit_status() == 1
	else:
		log.info("exit status of creation a file with RW: %s", stdout.channel.recv_exit_status())
		assert stdout.channel.recv_exit_status() == 0
