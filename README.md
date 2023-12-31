https://github.com/hansel67/psyloop/assets/16061901/a9e90678-d06d-4fea-b11c-87d9300d1271

# PsyLoop
Tkinter window to preview and render versatile fractal animation mp4s with a single input function.

The output should be in the form of a triplet $(R,G,B)$ of floats in $[0,1]$. Built-in colormaps convert real numbers to $(R,G,B)$ triplets.

Settings:
* height $h$ px
* width $w$ px
* framerate $fps$ fps
* duration $duration$ sec

Variables:
* $x\in[-w/h,w/h]$
* $y\in[-1,1]$
* $t\in[0,1]$
* $z=x+yi$
* $r=|z|\in\left[0,\sqrt{(w/h)^2+1}\right]$
* $\text{th}=\frac{\text{arg}(z)}{2\pi}\in[0,1)$

Operators for $\mathbb C$:
* $+,-,*,/,%,\text{pow}(-,-)$
* $z\text{.real}$ and $z\text{.imag}$

Functions:
* $\text{sin},\text{cos},\text{tan}$
* $\text{exp},\text{log}$
* $\text{abs},\text{angle},\text{minimum},\text{maximum},\text{floor},\text{ceil}$
* $\text{arcsin},\text{arccos},\text{arctan},\text{arctan2},\text{sinh},\text{cosh},\text{tanh}$

Colormaps:
* $\text{gray},\text{prism}$
