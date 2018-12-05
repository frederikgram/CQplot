# CQplot - Automatically measure code-quality progression

CQplot automatically finds every .py and .pywn file in a given codebase,
hereafter it uses pylinter, to score the files. And then it collects the date which the file was lastly modified.

This data is used to create a 2D scatterplot using matplotlib.

# Installation
```
> git clone http://github.com/frederikgram/CQplot
> pip install -r requirements.txt
```

# Usage

```
> Python cq_plot.py path_to_codebase (Defaults to current path)
>>> Average score: X/10
2D Plot
````

# Example

WIP