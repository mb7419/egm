import numpy as np
import pandas as pd

def evidencegapmap(dataset, x_column, y_column, xy_column=None, bubble_column=None, bubble_text=None, bubble_link=None, time_column=None, size_column=None, color_column=None,   
               xbin_list=None, ybin_list=None,xbin_size=100, ybin_size=100, x_title=None, y_title=None, title=None, colorbar_title=None,
               scale_bubble=10, colorscale=None, marker_opacity=None, marker_border_width=None,show_slider=True, show_button=True, show_colorbar=True, show_legend=None, 
               width=None, height=None):
    ''' Makes the animated and interactive bubble charts from a given dataset.'''
    
    # Initialize the number of bins 
    xbin_range = [0,(len(xbin_list)-1)]
    ybin_range = [0,(len(ybin_list)-1)]
    #Initialize Axes range                                  
    x_range=[0,0] 
    y_range=[0,0]
    # Set category_column as None and update it as color_column only in case
    # color_column is not None and categorical, in which case set color_column as None
    category_column = None
    if color_column: # Can be numerical or categorical
        if dataset[color_column].dtype.name in ['category', 'object', 'bool']:
            category_column = color_column
            color_column = None
    # Set the plotting mode for the plots inside a cell
    if xy_column :
        mode = 'nlpmode'
        xmax = max(map(lambda xy: xy[0], list(dataset[xy_column])))
        xmin = min(map(lambda xy: xy[0], list(dataset[xy_column])))
        ymax = max(map(lambda xy: xy[1], list(dataset[xy_column])))
        ymin = min(map(lambda xy: xy[1], list(dataset[xy_column])))
        xshift = (xmax + xmin)/2
        yshift = (ymax + ymin)/2
        xy_scale= max(xmax-xmin, ymax-ymin)
        #print("xmax {}, xmin {}, ymax {}, ymin {}, xshift {}, yshift {} xy_scale {}".format(xmax, xmin, ymax, ymin, xshift, yshift, xy_scale))
    else :
        mode = 'randommode'
        xy_scale = 1
        xshift=yshift =0
    
    # Set the variables for making the grid
    if time_column:
        years = dataset[time_column].unique()
    else:
        years = None
        show_slider = False
        show_button = False
        
    column_names = [x_column, y_column]
    
    column_names.append(bubble_column)
    if xy_column:
        column_names.append(xy_column)
    if bubble_text:
        column_names.append(bubble_text)
    if bubble_link:
        column_names.append(bubble_link)
    
    if size_column:
        column_names.append(size_column)
    
    if color_column:
        column_names.append(color_column)
        
        
    # Make the grid
    if category_column:
        categories = dataset[category_column].unique()
        col_name_template = '{}+{}+{}_grid'
        grid = make_grid_with_categories(dataset, column_names, time_column, category_column, years, categories)
        if show_legend is None:
            showlegend = True
        else: 
            showlegend = show_legend

        
    # Set the layout
    if show_slider:
        slider_scale = years
    else:
        slider_scale = None
                
    figure, sliders_dict = set_layout(x_title, y_title, title, show_slider, slider_scale, show_button, showlegend, width, height)
    
    if size_column:
        sizeref = 2.*max(dataset[size_column])/(scale_bubble**2) # Set the reference size for the bubbles
    else:
        sizeref = None

    # Add the frames
    if category_column:
        # Add the base frame
        for category in categories:
            if time_column:
                year = min(years) # The earliest year for the base frame
                col_name_template_year = col_name_template.format(year, {}, {})
            else:
                col_name_template_year = '{}+{}_grid'
            trace = get_trace(grid, col_name_template_year, x_column, y_column, xy_column, 
                              bubble_column,bubble_text, bubble_link, size_column, 
                              sizeref, scale_bubble, marker_opacity, marker_border_width, mode=mode,category=category, xsize=xbin_size, ysize=ybin_size,
                              xy_scale=xy_scale, xshift=xshift, yshift=yshift)
            figure['data'].append(trace)
           
        # Add time frames
        if time_column: # Only if time_column is not None
            for year in years:
                frame = {'data': [], 'name': str(year)}
                for category in categories:
                    col_name_template_year = col_name_template.format(year, {}, {})
                    trace = get_trace(grid, col_name_template_year, x_column, y_column, xy_column, 
                                      bubble_column, bubble_text, bubble_link, size_column, 
                                      sizeref, scale_bubble, marker_opacity, marker_border_width ,mode=mode, category=category, xsize=xbin_size, ysize=ybin_size,
                                      xy_scale=xy_scale, xshift=xshift, yshift=yshift)
                    
                    frame['data'].append(trace)

                    figure['frames'].append(frame) 

                if show_slider:
                    add_slider_steps(sliders_dict, year)
                
    else:
        # Add the base frame
        if time_column:
            year = min(years) # The earliest year for the base frame
            col_name_template_year = col_name_template.format(year, {})
        else:
            col_name_template_year = '{}_grid'
        trace = get_trace(grid, col_name_template_year, x_column, y_column, xy_column, 
                          bubble_column, bubble_text, bubble_link, size_column, 
                          sizeref, scale_bubble, marker_opacity, marker_border_width,
                          color_column, colorscale, show_colorbar, colorbar_title, mode=mode, xsize=xbin_size, ysize=ybin_size,
                          xy_scale=xy_scale, xshift=xshift, yshift=yshift)
       
        figure['data'].append(trace)
        
        # Add time frames
        if time_column: # Only if time_column is not None
            for year in years:
                col_name_template_year = col_name_template.format(year, {})
                frame = {'data': [], 'name': str(year)}
                trace = get_trace(grid, col_name_template_year, x_column, y_column, xy_column,
                                  bubble_column, bubble_text, bubble_link,size_column, 
                                  sizeref, scale_bubble, marker_opacity, marker_border_width,
                                  color_column, colorscale, show_colorbar, colorbar_title, mode=mode, xsize=xbin_size, ysize=ybin_size, 
                                  xy_scale=xy_scale, xshift=xshift, yshift=yshift)

                frame['data'].append(trace)
                figure['frames'].append(frame) 
                if show_slider:
                    add_slider_steps(sliders_dict, year) 
    # Set ranges for the axes
   
    x_range = set_range(dataset[x_column], xbin_size)
    y_range = set_range(dataset[y_column], ybin_size)
    
    figure['layout']['xaxis']['range'] = x_range
    figure['layout']['yaxis']['range'] = y_range
        
    if show_slider:
        figure['layout']['sliders'] = [sliders_dict]
    
    tracepoint = draw_evidence_gap_map_structure_horzero(xbin_list,ybin_list,xbin_size,ybin_size )
    figure['data'].append(tracepoint)
    for i in range(len(ybin_list)+1): 
        tracepoint = draw_evidence_gap_map_structure_hor(i, xbin_list,ybin_list,xbin_size,ybin_size )
        figure['data'].append(tracepoint)
    tracepoint = draw_evidence_gap_map_structure_verzero(xbin_list,ybin_list,xbin_size,ybin_size )
    figure['data'].append(tracepoint)
    for i in range(len(xbin_list)+1): 
        tracepoint = draw_evidence_gap_map_structure_ver(i, xbin_list,ybin_list,xbin_size,ybin_size )
        figure['data'].append(tracepoint)
    return figure

