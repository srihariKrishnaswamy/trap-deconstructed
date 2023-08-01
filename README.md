# Trap Deconstructed: Analyzing Songs' BPM, Key, Mode and Feel 

This app uses PyTorch (for model building, training and evaluation), Python (for a Flask server & data manipulation) and React.js (frontend) to create a tool for music producers to learn certain characteristics about trap samples they hear or songs that they like, and give them a conceptual starting point on how to create a similar sound. As a producer myself, I've many times heard a song or a sample and thought, 'it'd be nice to make something in this key and bpm,' and then guess and check the key and bpm until I had lost my inspiration. So, this tool does all that work for us, leveraging the power of Machine Learning.

Simply press record, play whatever song or sample you want to analyze over a 10 second period, and watch as the Neural Networks & Transformers work their magic!

## How Does it Work
To start, a script records audio for 10 seconds within the frontend react app. This audio gets passed through a Flask server & saved to a .wav file. Then, a python script gets fired up from within the server that does a few things:
1. Deep Convolutional Neural Networks take the audio file and predict the samples key, mode and feel.
2. Using the librosa audio processing library, the sample's bpm is also predicted.
3. All these labels then get piped into Chat-GPT using the OpenAI API. Chat-GPT's response to create a similar sound is recorded.

All of these predictions and steps to create a similar sound are then passed back up to the react app, where the user learns about the song and can instantly get to work!

## The Development Process

Before I could start building models, I had to assemble a preliminary dataset. So, I set to work, labeling 200 of my favorite songs (and passing them through a script that randomly sliced them to 10x the samples) for their keys, modes and the feel of each song. I then built a CNN for the prediction of each of the 3 labels. After a couple weeks of iteration, changes to models' architectures and more and more data collection, I decided to hook the models' results up to the openai API. Soon after, I felt in a good enough spot to move on to front end work. 

During 4th of July weekend, I wrote out the front end of the app and the flask server. After hooking everything up, the inital rendition of 'Trap Deconstructed' was complete!

Iteration is still happening on the models. I want to get them to predict as accuractely as possible, and unfortunatley, training them on increasingly large dataset takes a lot of time. But, in the near future, I aim to fully close the door on this project!

As far as model stats, the key model predicts at about a 30% test accuracy, the mode model at 85%, and the feel model at 80%. There is improvement to be made, and I am still experimenting with different architectures and growing my dataset.

## Getting Started

This app will be deployed to the web in the near future!
