**egm**
******************************

**Evidence Gap Maps(egm)** are useful in research for plotting research gaps for a research area. This library (extension of the [Bubbly]( https://github.com/AashitaK/bubbly) package) provides interactive and animated charts using *Plotly* that can be useful to view reasearch gaps and tracking time based progress of relevant research. The animated bubble charts can accommodate up to six variables viz. X-axis, Y-axis, time, bubbles (the research artifacts of title , abstract and doi) their size (similarity to research question) and their color in a compact and captivating way. Evidence Gap Maps are easy to use with plenty of customization, especially suited for use in Jupyter notebooks and is designed to work with ``plotly``'s offline mode such as in Kaggle kernels. 

In general egm package can be useful in making a plot where two catagorical variable are plotted aganst each other and creates bins.

Dependencies
------------
* Python 3.7+
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
There are two modes supported. In the random mode is more user friendly and points are scattered randomly (evenly) in a bin. 
![Random Mode](./egm.png?raw=true "Random Mode"). Time can be included in both modes for a dynamic year wise plot.

*Mode Random*
figure = evidencegapmap(dataset=pd, x_column='x', y_column='y',
  bubble_column='title_column',bubble_text='bubbletext_column', bubble_link='bubblelink_column', size_column='size_column', color_column='color_column',xbin_list=<list1>, ybin_list = <list2>,
  xbin_size=100, ybin_size = 100, x_title="X Axis Title", y_title="Y Axis Title", title='Evidence Gap Map for XYZ',scale_bubble=4, marker_opacity=0.8,height=900, width=1200)
iplot(figure)
  
In the NLP mode the x and y coordinates provided are transformed into the bin so that they distribution indicates similarity and disimilarity.
![NLP Mode](./egm.gif?raw=true "NLP Mode")
 
 *NLP Mode*
 figure = evidencegapmap(dataset=pd, x_column='x', y_column='y',xy_column='xy_column',
  bubble_column='title_column',bubble_text='bubbletext_column', bubble_link='bubblelink_column', time_column='publish_year', size_column='size_column', color_column='color_column',xbin_list=<list1>, ybin_list = <list2>,
  xbin_size=100, ybin_size = 100, x_title="X Axis Title", y_title="Y Axis Title", title='Evidence Gap Map for XYZ',scale_bubble=4, marker_opacity=0.8,height=900, width=1200)


View a working example [here](https://www.kaggle.com/uplytics/evidence-gap-map-for-risk-areas)