def draw_evidence_gap_map_structure_horzero(x_list=None, y_list=None,xbin=100, ybin=100):
    number_of_xcats = len(x_list)
    number_of_ycats = len(y_list)
    draw_horizontals_zero= {
        'x': [int((xbin/2)+i*(xbin)) for i in range(number_of_xcats)],
        'y': [0 for i in range(number_of_xcats)],
        'text': [x_list[line] for line in range(number_of_xcats)],
        'mode': 'lines+text',
        'textposition': 'bottom center',
        'showlegend': False
    }
    return draw_horizontals_zero
def draw_evidence_gap_map_structure_hor(linenum=1, x_list=None, y_list=None,xbin=100, ybin=100):
    number_of_xcats = len(x_list)
    number_of_ycats = len(y_list)
    draw_horizontals = {
        'x': [int(i*xbin) for i in range(number_of_xcats+1)],
        'y': [int(linenum*(ybin)) for i in range(number_of_xcats+1)],
        'text': "",
        'mode': 'lines',
        'showlegend': False
    }
    return draw_horizontals
def draw_evidence_gap_map_structure_verzero(x_list=None, y_list=None,xbin=100, ybin=100):
    number_of_xcats = len(x_list)
    number_of_ycats = len(y_list)
    draw_verticals_zero= {
        'x': [0 for i in range(number_of_ycats)],
        'y': [int((ybin/2)+i*(ybin)) for i in range(number_of_ycats)],
        'text': [y_list[line] for line in range(number_of_ycats)],
        'mode': 'lines+text',
        'textposition': 'middle left',
        'showlegend': False
    }
    return draw_verticals_zero
