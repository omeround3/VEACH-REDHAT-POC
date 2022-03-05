import subprocess


class Sheller:
    def __init__(self, password: str):
        """
        :param password: sudo password
        """
        # self.password = bytes(password, 'utf-8')
        self.password = password

    def run_shell_command(self, cmd: str, stdout_pattern: list) -> list:
        """
        :param cmd: a str with the full shell command you want to run
        :param stdout_pattern: list of output record strings, e.g ['app_name', 'version']
        :return: a list of dict values, where key bwlongs to 'stdout_patters' and values the output of the shell command
        """
        args = [arg for arg in cmd.split(' ') if len(arg) > 0]
        args.insert(0, 'sudo')
        args.insert(1, '-S')

        ret_val = []

        cmd1 = subprocess.Popen(['echo', self.password], stdout=subprocess.PIPE)
        cmd2 = subprocess.Popen(args, stdin=cmd1.stdout, stdout=subprocess.PIPE)

        if cmd2.stderr:
            raise Exception(cmd2.stderr.read().decode())

        counter = 0
        for record in cmd2.stdout:
            counter +=1
            tmp = record.decode().split('\t')
            if len(tmp) == len(stdout_pattern):
                ret_val.append(dict(zip(stdout_pattern, tmp)))
        return ret_val
