# Shape Drawer
## A simple shape creator 

Draws shapes by defining connections between points. Shapes can be saved as a text file. **File Schema** specifed below.
### Supports
- Straight Edges 
- Bezier Curves

## Shape File Schema
Each shape file contains **strings** delimited by **newlines** `\n` without other whitespaces. Each element is either: 
+ *2* numbers delimited by `,` representing  a **shape's vertex** 
Example: `"x,y"` => `P = (x,y)` 
+ *4* numbers delimited by `,` representing the **2 control points of a bezier curve**
+ Example: `"w,x,y,z"` =>  `C1 = (w,x), C2 = (y,z)`

## Usage
```
./main.py
```

## Shape Creater Controls
TODO lol
