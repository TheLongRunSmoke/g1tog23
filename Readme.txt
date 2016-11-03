Processing script for making circles from segments.
Converting g1 to g2/g3 commands.

Needs python 2.7! Not worked with Python 3!

==========================================================

How to use

!! For windows users: fix paths in .cmd file !!
Don't forget quotes for paths containing spaces!

 * Simplify3D:

Edit Processes, Show Advanced options, go to Scripts tab,
find Post Processing, add next command to text field:

For linux and Mac users:
python /path/to/g1tog23/g1tog23.py "[output_filepath]"

For windows users:
c:\path\to\g1tog23\g1tog23.cmd "[output_filepath]"


 * Slic3r:

Go to Print Settings, switch to Output options tab,
add to Post-Processings scripts field:

For linux and Mac users:
python /path/to/g1tog23/g1tog23.py

For windows users:
c:\path\to\g1tog23\g1tog23.cmd


 * Other:

Find post-processing settings and add scripts to it.
