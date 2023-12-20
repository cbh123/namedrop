import os
import replicate
import base64
import argparse
import imghdr
import xattr
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None
        elif event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            rename_images_in_dir(event.src_path)


def encode_image(image_path):
	"""Encode an image into URI"""
	with open(image_path, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
		return "data:image/png;base64," + encoded_string

def rename_file(path):
    # Check if path is a file and exists
	if not os.path.isfile(path) or not os.path.exists(path):
		return None

	# Check if file is already renamed
	try:
		if xattr.getxattr(path, 'user.renamed'):
			print(f"Skipping {path}, already renamed.")
			return os.path.split(path)[1]
	except OSError:
		pass  # Attribute does not exist, continue with renaming


	uri = encode_image(path)

	# use https://replicate.com/yorickvp/llava-13b to rename file
	output = replicate.run(
		"yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
		input={
			"image": uri,
			"top_p": 1,
			"prompt": "Can you create a filename for this image? Just give me the filename, no pre-amble, and no extension.",
			"max_tokens": 1024,
			"temperature": 0.2
		}
	)
	output = "".join([x for x in output])

	# get extension from original filename
	_directory, filename = os.path.split(path)
	_filename, extension = os.path.splitext(filename)

	# add hyphens between spaces and lowercase, remove .
	output = output.replace(" ", "-").lower().replace(".", "")

	# replace .png, .jpg, .jpeg in output with nothing
	output = output.replace(".png", "").replace(".jpg", "").replace(".jpeg", "")

	# After renaming the file, set the 'user.renamed' attribute
	xattr.setxattr(path, 'user.renamed', b'true')

	print(f"Renaming {filename} to {output}{extension}")
	return output + extension


def rename_images_in_dir(path):
	if os.path.isdir(path):
		for filename in os.listdir(path):
			file_path = os.path.join(path, filename)
			if not os.path.isfile(file_path):
				continue
			if imghdr.what(file_path) in ['jpeg', 'png']:
				new_name = rename_file(os.path.join(path, filename))
				os.rename(os.path.join(path, filename), os.path.join(path, new_name))
	elif os.path.isfile(path) and path.lower().endswith(('.png', '.jpg', '.jpeg')):
		directory, filename = os.path.split(path)
		new_name = rename_file(path)
		os.rename(path, os.path.join(directory, new_name))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Rename images in a directory or a single file.')
	parser.add_argument('path', help='The directory or file to rename images in.')
	args = parser.parse_args()

	rename_images_in_dir(args.path)

	event_handler = ImageHandler()
	observer = Observer()
	observer.schedule(event_handler, path=args.path, recursive=False)
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
