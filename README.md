
# Project focusMonitor



## Installation

Clone the repo into a folder\
Install python requirements\
It is recommended to create a virtualenv
```bash
  cd Hacktech-2022-master/
  pip install -r requirements.txt
```

Edit config.json:
- replace MAGE_KEY with your MAGE API key
- replace MAGE_MODEL with your model name
(To be replaced with custom middleware API)

Run app.py
```bash
  python app.py
```

In the future there will be an installable file for all users.


    
## Requirements
```py
certifi
charset-normalizer
cycler
desktop-notifier
fonttools
idna
keyboard
kiwisolver
matplotlib
mouse
numpy
packaging
pandas
Pillow
pyparsing
pyqtgraph
PySide6
python-dateutil
pytz
requests
rubicon-objc
shiboken6
six
urllib3
zroya
```

## Inspiration
With all of us staying home on the computer all day so frequently in this era, we found it more important than ever to 
maintain productivity despite all the distractions we might have. The idea of focusMonitor stemmed from this, and grew 
into a more overarching ability to analyze how we work in the hopes of achieving greater productivity- without losing 
the original feature of reminders to get back on track if we lose focus.

## What it does
The app collects information about the frequency of key presses every minute and requests a prediction from MAGE AI's 
API about whether the data reflects 'distracted' or 'focused' behavior. If you seem to be distracted for a few minutes, 
it sends you a gentle reminder to get back to work, and allows you to give it feedback by telling it if you're not 
actually distracted. There's also a user interface that allows you to see real-time updating analytics of your focus, 
so you can see how well you've been focusing.

## How we built it
We created a number of python files to manage smaller portions of the code, and used GitHub to collaborate and post 
updates as we worked on separate pieces of code. Once we set up the data collection process and notification systems, 
we generated data, then worked on integrating the functions we built while getting the MAGE AI API set up. Finally, we 
bug-tested and put together the rest of the pieces so we could run through a cohesive demonstration of the product.

## Challenges we ran into
There were a number of challenges to overcome, including but not limited to cross-platform troubles as some of our team 
use primarily Windows and others Mac, difficulty setting up and properly formatting data collection, and finding ways 
of handling unusual keys and other bugs that would crash the collection program.

## Accomplishments that we're proud of
Our MAGE setup fairly effectively judges distracted and not-distracted behavior for the minimal training data we were 
able to create in the timeframe, and we managed to solve a large number of compatibility issues to ensure that the 
project would be both usable and useful to all members of the project after the hackathon ends.

## What we learned
We learned a lot about MAGE AI, cross-platform compatibility development, and the notifications systems for Mac and 
Windows during this project.

## What's next for focusMonitor
We have a large number of improvements we discussed making, including addition of mouse data for further effectiveness 
in classifying data, and the possibility of detecting more specifically what 'distracting' or 'focused' activities were 
taking up time. This would allow users to better understand where their time is going, as well as increase the accuracy 
of detecting distracted behavior.

## Authors

- [Eli Fischl](https://github.com/Vio-Eli/)
- [Luc Davis](https://github.com/Kratargon)
- [Ryan O'Dell](https://github.com/Midnight145/)

