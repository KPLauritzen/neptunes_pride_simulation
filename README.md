# Finding (near-)optimal starting moves for [Neptune's Pride](https://np.ironhelmet.com)

Inspired by [this post]( http://www.kotaku.com.au/2014/03/how-i-broke-neptunes-pride-2/ ) which led me to a [series of posts on optimizing decisions in games](http://intelligenceengine.blogspot.com/2013/07/decision-modeling-and-optimization-in.html).

## Installation
Requires `numpy` and `deap`. Both should be available with `pip install numpy deap`.

## Usage
Open `genetic_algorithm.py` and edit the initial conditions in the `setup_test_player` function.
Then run `python genetic_algorithm.py` and examine the results.

The final output is a list of actions to take each day to maximize the number of ships produced.
