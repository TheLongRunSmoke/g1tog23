# G1toG2/3

Processing script for making circles from segments.
Converting g1 to g2/g3 commands.

## What's news

**v1.4**
 * Accuracy is slightly increased.
 * UI added.
 

**v1.3**
 * Migrate to Python3.
 * Windows binaries available.

## Install

#### **Windows only**
 
1. [**Download**](https://github.com/TheLongRunSmoke/g1tog23/releases) binaries from release section.
2. Unpack rar somewhere.

Or use source by follow.

#### **Windows, Linux or Mac**
 
1. Clone or download script.
2. Install Python, if you don't have it all ready.
3. Install requared lib:
```
pip install pyqt5
```

## How to use

**Attention!**
Don't forget quotes for paths containing spaces!

 * **Simplify3D**

Edit Processes, Show Advanced options, go to Scripts tab,
find Post Processing, add next command to text field:

For linux and Mac users:
```
python /path/to/g1tog23/g1tog23.py "[output_filepath]"
```

For windows users:
```
c:\path\to\g1tog23\g1tog23.exe "[output_filepath]"
```
or source:
```
python c:\path\to\g1tog23\g1tog23.py "[output_filepath]"
```


 * **Slic3r**

Go to Print Settings, switch to Output options tab,
add to Post-Processings scripts field:

For linux and Mac users:
```
python /path/to/g1tog23/g1tog23.py
```

For windows users:
```
c:\path\to\g1tog23\g1tog23.exe
```
or source:
```
python c:\path\to\g1tog23\g1tog23.py
```

 * **Other**

Find post-processing settings and add scripts to it.
