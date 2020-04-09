**egm**
******************************

**Evidence Gap Maps(egm)** are useful for visualizing research gaps. This library (extension of the [Bubbly]( https://github.com/AashitaK/bubbly) package) provides interactive and animated charts using *Plotly*, useful for plotting reasearch papers. The animated bubble charts can accommodate multiple variables viz. X-axis, Y-axis, time, bubbles (the research artifacts of title , abstract and doi) their size (similarity to research question) and their color in a compact and captivating way. Evidence Gap Maps (egm) python package is easy to use with plenty of customization, and is designed to work with ``plotly``'s offline mode useful in Jupyter Notebooks, Google Colab and Kaggle kernels. 

egm package can also be useful in making a plot where two catagorical variable are to be plotted aganst each other as bins.

Dependencies
------------
* Python 3.x
* numpy
* pandas 
* plotly

Installation
-------------
pip install egm

**Modes**
----------------------------
There are two modes supported. Time can be included in both modes for a dynamic year wise plot. 

**1. Mode Random**

The random mode is more display friendly and the plot in a bin is scattered evenly.  

figure = **evidencegapmap**(dataset=pd, x_column='x', y_column='y',
  bubble_column='title_column',bubble_text='bubbletext_column', bubble_link='bubblelink_column', size_column='size_column', color_column='color_column',xbin_list=<list1>, ybin_list = <list2>,
  xbin_size=100, ybin_size = 100, x_title="X Axis Title", y_title="Y Axis Title", title='Evidence Gap Map for XYZ',scale_bubble=4, marker_opacity=0.8,height=900, width=1200)

*iplot(figure)*
  
![Random Mode](./egm.png?raw=true "Random Mode")
 

 **2. NLP Mode**
   
For the NLP mode, x and y coordinates are provided arrays and are transformed and plotted in the bin. The mode is useful for displaying the similarity and disimilarity of research papers

 *figure = **evidencegapmap**(dataset=pd, x_column='x', y_column='y',xy_column='xy_column',
  bubble_column='title_column',bubble_text='bubbletext_column', bubble_link='bubblelink_column', time_column='publish_year', size_column='size_column', color_column='color_column',xbin_list=<list1>, ybin_list = <list2>,
  xbin_size=100, ybin_size = 100, x_title="X Axis Title", y_title="Y Axis Title", title='Evidence Gap Map for XYZ',scale_bubble=4, marker_opacity=0.8,height=900, width=1200)*
  
 *iplot(figure)*

![NLP Mode](./egm.gif?raw=true "NLP Mode")

Usage in a Notebook & Example 
----------------------------

Refer to this [collab notebook](https://shorturl.at/gwCZ6) for a basic working example with [sample data](https://github.com/mb7419/egm/blob/master/egmsample.csv) 


View an end to end working example [here](https://www.kaggle.com/uplytics/evidence-gap-map-for-risk-areas)





