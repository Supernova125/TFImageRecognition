
# Introduction

This Project is my first try on using ai with image recognition. It uses the Keras module from TensorFlow to recognize which game the screenshot is from that is input into the system.

At the moment it only supports very few games because I haven't found the time to extend it massively but I plan on adding more and more features in the future.

# Getting started

This is a documentation of all this stuff here

## Feeding the training

You can feed images to the training by obtaining an mp4 or other video file of just gameplay (for better results) and then you can use `moviesplitter.py` to split it up into frames and automatically input them into `/game_images/{game-name}`. It recognizes the game by searching in the filename for any of the **currently registered** games!

## Creating a training package

The training will not just use all images in game_images because that would be way too much. Instead you can use `batcher.py` to split the folders up. You can go into the `batcher.py` file and change the amount of images you want. Then it chooses randomly which images to use. The result will be the specified amount of randomly selected images in (by default) `/imagebatch/`. This will then be used by `model.py`.

## Generating the model

Training and saving the model is easy after that. Just run `model.py` and the desired .keras file should be created.

## Using the model

If you want to use the model you can just use the just created .keras file and just like in the example `game_model_tester.py` import it into your project and use it like specified.

# Using the Importable module

When using the `gamerecognizer_module.py` you need to watch out for one thing: The prediction gives back an integer as the prediction which is the index of the folder.

If you have this in your `game_images`:
- minecraft
- valorant

Then `minecraft` would be 0 and `valorant` would be 1. 

So note down your games and the indexes of them when generating your model!