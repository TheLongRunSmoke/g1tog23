# G1toG2/3

Processing script for making circles from segments.
Converting g1 to g2/g3 commands.

~~Needs python 2.7! Not worked with Python 3!~~</br>
Now work well with 3.6 at least.

## How to use

**Attention!**
Don't forget quotes for paths containing spaces!

 * Simplify3D:

Edit Processes, Show Advanced options, go to Scripts tab,
find Post Processing, add next command to text field:

For linux and Mac users:
```
python /path/to/g1tog23/g1tog23.py "[output_filepath]"
```

For windows users:
```
python c:\path\to\g1tog23\g1tog23.py "[output_filepath]"
```

 * Slic3r:

Go to Print Settings, switch to Output options tab,
add to Post-Processings scripts field:

For linux and Mac users:
```
python /path/to/g1tog23/g1tog23.py
```

For windows users:
```
python c:\path\to\g1tog23\g1tog23.py
```

 * Other:

Find post-processing settings and add scripts to it.
