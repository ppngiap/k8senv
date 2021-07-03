import argparse
import os
import subprocess


class Node:
    def __init__(self, cols):
        self.repository = cols[0]
        self.tag = cols[1]
        self.id = cols[2]
        self.created = cols[3]
        self.size = cols[4]
        self.tarfile = self.repository.replace(':', '-').replace('/', '-') + self.tag + ".tar"

    def save_image_string(self):
        return "sudo docker image save %s:%s -o %s" % (self.repository, self.tag, self.tarfile)

    def rm_image_string(self):
        return "sudo docker image rm %s # %s:%s" % (self.id, self.repository, self.tag)


class DockerImages:
    def __init__(self, filename):
        self.nodes = []
        text = open(os.path.expanduser(filename)).read()
        self.process_images(text)

    def process_images(self, text):
        lines = text.split("\n")
        for line in lines:
            if line.startswith("REPOSITORY"):
                continue
            if len(line) == 0:
                continue
            self.process_image(line)

    def process_image(self, line):
        cols = self.get_cols(line)
        self.nodes.append(Node(cols))

    def get_cols(self, line):
        cols = []
        words = line.split(" ")
        for word in words:
            if len(word):
                cols.append(word)
        return cols

    def exists(self, image):
        ret = False
        for n in self.nodes:
            if n.repository == image.repository and n.tag == image.tag:
                ret = True
                break
        return ret

