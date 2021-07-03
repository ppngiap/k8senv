import argparse
import docker_images as dimg


def process(images):
    for n in images.nodes:
        if n.tag == "<none>" or n.repository == "<none>":
            print(n.rm_image_string())


def main():
    parser = argparse.ArgumentParser(description='Removes images with <none>:<none>')
    parser.add_argument('images', type=str, help='text file contain output of "docker image ls"')
    args = parser.parse_args()

    images = dimg.DockerImages(args.images)
    process(images)


if __name__ == '__main__':
    main()