def draw_evidence_gap_map_structure_ver(linenum=1, x_list=None, y_list=None,xbin=100, ybin=100):
    number_of_xcats = len(x_list)
    number_of_ycats = len(y_list)
    draw_verticals = {
        'x': [int(linenum*(xbin)) for i in range(number_of_ycats+1)],
        'y': [int(i*ybin) for i in range(number_of_ycats+1)],
        'text': "",
        'mode': 'lines',
        'showlegend': False
    }
    return draw_verticals
    
def make_grid_with_categories(dataset, column_names, time_column, category_column, years=None, categories=None):
    '''Makes the grid for the plot as a pandas DataFrame.'''
    
    grid = pandas.DataFrame()
    if categories is None:
        categories = dataset[category_column].unique()
    if time_column:
        col_name_template = '{}+{}+{}_grid'
        if years is None:
            years = dataset[time_column].unique()
            
        for year in years:
            for category in categories:
                dataset_by_year_and_cat = dataset[(dataset[time_column] == int(year)) & (dataset[category_column] == category)]
                for col_name in column_names:
                    # Each column name is unique
                    temp = col_name_template.format(year, col_name, category)
                    if dataset_by_year_and_cat[col_name].size != 0:
                        grid = grid.append({'value': list(dataset_by_year_and_cat[col_name]), 'key': temp}, ignore_index=True) 
    else:
        col_name_template = '{}+{}_grid'
        for category in categories:
            dataset_by_cat = dataset[(dataset[category_column] == category)]
            for col_name in column_names:
                # Each column name is unique
                temp = col_name_template.format(col_name, category)
                if dataset_by_cat[col_name].size != 0:
                        grid = grid.append({'value': list(dataset_by_cat[col_name]), 'key': temp}, ignore_index=True) 
    return grid

 
def set_layout(x_title=None, y_title=None, title=None, show_slider=True, slider_scale=None, show_button=True, show_legend=False,
            width=None, height=None):
    '''Sets the layout for the figure.'''
    
    # Define the figure object as a dictionary
    figure = {
        'data': [],
        'layout': {},
        'frames': []
    }
    
    # Start with filling the layout first
    
    figure = set_2Daxes(figure, x_title, y_title)
        
    figure['layout']['title'] = title    
    figure['layout']['hovermode'] = 'closest'
    figure['layout']['showlegend'] = show_legend
    figure['layout']['margin'] = dict(l=60, b=50, t=50, r=60, pad=10)
    
    
    if width:
        figure['layout']['width'] = width
    if height:
        figure['layout']['height'] = height
    
    # Add slider for the time scale
    if show_slider: 
        sliders_dict = add_slider(figure, slider_scale)
    else:
        sliders_dict = {}
    
    # Add a pause-play button
    if show_button:
        add_button(figure)
        
    # Return the figure object
    return figure, sliders_dict

def set_2Daxes(figure, x_title=None, y_title=None):
    '''Sets 2D axes'''
    
    figure['layout']['xaxis'] = {'title': x_title, 'autorange': False, 'showgrid': False, 'zeroline': False, 'showline': False, 'ticks': '',
    'showticklabels': False, 'automargin': True}
    figure['layout']['yaxis'] = {'title': y_title, 'autorange': False, 'showgrid': False, 'zeroline': False, 'showline': False, 'ticks': '',
    'showticklabels': False, 'automargin': True} 
        
    return figure
    
        
