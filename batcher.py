import pathlib, random
from shutil import rmtree, copy
from toml import load as tload

config = tload('config.toml')

print("Starting batcher...")
print("Clearing folder...")
# empty whole folder
if pathlib.Path(config["batcher"]["batch_folder_name"]).exists():
    rmtree(config["batcher"]["batch_folder_name"])
pathlib.Path(config["batcher"]["batch_folder_name"]).mkdir(parents=True, exist_ok=True)

print("Finding images...")
data_dir = pathlib.Path('game_images').with_suffix("")
image_count = len(list(data_dir.glob('*/*.jpg')))
print(str(image_count) + " images found")

tar_image_count = config["batcher"]["tar_image_count"]

image_chance = tar_image_count / image_count

games = list(x.name for x in pathlib.Path("game_images").iterdir())
imgs_per_game = int(tar_image_count / len(games))

print("\nGlobal Chance: " + str(image_chance))
print("Batch size: " + str(tar_image_count))
print("Per Game: " + str(imgs_per_game))
print("All Imgs: " + str(image_count))
print("Starting to copy...")

# Iterate over each image in the data_dir and randomly decide whether to copy it
copiedfiles = 0
for game in games:
    print("Copying to " + str(config["batcher"]["batch_folder_name"]) + "/" + str(game))
    imgs = list(x for x in pathlib.Path("./game_images/"+game).iterdir() if x.name.endswith(".jpg"))
    print("Found " + str(len(imgs)) + " images for " + str(game))
    if len(imgs) == 0:
        continue
    local_chance = imgs_per_game / len(imgs)
    #print("Chance: " + str(local_chance))
    local_copied = 0
    while local_copied < imgs_per_game and local_copied < len(imgs): # prevents too small folders having multiple same imgs
        for image_path in imgs:
            if local_copied >= imgs_per_game:
                break
            if random.random() < local_chance:
                destination_dir = pathlib.Path(config["batcher"]["batch_folder_name"]) / image_path.parent.relative_to(data_dir)
                destination_dir.mkdir(parents=True, exist_ok=True)
                destination_path = destination_dir / image_path.name
                # copy
                copy(image_path, destination_path)
                copiedfiles += 1
                local_copied += 1
    print("Copied " + str(local_copied) + " images to " + str(config["batcher"]["batch_folder_name"]) + "/" + str(game))

print("Done!")
print("Copied " + str(copiedfiles) + " images to " + str(config["batcher"]["batch_folder_name"]))
input()