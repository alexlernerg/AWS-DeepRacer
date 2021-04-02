# AWS-DeepRacer
Self Driving Car built for AWS DeepRacer competition

### What is AWS DeepRacer?
<em> AWS DeepRacer is an integrated learning system for users of all levels to learn and explore reinforcement learning and to experiment and build autonomous driving applications. It consists of the following components:

An AWS Machine Learning service to train and evaluate reinforcement learning models in a simulated autonomous-driving environment.

AWS DeepRacer 1/18th scale RC vehicles capable of running inference on a trained AWS DeepRacer model for autonomous driving.

AWS DeepRacer for the participants to compete on model performances on a specific track in a simulated or real environment and have the results ranked on a virtual or physical leader board. </em>

To build the model and compete two main AWS services were used:

<strong>AWS Robomaker</strong>: Provides an environment to simulate and test our application in a 3d world with virtual tracks and a car to race.

<strong>AWS Sagemaker</strong>: Provides a training environment for the Reinforcement Learning model. It takes the image taken from the car as the input paramenter and returns an action as an output. These actions will determine the driving style of the car allowing it to race quickly around corners and, win!

### How does my model work? 
Multiple parameters were provided by AWS to train the car. The full list can be found at: https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html

After playing with different parameters and suprisingly failing to get the secret sauce working, I decided to use the steering direction of the car. The scoring function worked as follows:

1) Get a circle with fixed radius surrounding the car.
2) Find the intersection of the circle with the central line of the track.
3) Steer the car towards this point. If the car achieves this direction the reward is increased. The further away it looks from the desired angle the lower the reward.

![image](https://user-images.githubusercontent.com/80718396/113424274-c9e5fd00-93c7-11eb-93cd-7a48ddd55139.png)

The radius of the circle was adjusted depending on what track it was competing in and how wide the corners were. And that is it, got the secret sauce finishing top 10 worldwide!

![image](https://user-images.githubusercontent.com/80718396/113424671-72945c80-93c8-11eb-9c4e-08c84fa4da43.png)


### Was it a good idea?
For the first 20 minutes I didn't even manage to finish a full lap... Then the car started to get used to the environment and completes it's first lap! 5 minutes after the car got the hang of it and completed 50 consecutive laps without a single crash. This was the first time I managed to get the model working consistently without fail in less time, but why?

![image](https://user-images.githubusercontent.com/80718396/113425072-23026080-93c9-11eb-994f-b331c3f84d32.png)

We can see that after just 42 attempts the model learned to follow the track with a 100% success rate. This show. This is becuase Reinforcement Learning is all about rewarding good behaviour from early on. For example, imagine you are trying to get your dog to do a trick. If it does it, you reward him/her with a treat immediately and after multiple repetition it has learned to do it!

This is essentially the same with DeepRacer. When it points to the correct direction, the image tells the algorithm it's a good action and gives it a reward. 

I also attempted to cut corners, as travelling less distance helps the car travel faster along the track. Other benefits werer achieved as this reduced the risk of running away from the track and makes it easier to keep an eye on the desired path.