def add_slider(figure, slider_scale):
    '''Adds slider for animation'''
    
    figure['layout']['sliders'] = {
        'args': [
            'slider.value', {
                'duration': 400,
                'ease': 'cubic-in-out'
            }
        ],
        'initialValue': min(slider_scale),
        'plotlycommand': 'animate',
        'values': slider_scale,
        'visible': True
    }
    
    sliders_dict = {
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 20},
            'prefix': 'Year:',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': []
    }
    
    return sliders_dict

def add_slider_steps(sliders_dict, year):
    '''Adds the slider steps.'''
    
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
       'transition': {'duration': 300}}
     ],
     'label': str(year),
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)
    
def add_button(figure):
    '''Adds the pause-play button for animation'''
    
    figure['layout']['updatemenus'] = [
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 500, 'redraw': False},
                             'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                    'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }
    ]
    
def set_range(values, size): 
    ''' Finds the axis range for the figure.'''
    
    rmin = int(min([return_xbin_cords(x, size) for x in values]))-size/2
    rmax = int(max([return_xbin_cords(x, size) for x in values]))+size/2
    
        
    return [rmin, rmax] 

# To be used later when individual Risk Factos can be plotted
def return_xbin_cords(x_binnum, sizebin):
    # generate some random integers to fit in the research papers in a cell
    values = random.randint((-sizebin/2+5),(sizebin/2-5))
    #Plots start at (0, 0)
    xbin_cords = sizebin/2 + (x_binnum*sizebin) + values
    return int(xbin_cords)

# To be used later when individual Risk Factos can be plotted
def return_ybin_cords(y_binnum, sizebin):
    # generate some random integers to fit in the research papers in a cell
    values = random.randint((-sizebin/2+5),sizebin/2-5)
    #Plots start at (0, 0)
    ybin_cords = sizebin/2 + (y_binnum*sizebin) + values
    return int(ybin_cords)

# To be used later when individual Risk Factos can be plotted
def return_xy_cords_nlp(a, xy, sizebin, axes, scale, shift):
    if axes=='x':
        margin = 10
        # generate some random integers to fit in the research papers in a cell
        # remove a margin of 10 from the size of bin so effectively available size is 90 if bin is 100
        values = ((xy[0]-shift)/scale)*(sizebin - 10)
        #Plots start at (0, 0)
        x_cords = sizebin/2 + (a*sizebin) + values
        return int(x_cords)
    else :
        # generate some random integers to fit in the research papers in a cell
        # remove a margin of 10 from the size of bin so effectively available size is 90 if bin is 100
        values = ((xy[1]-shift)/scale)*(sizebin - 10)
        #Plots start at (0, 0)
        y_cords = sizebin/2 + (a*sizebin) + values
        return int(y_cords)
    
def return_text_by_category_in_bin(grid,category,xbinnum,ybinnum,template, xcol, ycol, column, bubbletext, link, size):
    indicesx=[]
    indicesy=[]
    for idx, row in grid[grid['key'].str.contains(category)].iterrows():
        if row['key']==template.format(xcol, category):
            for i, xx in enumerate(row['value']):
                if (xx==xbinnum):
                    indicesx.append(i)
        if row['key']==template.format(ycol, category):
            for i, yy in enumerate(row['value']):
                if (yy==ybinnum):
                    indicesy.append(i) 
    matchindex = list(set(indicesx) & set(indicesy))
    textoverall=[]
    textcol=[]
    texttext=[]
    textlink=[]
    textrelevance=[]
    for idx, row in grid[grid['key'].str.contains(category)].iterrows():
        for i, val in enumerate(matchindex):
            if row['key']==template.format(column, category):
                textcol.append('<b>Title:</b>'+ str(row['value'][val]))
            if bubbletext:
                if row['key']==template.format(bubbletext, category):
                    texttext.append('<br><b>Summary:</b>'+ str(row['value'][val]))
            if link:
                if row['key']==template.format(link, category):
                    textlink.append('<br><b>Link:</b>'+ str(row['value'][val]))   
            if size:
                if row['key']==template.format(size, category):
                    textrelevance.append('<br><b>Relevance:</b>'+ str(row['value'][val]))
    for idx, val in enumerate(textcol):
        # Display top 8 of relevant  and the highlighted 
        if idx==0:
            textall = ""
        else: 
            textall ='<br>----------------------------------------<br>'
        textall = textall + textcol[idx]
        if bubbletext:
            textall = textall + texttext[idx]
        if link:
            textall = textall + textlink[idx] 
        if size:
            textall = textall + textrelevance[idx]
        textoverall.append(textall)
        # Plotly only able to handle only upto 9 datapoints in hovertext
        # TODO ensure that the closest point being hovered is always included
        if idx==8 :
            break
    return "".join(textoverall)    

