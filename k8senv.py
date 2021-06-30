import os
import subprocess


class EnvNode:
    def __init__(self, var, pattern, abbr):
        self.var = var
        self.pattern = pattern
        self.abbr = abbr
        self.pod = ''

    def match(self, pod):
        return pod.find(self.pattern) != -1

    def set_pod(self, pod):
        if len(self.pod):
            print("#Pod exist : ", self.pod)
            print("#Pod to add: ", pod)
        self.pod = pod

    def output(self):
        if len(self.pod) == 0:
            print("#export %s=" % self.var)
            return
        print("export %s=%s" % (self.var, self.pod))
        print("alias kkbash%s=\'kubectl exec -it %s -- /bin/bash\'" % (self.abbr, self.pod))
        print("alias kksh%s=\'kubectl exec -it %s -- /bin/sh\'" % (self.abbr, self.pod))
        print("alias kkdp%s=\'kubectl describe pod %s\'" % (self.abbr, self.pod))
        print("alias kklogs%s=\'kubectl logs %s\'" % (self.abbr, self.pod))
        print("alias kkvi%s=\'kkdp%s > /tmp/pod_%s; vi /tmp/pod_%s\'" % (self.abbr, self.abbr, self.pod, self.pod))



class VmlcEnv:

    def set_template(self, file):
        self.nodes = []
        lines = open(file).readlines()
        for line in lines:
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


vmlcEnv.set_template(os.path.expanduser('~/.k8senv/vmlc_template.txt'))

process = subprocess.Popen(['kubectl', 'get', 'pods'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

process_pods(stdout)
print(stderr)
