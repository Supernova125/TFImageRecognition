import pathlib, os, random
from shutil import rmtree, copy
from toml import load as tload

config = tload('config.toml')

print("Starting batcher...")
print("Clearing folder...")
# empty whole folder
if os.path.exists(config["batcher"]["batch_folder_name"]):
    rmtree(config["batcher"]["batch_folder_name"])
    os.makedirs(config["batcher"]["batch_folder_name"])

print("Finding images...")
data_dir = pathlib.Path('game_images').with_suffix("")
image_count = len(list(data_dir.glob('*/*.jpg')))
print(str(image_count) + " images found")

tar_image_count = config["batcher"]["tar_image_count"]

image_chance = tar_image_count / image_count

print("\nChance: " + str(image_chance))
print("Batch size: " + str(tar_image_count))
print("All count: " + str(image_count))
print("Starting to copy...")

# Iterate over each image in the data_dir and randomly decide whether to copy it
copiedfiles = 0
for image_path in data_dir.glob('*/*.jpg'):
    if random.random() < image_chance:
        destination_dir = pathlib.Path(config["batcher"]["batch_folder_name"]) / image_path.parent.relative_to(data_dir)
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination_path = destination_dir / image_path.name
        #image_path.replace(destination_path)
        # copy
        copy(image_path, destination_path)
        copiedfiles += 1

print("Done!")
print("Copied: " + str(copiedfiles))
input()