import argparse
import os
import subprocess
import docker_images as dimg


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

    images = dimg.DockerImages(args.images)
    exclude = None
    if args.exclude is not None:
        exclude = dimg.DockerImages(args.exclude)
    process(images, exclude)


if __name__ == '__main__':
    main()
