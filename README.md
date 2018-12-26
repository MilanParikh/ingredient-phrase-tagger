# CRF Ingredient Phrase Tagger

[![Build Status](https://travis-ci.org/mtlynch/ingredient-phrase-tagger.svg?branch=master)](https://travis-ci.org/mtlynch/ingredient-phrase-tagger) [![Docker Pulls](https://img.shields.io/docker/pulls/mtlynch/ingredient-phrase-tagger.svg?maxAge=604800)](https://hub.docker.com/r/mtlynch/ingredient-phrase-tagger/) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE.md)

## Fork Notes

This is a fork of the original [NY Times ingredient-phrase-tagger](https://github.com/NYTimes/ingredient-phrase-tagger). This fork is maintained by [Michael Lynch](https://github.com/mtlynch)

This fork maintains the design of the original ingredient-phrase-tagger, but adds bugfixes and additional features to aid in future development:

* Adds a [Docker image](https://hub.docker.com/r/mtlynch/ingredient-phrase-tagger/) for easy deployment.
* Adds a [continuous integration build](https://travis-ci.org/mtlynch/ingredient-phrase-tagger) on every check-in.
* Adds unit tests.
* Adds end-to-end tests.
* Enforces rules for source formatting and linting.

These improvements were described in a series of blog posts on [mtlynch.io](https://mtlynch.io):

* [Resurrecting a Dead Library: Part One - Resuscitation](https://mtlynch.io/resurrecting-1/)
* [Resurrecting a Dead Library: Part Two - Stabilization](https://mtlynch.io/resurrecting-2/)
* [Resurrecting a Dead Library: Part Three - Rehabilitation](https://mtlynch.io/resurrecting-3/)

## Zestful

[Zestful](https://zestfuldata.com) is a managed ingredient-parsing service based on this library. It has higher accuracy and more frequent updates:

* https://zestfuldata.com

## Overview

This repo contains scripts to extract the Quantity, Unit, Name, and Comments
from unstructured ingredient phrases. We use it on [Cooking][nytc] to format
incoming recipes. Given the following input:

    1 pound carrots, young ones if possible
    Kosher salt, to taste
    2 tablespoons sherry vinegar
    2 tablespoons honey
    2 tablespoons extra-virgin olive oil
    1 medium-size shallot, peeled and finely diced
    1/2 teaspoon fresh thyme leaves, finely chopped
    Black pepper, to taste

Our tool produces something like:

    {
        "qty":     "1",
        "unit":    "pound"
        "name":    "carrots",
        "other":   ",",
        "comment": "young ones if possible",
        "input":   "1 pound carrots, young ones if possible",
        "display": "<span class='qty'>1</span><span class='unit'>pound</span><span class='name'>carrots</span><span class='other'>,</span><span class='comment'>young ones if possible</span>",
    }

We use a conditional random field model (CRF) to extract tags from labelled
training data, which was tagged by human news assistants. We wrote about our
approach [on the New York Times Open blog][openblog]. More information about
CRFs can be found [here][crf_tut].

On a 2012 Macbook Pro, training the model takes roughly 30 minutes for 130k
examples using the [CRF++][crfpp] library.

## Development

On OSX:

```bash
brew install crf++
python setup.py install
```

Docker:

```bash
docker pull mtlynch/ingredient-phrase-tagger
```

## Quick Start

The most common usage is to train the model with a subset of our data, test the
model against a different subset, then visualize the results. We provide a shell
script to do this, at:

    ./roundtrip.sh

You can edit this script to specify the size of your training and testing set.
The default is 20k training examples and 2k test examples.


## Usage

### Training

To train the model, we must first convert our input data into a format which
`crf_learn` can accept:

    bin/generate_data --data-path=input.csv --count=1000 --offset=0 > tmp/train_file

The `count` argument specifies the number of training examples (i.e. ingredient
lines) to read, and `offset` specifies which line to start with. There are
roughly 180k examples in our snapshot of the New York Times cooking database
(which we include in this repo), so it is useful to run against a subset.

The output of this step looks something like:

    1            I1      L8      NoCAP  NoPAREN  B-QTY
    cup          I2      L8      NoCAP  NoPAREN  B-UNIT
    white        I3      L8      NoCAP  NoPAREN  B-NAME
    wine         I4      L8      NoCAP  NoPAREN  I-NAME

    1/2          I1      L4      NoCAP  NoPAREN  B-QTY
    cup          I2      L4      NoCAP  NoPAREN  B-UNIT
    sugar        I3      L4      NoCAP  NoPAREN  B-NAME

    2            I1      L8      NoCAP  NoPAREN  B-QTY
    tablespoons  I2      L8      NoCAP  NoPAREN  B-UNIT
    dry          I3      L8      NoCAP  NoPAREN  B-NAME
    white        I4      L8      NoCAP  NoPAREN  I-NAME
    wine         I5      L8      NoCAP  NoPAREN  I-NAME

Next, we pass this file to `crf_learn`, to generate a model file:

    crf_learn template_file tmp/train_file tmp/model_file


### Testing

To use the model to tag your own arbitrary ingredient lines (stored here in
`input.txt`), you must first convert it into the CRF++ format, then run against
the model file which we generated above. We provide another helper script to do
this:

    python bin/parse-ingredients.py input.txt > results.txt

The output is also in CRF++ format, which isn't terribly helpful to us. To
convert it into JSON:

    python bin/convert-to-json.py results.txt > results.json

See the top of this README for an example of the expected output.


## Authors

* [Erica Greene][eg]
* [Adam Mckaig][am]
* [Michael Lynch](https://github.com/mtlynch)


## License

[Apache 2.0][license].


[nytc]:     http://cooking.nytimes.com
[crf_tut]:  http://people.cs.umass.edu/~mccallum/papers/crf-tutorial.pdf
[crfpp]:    https://taku910.github.io/crfpp/
[openblog]: http://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/?_r=0
[eg]:       mailto:ericagreene@gmail.com
[am]:       http://github.com/adammck
[license]:  https://github.com/NYTimes/ingredient-phrase-tagger/blob/master/LICENSE.md
