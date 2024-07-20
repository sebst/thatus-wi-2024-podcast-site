import os
import json
import logging
import tempfile
import shutil



DATA_GIT_REPO = "https://github.com/sebst/thatus-wi-2024-podcast-collector.git"
DATA_GIT_REPO_NAME = "thatus-wi-2024-podcast-collector"
DATA_JSON_PATH_IN_GIT_REPO = "generated"
DATA_IMAGES_PATH_IN_GIT_REPO = "generated/images"
DATA_JSON_STORAGE = "data/podcasts"
DATA_IMAGE_STORAGE = "data/podcasts"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

from git import Repo

def sync_podcasts(json_storage_path, image_storage_path):
    tmp_dir = tempfile.gettempdir()
    tmp_clone_dir = os.path.join(tmp_dir, DATA_GIT_REPO_NAME)
    
    # Cloning git repository
    print(f"Cloning {DATA_GIT_REPO} into {tmp_clone_dir}...")
    Repo.clone_from(DATA_GIT_REPO, tmp_clone_dir)
    print(f"Cloning {DATA_GIT_REPO} into {tmp_clone_dir}... successful")
    
    # Reading JSON files
    json_file_dir = os.path.join(tmp_clone_dir, DATA_JSON_PATH_IN_GIT_REPO)
    json_files = [json_file for json_file in os.listdir(json_file_dir) if json_file.endswith('.json')]
    print(f"Found {len(json_files)} JSON files in {json_file_dir}")
    
    # Copy JSON files over
    for json_file in json_files:
        # Copy files over
        src = os.path.join(tmp_clone_dir, DATA_JSON_PATH_IN_GIT_REPO, json_file)
        dst = os.path.join(json_storage_path, json_file)
        print(f"Copying {json_file} from {src} to {dst}...")
        shutil.copy2(src, dst)

        # Modify file content
        with open(dst) as f:
            data = json.load(f)
            # Modify image key to only contain the filename
            data["image"] = f"./{os.path.basename(data['image'])}"

        # Write new file content
        with open(dst, 'w') as fp:
            json.dump(data, fp, indent=4)

    # Copy images over
    # Right now we only do it oneway.
    # If a podcast updates its image, we don't delete the old one.
    # Dirty? Maybe. However, fast for now and the assumption is, that this
    # will not happen very often. If this assumption is wrong, we will update the
    # piece of code below.
    images_file_dir = os.path.join(tmp_clone_dir, DATA_IMAGES_PATH_IN_GIT_REPO)
    image_files = [image_file for image_file in os.listdir(images_file_dir) if not image_file.startswith(".")]
    print(f"Found {len(image_files)} image files in {images_file_dir}")

    for image_file in image_files:
        # Copy files over
        src = os.path.join(tmp_clone_dir, DATA_IMAGES_PATH_IN_GIT_REPO, image_file)
        dst = os.path.join(image_storage_path, image_file)
        print(f"Copying {image_file} from {src} to {dst}...")
        shutil.copy2(src, dst)

        # # Resize images
        # image_to_resize = Image.open(dst)
        # if image_to_resize.width > 700 and image_to_resize.height > 700:
        #     print(f"Resizing {image_file} from {image_to_resize.width}x{image_to_resize.height} to 700x700...")
        #     resized_image = image_to_resize.resize((700, 700))
        #     resized_image.save(dst)

    # # Copy OPML file over
    # # Existing files will be replaced.
    # src = os.path.join(tmp_clone_dir, DATA_OPML_FILE_PATH_IN_GIT_REPO)
    # print(f"Copying {src} to {opml_storage_path} ...")
    # shutil.copy2(src, opml_storage_path)
    # print(f"Copying {src} to {opml_storage_path} ... done")

    # Removing git clone
    print(f"Removing cloned repository from merged JSON file {tmp_clone_dir}...")
    shutil.rmtree(tmp_clone_dir)

    print("Aaaaand we are done")


def main():
    image_storage_path = os.path.join(SCRIPT_DIR, "..", DATA_IMAGE_STORAGE)
    json_storage_path = os.path.join(SCRIPT_DIR, "..", DATA_JSON_STORAGE)

    sync_podcasts(json_storage_path, image_storage_path)


if __name__ == "__main__":
    main()
