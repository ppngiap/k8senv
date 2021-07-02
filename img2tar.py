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


def process(images, ex):
    for n in images.nodes:
        s = ""
        if ex is not None and ex.exists(n):
            s = "# "
        if n.tag == "3.1.8-pv757-saml" \
                or n.tag == "3.1.5-alok-tom" \
                or n.tag == "3.1.622" \
                or n.tag == "3.1.104" \
                or n.tag == "<none>":
            s = "# "
        print("%s%s" % (s, n.save_image_string()))


def main():
    parser = argparse.ArgumentParser(description='Generate script to create tar from docker images')
    parser.add_argument('--exclude', type=str, help='text file contain output of "docker image ls" to be excluded',
                        default=None, required=False)
    parser.add_argument('images', type=str, help='text file contain output of "docker image ls"')
    args = parser.parse_args()

    images = DockerImages(args.images)
    exclude = None
    if args.exclude is not None:
        exclude = DockerImages(args.exclude)
    process(images, exclude)


if __name__ == '__main__':
    main()
