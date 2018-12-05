# CQplot - Automatically measure code-quality progression

CQplot automatically finds every .py and .pywn file in a given codebase,
hereafter it uses pylinter, to score the files. And then it collects the date which the file was lastly modified.

This data is used to create a 2D scatterplot using matplotlib.