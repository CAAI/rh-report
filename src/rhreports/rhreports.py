from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

class rhreports:
    def __init__(self):
        # Set A4 paper (8.27 x 11.69 inches)
        self.fig, self.ax = plt.subplots(figsize=(8.27,11.69), constrained_layout=True)

        # Set facecolor
        self.ax.set_facecolor('white')

        # Remove axes from figure
        self.ax.axis('off')

        # Set page margins [top, right, bottom, left]
        self.margin = [0.075, 0.075, 0.05, 0.075]
        
    def set_title(self, ypos, title:str='', subtitle:str=None):
        """ Set the title
        """

        # Add title
        xpos = self.margin[3] 
        titleax = self.ax.text(xpos, ypos, title, weight='bold', fontsize=24)

        if subtitle is None:
            return

        # Get width of title
        r = self.fig.canvas.get_renderer()
        bb = titleax.get_window_extent(renderer=r).transformed(self.ax.transData.inverted())
        xpos += bb.width-0.005*len(title)

        # Add subtitle
        self.ax.text(xpos, ypos, subtitle, fontsize=16)
    
    def create_axes(self, pos: list, ncols:int=1):
        """ Add new axes to the figure
            
        Parameters:
            pos: [left, bottom, width, height]
            ncols: set the number of columns across
        """

        # Get position and dimensions
        x, y, width, height = pos

        # Sanity check
        assert x+width<=1
        
        # Calculate width of axes
        colwidth = width/ncols

        # Allocate axes
        axs = []

        # Loop over each column
        for i in range(ncols):
            axs.append(self.fig.add_axes([x+(i)*colwidth, y, colwidth, height]))
        
        return axs
    
    def add_text(self, xpos:float, ypos:float, txt:str, **kwargs):
        self.ax.text(xpos, ypos, txt, kwargs)

    def set_demographics(self, pos:list, fields:dict={}):
        """ Create the demographics section
        
        Parameters:
            pos: [left, bottom, width, height]
            fields: Nested dict with key/value pairs
        """

        # Get position and dimensions
        x, y, width, height = pos

        # Sanity check
        assert x + width <= 1

        ymax = y
        ymin = y - height

        # Create horizontal lines
        self.ax.axhline(y=ymax, xmin=x, xmax=x+width, color='k', linewidth=1) # hline
        self.ax.axhline(y=ymin, xmin=x, xmax=x+width, color='k', linewidth=1) #hline

        # Get number of fields
        nfields = len(fields)

        if not nfields:
            return

        # Loop over all key/value pairs in 'fields' dict and calculate lenght of strings
        strlen = []
        for k,v in fields.items():
            strlen.append(max([len(k),len(str(v))]))
        
        # Calculate width of each field
        colwidth = (width-0.02)/np.sum(np.array(strlen))

        # Set starting x-position
        x0 = x+0.01

        # Calculate the offset from starting pos
        cumsum = np.cumsum(np.array(strlen))
        
        # Loop over each key/value pairs in 'fields' dict
        i = 0
        for k,v in fields.items():
            # Handle first iteration differently
            if i == 0:
                xpos = x0
            else:
                xpos = x0+(cumsum[i-1]*colwidth)
            
            # Insert fields into the demograpchis section
            if nfields> 1 and i == nfields-1:
                # Align last field to the right
                self.ax.text(x+width-0.01, y-0.015, k, fontsize=7, ha='right')
                self.ax.text(x+width-0.01, y-0.03, v, fontsize=9, ha='right')
            else:
                # Align fields to the left
                self.ax.text(xpos, y-0.015, k, fontsize=7, ha='left')
                self.ax.text(xpos, y-0.03, v, fontsize=9, ha='left')

            i+=1

    def create_table(self, pos: list, data: dict, rowheader: bool=True):
        """ Create table 
        
        Parameters:
            pos: [left, bottom, width, height]
                - height is determined by number of rows
            data: Nested dict
            rowheader: Boolean
        """

        # Get position and dimensions
        x, y, width, _ = pos

        # Sanity check
        assert x + width <= 1

        # Determine number of columns in table
        ncols = len(data) + rowheader

        # Calculate column width - equal width (TODO: individual column widths)
        colwidth = width/ncols

        ### Header
        # Horizontal line
        self.ax.axhline(y=y-0.01, xmin=x, xmax=x+width, color='k', linewidth=1) # hline

        # Iterate through each key
        for col, key in enumerate(data.keys()):
            # Add column header text
            self.ax.text(x + 0.015 + (col+rowheader)*colwidth, y-0.03, key, weight='bold', fontsize=8, ha='left')
        
        # Horizontal line
        self.ax.axhline(y=y-0.04, xmin=x, xmax=x+width, color='k', linewidth=1) # hline

        ### Body
        for col, (_, values) in enumerate(data.items()):
            for row, (key, value) in enumerate(values.items()):
                if col == 0 and rowheader:
                    # Add title column in bold
                    self.ax.text(x + 0.01, y-0.06-(row*0.025), key, fontsize=8, weight='bold')

                    # Divider
                    xmin = x
                    xmax = x + colwidth
                    self.ax.axhline(y=y-0.069-(row*0.025), xmin=xmin, xmax=xmax, color=(0.9,0.9,0.9), linewidth=1) # hline
                
                # Add column if rowheader is true
                i = col+rowheader

                # Add text
                self.ax.text(x + 0.015 + (i)*colwidth, y-0.06-(row*0.025), value, fontsize=8, ha='left')

                # Add Divider
                xmin = x + 0.01 + (i)*colwidth
                xmax = x + (i+1)*colwidth
                self.ax.axhline(y=y-0.069-(row*0.025), xmin=xmin, xmax=xmax, color=(0.9,0.9,0.9), linewidth=1) # hline
        
        # Divider
        xmin = x + 0.01 + (col)*colwidth
        xmax = x + (col+1)*colwidth
        self.ax.axhline(y=y-0.069-(row*0.025), xmin=xmin, xmax=xmax, color=(0.9,0.9,0.9), linewidth=1) # hline      

    def set_footer(self, data, ypos:float = None):
        """
        Parameters:
          ypos: y-position or default to self.margin[2]
          data: Nested dict with keys:
            'left'
            'center'
            'right'

            Under each key (left, center, right) a dict with type:
              type: 'text'
                content: ''
                color: RGB tuple
                fontsize: default 'x-small'
                linespacing: default 1.5
              type: 'img'
                src: png filename
                height: float [0-1]
        """

        # Set y-position of footer
        ypos = self.margin[2] if ypos is None else ypos
        
        for pos in ['left', 'center', 'right']:
            if not pos in data:
                continue
            # Text
            if data[pos]['type'] == 'text':
                textcolor = data[pos]['color'] if 'color' in data[pos] else mpl.rcParams['text.color']
                fontsize = data[pos]['fontsize'] if 'fontsize' in data[pos] else 'x-small' # mpl.rcParams['font.size']
                linespacing = data[pos]['linespacing'] if 'linespacing' in data[pos] else 1.5

                # Different xpos depending on position
                if pos == 'left':
                    xpos = self.margin[3]
                elif pos == 'center':
                    xpos = 0.5
                elif pos == 'right':
                    xpos = 1-self.margin[1]
                self.ax.text(xpos, ypos, data[pos]['content'], fontsize=fontsize, color=textcolor, linespacing=linespacing, ha=pos)
            # Image    
            elif data[pos]['type'] == 'img':
                pngfile = data[pos]['src'] if 'src' in data[pos] else print('Error: src not found')
                im = plt.imread(pngfile)

                # Height is accoding to the RegionH design manual set to 1/15 of page height
                height = data[pos]['height'] if 'height' in data[pos] else (1-self.margin[0]-ypos)/15
                width = im.shape[1] * height/im.shape[0]

                # Different xpos depending on position
                if pos == 'left':
                    xpos = self.margin[3]
                elif pos == 'center':
                    xpos = 0.5-width/2
                elif pos == 'right':
                    xpos = 1-self.margin[1]-width
                    
                # Create axes with position of logo
                ax = self.fig.add_axes([xpos, ypos-0.008, width, height])

                # Display the image in the axes
                ax.imshow(im, interpolation='none')
                ax.axis('off')  # Remove axis of the image

    def save(self, filename: Path)->Path:
        """ Save report to PDF
        """
        # Save figure as PDF
        plt.savefig(filename, format='pdf')

        # Cleanup
        plt.close(self.fig)

        return filename