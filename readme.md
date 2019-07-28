# Pose Detection

In this project I used the [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation) which is openpose model in python. 
This mode return the joints of a person given a video or photo.

## How to use this repo

Clone this repo [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation). Then Paste all the code from this repo inside the cloned folder.
First make the database using the code present in `making database`. This will give you the position of joints. Then use the code in `create train test val` and get the distance between the joints, and create the train test and val files. Then run the keras model on these files and get the output.

## Database

Database is created by running this model on lot of videos and photos. Then the eular or cosine distance is calculated between joints and neck joint. Save all these values in a file, this will be our database.

## Training

A keras mode is used to train, you can find it in notebook section.

## Testing

You can test a video or photo using code in folder `testing`.

### Note -> you will see some places, I have flipped the videos it is only because, videos from my phone were inverted. Remove it if that is not the case.

## Output

<img src="video/output2.mp4" width="600">
