# 14 & 16 Nov 23 - Using the FFT with Real Data

Y'all have learned the main process for using an FFT on a 1D signal, so let's use it in the context of some real world data. We'll give you different kind of data that you can choose to work with: Transit light curve data and audio signals. Take a look at both datasets and start working on whichever one you'd like first.


## Transit Data

You work in a lab that is observing light curves to determine if there are transiting objects near a star and, if so, what is their period. Using the brightness of the star itself, we can determine it's mass and then it's a quick analysis to get the mass of the transiting objects (Thanks, Newton!).

In this activity, you have three data files that describe the CCD voltage on a sensor as a function of time. The observations were taken over a 48 hour period. You will need to read in the data, determine the sampling frequency, and then develop an FFT model to look into the frequency components.

<img src="https://images.newscientist.com/wp-content/uploads/2019/09/26122246/c0471894-rejuvenated_gas_giant_planet_illustration-spl.jpg" width=600px>

### Data Files

* [Observation 1](https://raw.githubusercontent.com/dannycab/phy415msu/main/MMIPbook/assets/data/FFT/obs1.csv)
* [Observation 2](https://raw.githubusercontent.com/dannycab/phy415msu/main/MMIPbook/assets/data/FFT/obs2.csv)
* [Observation 3](https://raw.githubusercontent.com/dannycab/phy415msu/main/MMIPbook/assets/data/FFT/obs3.csv)

The first data file is known to contain data from the observation of 2 transiting objects. Your lab mate misnamed the other two files, so it's not clear if they are the same set of observations or not.

Start with observation 1. You can use `pd.read` from the pandas library to read in the data.

**&#9989; Questions to answer**

For observation 1,

1. What does the FFT look like? Can you describe where the real observavtions might be in the plot?
2. Can you clean the noise from the data to find the real signal?
3. Can you estimate the transit times for the objects?

For observations 2 and 3,

1. Which one (or both or neither) observations are those of observation 1?
2. If there's a file with new observations, can you learn the same things as above?


```python
## your code here
```

## Audio Signals & Effects

A lot of audio processing boils down to taking the FFT of some audio signal, doing something to that frequency spectrum, the using the inverse FFT to get a new signal back with some effects on it. Here's some musical data to practice this:

Data:

 - Signal 1: [a single note played on a guitar](https://raw.githubusercontent.com/valentine-alia/phy415fall23/main/content/assets/note.wav)
 - Signal 2: [a chord played on a guitar](https://raw.githubusercontent.com/valentine-alia/phy415fall23/main/content/assets/chord.wav)
 - Signal 3: [metal riff without distortion](https://raw.githubusercontent.com/valentine-alia/phy415fall23/main/content/assets/riff.wav)
 - Signal 4: [a full track](https://raw.githubusercontent.com/valentine-alia/phy415fall23/main/content/assets/track.wav)

For some code to help you read-in and listen to the audio, refer to [yesterday's notes](https://dannycaballero.info/phy415fall23/content/3_waves/notes-Using-FFTs.html)

**&#9989; Questions to answer**

For signal 1:

1. What does the fourier transform of the signal look like? Does it have a lot of peaks?
2. What note is being played?

For signal 2:

1. What chord is being played (i.e. what are the individual notes?)
2. After taking the FFT of the data, try to get rid of the frequency components of the highest note in the chord then take the IFFT to see what the new signal sounds like. What do you notice?
3. Repeat 2. but for the lowest note.

For signal 3:

1. Without distortion, this metal riff sounds... kindof lame to be honest. Try adding distortion to the signal.

For signal 4:

1. Oftentimes in audio enginnering its useful to use an "equalizer" to boost or lessen certain frequencies in an audio signal to give it a different sound. Try cutting out all the frequencies above some threshold and see what it sounds like then. 
2. Try to isolate the synth bass from the rest of the signal. Is it possible to get a perfect separation?
3. At the begging of the track, you can hear that there is some effect on the guitars. Can you use the FFT to figure out what this effect is doing?




```python
## your code here
```
