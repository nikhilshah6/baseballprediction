Project Purpose: To classify what pitch a baseball pitcher has thrown given video data of their pitch with a tracer added on. I’ve grown up watching baseball and solving this problem would be 
something that I would be pretty motivated to figure out. I’ve switched to only analyzing a single pitcher (Max Scherzer) to decrease variability between the definitions of pitches. Max Scherzer's
curve is going to look different than Logan Webb's. 

Dataset: I created a scraper provided in this repo (vidScraper2.py) to pull video data from baseballsavant.mlb.com. Essentially I used a chrome extension to gather all on-screen info of the webpage after running
a query for all Max Scherzer's pitches in 2018. This info was gathered in a google sheet which I then cleaned to contain isolated URLs to the videos corresponding to each pitch. I then used
this repo-- https://github.com/chonyy/ML-auto-baseball-pitching-overlay to add tracers to each video that I had gathered. I then validated all these pitching sequences with data from Kaggle detailing all the
pitches in the 2018 MLB season-- https://www.kaggle.com/datasets/pschale/mlb-pitch-data-20152018. Using that I was able to create my dataset.

How to Train Model: I used a collate function to add padding to each video to match the video with maximum frames per batch size to ensure each tensor was the same size. I also downsized the resolution of each video to use less memory while training which you can see in the resize_video_tensor function in loader.ipynb. At this point, I created my train/test/validation split  and created my data loaders. I had to use a low batch size of 2 in order to use less memory as well. I then loaded in the 3D RESNET model (r3d18), froze the weights and added the classification head. I refrained from adding any activation, pooling, or extra convolutional layers in order to save compute as my training loop would crash my kernel. 

Result Evaluation: At the baseline I used accuracy to evaluate my model which came at around 52.33%. This could definitely be higher given more epochs and more optimized use of memory. However, when taking a closer look at the confusion matrix, we can see that the model only predicted fastballs, which is what Max Scherzer also happens to throw about 45% of the time. When looking at other iterations of training, we can see that Scherzer's pitch that is most unlike the FF is his CU because of its large vertical break. When the model decides to start making other guesses, the accuracy dramatically decreases. This is most likely due to the impreciseness of the tracers that were added onto each pitch. <img width="616" alt="Screen Shot 2025-03-14 at 8 50 04 PM" src="https://github.com/user-attachments/assets/f7865614-ba73-48a6-8fbd-414aaa515214" />

This is why despite having a decent accuracy score the precision and f1 scores are much lower.
<img width="171" alt="Screen Shot 2025-03-14 at 8 54 18 PM" src="https://github.com/user-attachments/assets/4676590e-bd4b-4f8e-ac1b-742dc9ac1d47" />
<img width="951" alt="Screen Shot 2025-03-14 at 8 54 31 PM" src="https://github.com/user-attachments/assets/5b39e697-24f0-4f5d-ac23-6b0fc9cde575" />

Note: models.py, dataset.py, train_models.py equivalents are all aggregrated in loader.ipynb. This is within baseballprediction/pitchclassifier
