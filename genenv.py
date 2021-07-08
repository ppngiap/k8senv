import os
import subprocess
import argparse


class EnvNode:
    def __init__(self, var, pattern, abbr):
        self.var = var
        self.pattern = pattern
        self.abbr = abbr
        self.pod = None
        self.container = None

    def match(self, pod):
        return pod.find(self.pattern) != -1

    def __set_container(self, pod):
        # typical pod has the format of *-59c8c86bcb-b2tr7
        arr = pod.split('-')
        try:
            if len(arr[-1]) == 5 and (len(arr[-2]) == 10 or len(arr[-2]) == 9):
                self.container = "-".join(arr[0:-2])
        except IndexError:
            self.container = None

    def set_pod(self, pod):
        if self.pod is not None:
            print("#Pod exist : %s" % self.pod)
            print("#Pod to add: %s" % pod)
        self.pod = pod
        self.__set_container(self.pod)

    def output(self):
        if self.pod is None:
            print("#export %s=" % self.var)
            return
        print("export %s=%s" % (self.var, self.pod))
        print("alias kkbash%s=\'kubectl exec -it %s -- /bin/bash\'" % (self.abbr, self.pod))
        print("alias kksh%s=\'kubectl exec -it %s -- /bin/sh\'" % (self.abbr, self.pod))
        print("alias kkdp%s=\'kubectl describe pod %s\'" % (self.abbr, self.pod))
        if self.container is not None:
            print("alias kklogs%s=\'kubectl logs %s -c %s\'" % (self.abbr, self.pod, self.container))
        else:
            print("alias kklogs%s=\'kubectl logs %s\'" % (self.abbr, self.pod))
        print("alias kkvi%s=\'kkdp%s > /tmp/pod_%s; vi /tmp/pod_%s\'" % (self.abbr, self.abbr, self.pod, self.pod))


class VmlcEnv:

    def set_template(self, file):
        self.nodes = []
        lines = open(file).readlines()
        for line in lines:
            line = line.strip()
            if len(line) == 0: continue
            words = line.split(':')
            self.nodes.append(EnvNode(words[0].strip(), words[1].strip(), words[2].strip()))

    def set_pod(self, pod):
        for node in self.nodes:
            if node.match(pod):
                node.set_pod(pod)
                break

    def output(self):
        for node in self.nodes:
            node.output()


vmlcEnv = VmlcEnv()


def get_cols(line):
    cols = []
    words = line.split(" ")
    for word in words:
        if len(word):
            cols.append(word)
    return cols


def process_pod(line):
    cols = get_cols(line)
    vmlcEnv.set_pod(cols[0])


def process_pods(text):
    lines = text.split("\n")
    for line in lines:
        if line.startswith("NAME"):
            continue
        if len(line) == 0:
            continue
        process_pod(line)
    vmlcEnv.output()


def main():
    vmlcEnv.set_template(os.path.expanduser('~/.k8senv/vmlc_template.txt'))

    parser = argparse.ArgumentParser(description='Generates script to create various pod environment variables')
    parser.add_argument('--test', type=str, help='text file contain output of "kubectl get pods"',
                        default=None, required=False)
    args = parser.parse_args()

    if args.test is not None:
        process_pods(open(os.path.expanduser(args.test)).read())
    else:
        process = subprocess.Popen(['kubectl', 'get', 'pods'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        process_pods(stdout)
        print(stderr)


if __name__ == '__main__':
    main()