# The size is used to categorize in High (top 10% percentile), Medium ( to 50% ) and Rest as Low
def return_transformed_size(size, comparewith):
    if size > np.percentile(comparewith, 90):
        return size*1.25
    elif size > np.percentile(comparewith, 50):
        return size
    else :
        return size/1.25
    
def get_trace(grid, col_name_template, x_column, y_column,xy_column, bubble_column, bubble_text, bubble_link,size_column=None, 
            sizeref=1, scale_bubble=10, marker_opacity=None, marker_border_width=None,
            color_column=None, colorscale=None, show_colorbar=True, colorbar_title=None, mode=None, category=None, xsize=100, ysize=100, 
            xy_scale=1, xshift=0, yshift=0):
    ''' Makes the trace for the data as a dictionary object that can be added to the figure or time frames.'''
    try:
        if mode =='randommode':
            trace = {
                    'x': [return_xbin_cords(x, xsize) for x in grid.loc[grid['key']==col_name_template.format(x_column, category), 'value'].values[0]],
                    'y': [return_ybin_cords(y, ysize) for y in grid.loc[grid['key']==col_name_template.format(y_column, category), 'value'].values[0]],
                    'text': [i + '<br><b>Summary:</b>' + j + '<br><b>Link:</b>' + k for i, j, k in zip(grid.loc[grid['key']==col_name_template.format(bubble_column, category), 'value'].values[0], grid.loc[grid['key']==col_name_template.format(bubble_text, category), 'value'].values[0],grid.loc[grid['key']==col_name_template.format(bubble_link, category), 'value'].values[0])],
                    'hovertemplate': '<b>Title:</b>%{text}<extra></extra>',
                    'mode': 'markers'
            }
        else:
            trace = {
                    'x': [return_xy_cords_nlp(x,xy, xsize, 'x', xy_scale, xshift) for x, xy in zip(grid.loc[grid['key']==col_name_template.format(x_column, category), 'value'].values[0],grid.loc[grid['key']==col_name_template.format(xy_column, category), 'value'].values[0])],
                    'y': [return_xy_cords_nlp(y,xy, ysize, 'y', xy_scale, yshift) for y, xy in zip(grid.loc[grid['key']==col_name_template.format(y_column, category), 'value'].values[0],grid.loc[grid['key']==col_name_template.format(xy_column, category), 'value'].values[0])],
                    'text': [return_text_by_category_in_bin(grid,category,x,y,col_name_template,x_column,y_column,bubble_column,bubble_text,bubble_link,size_column) for x, y  in zip(grid.loc[grid['key']==col_name_template.format(x_column,category), 'value'].values[0],grid.loc[grid['key']==col_name_template.format(y_column, category), 'value'].values[0])],
                    'hovertemplate': '%{text}<extra></extra>',
                    'mode': 'markers'
            }
        if size_column:
                trace['marker'] = {
                    'sizemode': 'diameter',
                    'sizeref': sizeref,
                    'size': [return_transformed_size(size, grid.loc[grid['key']==col_name_template.format(size_column, category), 'value'].values[0]) 
                             for size in grid.loc[grid['key']==col_name_template.format(size_column, category), 'value'].values[0]],
                }
        else:
                trace['marker'] = {
                    'size': 10*scale_bubble,
                }

        if marker_opacity:
                trace['marker']['opacity'] = marker_opacity

        if marker_border_width:
                trace['marker']['line'] = {'width': marker_border_width}

        if color_column:
                    trace['marker']['color'] = grid.loc[grid['key']==col_name_template.format(color_column), 'value'].values[0]
                    trace['marker']['colorbar'] = {'title': colorbar_title}
                    trace['marker']['colorscale'] = colorscale

        if category:
                trace['name'] = category
    except:
        trace = {
            'x': [],
            'y': [],
            }

    return trace
