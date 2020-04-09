**egm**
******************************

**Evidence Gap Maps(egm)** are useful in research for plotting research gaps for a research area. This library (extension of the [Bubbly]( https://github.com/AashitaK/bubbly) package) provides interactive and animated charts using *Plotly* that can be useful to view reasearch gaps and tracking time based progress of relevant research. The animated bubble charts can accommodate up to six variables viz. X-axis, Y-axis, time, bubbles (the research artifacts of title , abstract and doi) their size (similarity to research question) and their color in a compact and captivating way. Evidence Gap Maps are easy to use with plenty of customization, especially suited for use in Jupyter notebooks and is designed to work with ``plotly``'s offline mode such as in Kaggle kernels. 

In general egm package can be useful in making a plot where two catagorical variable are plotted aganst each other and creates bins.

Dependencies
------------
* Python 3.4+
* numpy
* pandas 
* plotly

Installation
-------------
pip install egm

  
Usage in a Jupyter Notebook
----------------------------

**Modes**
----------------------------
**1** There are two modes supported. Time can be included in both modes for a dynamic year wise plot. The random mode is more display friendly and the plot in a bin is scattered evenly. 


**Mode Random**

from __future__ import division

from plotly.offline import init_notebook_mode, iplot

init_notebook_mode()

figure = **evidencegapmap**(dataset=pd, x_column='x', y_column='y',
  bubble_column='title_column',bubble_text='bubbletext_column', bubble_link='bubblelink_column', size_column='size_column', color_column='color_column',xbin_list=<list1>, ybin_list = <list2>,
  xbin_size=100, ybin_size = 100, x_title="X Axis Title", y_title="Y Axis Title", title='Evidence Gap Map for XYZ',scale_bubble=4, marker_opacity=0.8,height=900, width=1200)

iplot(figure)
  
![Random Mode](./egm.png?raw=true "Random Mode")
  
**2** The NLP mode, x and y coordinates are provided and are transformed and plotted in the bin. The mode is useful for displaying the similarity and disimilarity of points
 
 **NLP Mode**
 
from __future__ import division

from plotly.offline import init_notebook_mode, iplot

init_notebook_mode()

 figure = **evidencegapmap**(dataset=pd, x_column='x', y_column='y',xy_column='xy_column',
  bubble_column='title_column',bubble_text='bubbletext_column', bubble_link='bubblelink_column', time_column='publish_year', size_column='size_column', color_column='color_column',xbin_list=<list1>, ybin_list = <list2>,
  xbin_size=100, ybin_size = 100, x_title="X Axis Title", y_title="Y Axis Title", title='Evidence Gap Map for XYZ',scale_bubble=4, marker_opacity=0.8,height=900, width=1200)
  
 iplot(figure)

![NLP Mode](./egm.gif?raw=true "NLP Mode")


View a working example [here](https://www.kaggle.com/uplytics/evidence-gap-map-for-risk-areas)





