Hi there, this project was made way back my last semester in college. This project is a desktop based application to be compatbile for raspberry pi 3b. Basically this project is design to diagnose tooth cavity severity. The algorithm of this program was very hackish which later be explain.

## Dependencies:
- Kivy
- MySQLdb
- Google Cloud API (Vision)
- OpenCV
- Numpy
- Matplotlib
- Request

## Software Design

![alt text][logo5]

[logo5]: https://github.com/AbadJoshuaD/iSmile/blob/master/readmeimages/softwaredesign.png "Software Design Image"



My team used an intra oral camera to capture image of patient tooth and diagnose its tooth cavity severity using our algorithm. Like what I have said the algorithm was hackish, I used 2 API for this project for diagnosing tooth cavity. The first API I used was Google Vision API. I utilze the power of google vision api training datasets to identify if the captured image was indeed a tooth image. It is really hard to do validation on this project since the scarcity for training a dataset that could provide accurate label to the image specially tooth image was nearly non existent therefore I used google vision API. The vision api was indeed helpful for image classification and label detection. 

Upon validating the image, the next process the image undergo through api called Nanonets. Nanonets is ML api that can do classification machine learning modelling. I used this API to train the images based on their severity such as normal,moderate and severe. Each model contains about 250+ images of classified images by a professional dentist. Upon completing the training, the model can classify the images correctly 75% of the time based on our testing.  Then the classified result was displayed using Kivy as GUI interface for python desktop application and stored result on a simple backend setup I made on MySQL.

## Key Features
- Capture image using Intra Oral Camera

![alt text][logo]

[logo]: https://github.com/AbadJoshuaD/iSmile/blob/master/readmeimages/capture.jpg "Capture Image"


- Diagnose tooth severity
![alt text][logo1]

[logo1]: https://github.com/AbadJoshuaD/iSmile/blob/master/readmeimages/diagnose.png "Diagnose Image"

- Display Patient Record
![alt text][logo2]

[logo2]: https://github.com/AbadJoshuaD/iSmile/blob/master/readmeimages/patientrecord.png "Patient Record Image"

- Diagnosis Record
![alt text][logo3]

[logo3]: https://github.com/AbadJoshuaD/iSmile/blob/master/readmeimages/diagnosisrecord.png "Diagnosis Record Image"

- Dental Chart
![alt text][logo4]

[logo4]: https://github.com/AbadJoshuaD/iSmile/blob/master/readmeimages/dentalchart.png "Dental Chart Image"



## Conclusion
Although this project was very hackish and the code was pure garbage(ahahahaha :) ), I have learned a lot from doing this project specially building system from scratch and learning new technology. My team chooses this project since we are all embedded systems major. Most of our programming subjects we're about micro computers and controller such as raspberry pi and arduino. Before this project, I never have a keen interest on learning programming deeply. But after doing this project, it piques my interest on building things and being able to actually see the actual product was indeed satisfying. After this project I pour some of my time on learning programming until recently I decided to learn full stack web development full time.

## Final Prototype Look

![alt text][logo6]

[logo6]: https://github.com/AbadJoshuaD/iSmile/blob/master/readmeimages/finaldesign.jpg "Final Design Image"
