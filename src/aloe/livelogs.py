import ipywidgets as widgets
from collections import OrderedDict
from aloe.utils import bcolors
import math

class LiveLog:
    def __init__(self):
        self.eventlogs = list()
        
    def add_eventlog(self, event_name, value):
        self.eventlogs.append((event_name, value))
        
    def regroup_eventlogs(self):
        if not self.eventlogs: pass
        separator=self.eventlogs[0][0]
        self.groups = list()
        for event_name, value in self.eventlogs:
            if event_name==separator:
                self.groups.append(dict())
            if event_name not in self.groups[-1]:
                self.groups[-1][event_name] = list()
            self.groups[-1][event_name].append(value)
            

# Widgets for learning logs            
#--------------------------            
STATE_ATTRIBUTES = ['f', 'g', 'p', 'n', 'c', 'h']
ATTR_DESCRIPTION = {
    'p':'Number of positive examples covered',
    'n':'Number of negative examples covered',
    'f':'Fitness value\nf=p-(n+c+h)',
    'g':'Upper bound on fitness value\ng=p-(c+h)',
    'h':'Optimistic estimate of atoms needed',
    'c':'Number of atoms in the body',
}            
class LearningLog(LiveLog):    
    focus = None
    focus_default_color = None
    
    def interact(self):
        if not hasattr(self, 'widgets'):
            self.build_widgets()
        return widgets.interact(lambda e: self.widgets[e], e=self.eg_widget)
        
    def build_widgets(self):
        self.regroup_eventlogs()
        self.groups2id = OrderedDict((group['Current example'][0],i) for i, group in enumerate(self.groups))
        
        # Example generalized widget
        self.eg_widget = widgets.Dropdown(
            options=list(self.groups2id),
            description='Example:',
            disabled=False,
        )
        
        self.widgets = {eg:self._group_details(eg) for eg in self.groups2id}
        
        
    def _group_details(self, eg):
        """ eg: example generalized """
        group_log = self.groups[self.groups2id[eg]]
        
        bottom_i_details = self._bottom_i_details(group_log)
        states_details   = self._states_details(group_log)
        
        group_details = widgets.VBox([bottom_i_details, states_details])
        
        return group_details
    
    def _bottom_i_details(self, group_log):
        bottom_i = group_log['Bottom_i'][0]
        
        layout1 = widgets.Layout(display="flex", justify_content="flex-start", height='auto', width='auto')
        layout2 = widgets.Layout(display="flex", justify_content="flex-start", height='auto', width='auto')
        
        
        # To display bottom_i on multiple lines
        k = 3
        body_grouped_by_k = [', '.join([str(b) for b in bottom_i.body[k*i:k*(i+1)]]) for i in range(math.ceil(len(bottom_i.body)/k))]
        head_string = str(bottom_i.head) + ' :- '
        head_tab = '\n'+(' '*int(len(head_string)*1.75))
        center_ttip = head_string + head_tab.join(body_grouped_by_k)
        
        bottom_widget = widgets.AppLayout(
            left_sidebar= widgets.Button(description='Bottom i:',  button_style='success', layout=layout1), 
            center      = widgets.Button(description=str(bottom_i), button_style='warning', layout=layout2, tooltip=center_ttip), 
            pane_widths = (.15,.85,0)
        )
        return bottom_widget

        
    def _states_details(self, group_log):
        states = group_log['State']
        n_states = len(states)

        # Fn measure part    
        n_attributes = len(STATE_ATTRIBUTES)

        grid = widgets.GridspecLayout(n_states+2, n_attributes)

        for j, attr in enumerate(STATE_ATTRIBUTES):
            b = self._state_button(grid, attr)
            if attr in ATTR_DESCRIPTION:
                b.tooltip = ATTR_DESCRIPTION[attr]
            grid[1, j] = b 
        for i, s in enumerate(states):
            for j, attr in enumerate(STATE_ATTRIBUTES):
                grid[i+2, j] = self._state_button(grid, attr, s)
                if s.clause==group_log['Clause'][0]:
                    grid[i+2, j].style.button_color = '#964B00'

        # Clause part
        attr = 'clause'
        clause_widget = widgets.GridspecLayout(n_states+2, 1)
        clause_widget[1, 0] = self._state_button(grid, attr)
        for i, s in enumerate(states):
            clause_widget[i+2, 0] = self._state_button(grid, attr, s)
            if s.clause==group_log['Clause'][0]:
                clause_widget[i+2, 0].style.button_color = '#964B00'

        # States_widget
        states_widget = widgets.AppLayout(left_sidebar=clause_widget, center=grid, pane_widths=(.6,.4,0))

        return states_widget    
    
    def _state_button(self, grid, attr, s=None):        
        if s is None:
            descr = attr
            b_style = 'success'
        else:
            descr = str(getattr(s, attr))
            b_style = 'warning'

        if attr=='clause':
            layout = widgets.Layout(display="flex", justify_content="flex-start", height='auto', width='auto')
        else:
            layout = widgets.Layout(height='auto', width='auto')

        button = widgets.Button(description=descr, button_style=b_style, layout=layout)

        if s is not None:
            if   attr=='p'or attr=='n':
                button.on_click(self._explain_pos_neg_button(attr, s, grid))
        return button
    
    def _clear_grid_explanation(self, grid):
        grid[0,:] = widgets.Label('')

    def _explain_pos_neg_button(self, label, s, grid):
        if label=='p':
            expl_covered = set(s.E_cov['pos'])
            all_examples = s.hm.E['pos']
        else: #label=='n'
            expl_covered = set(s.E_cov['neg'])
            all_examples = s.hm.E['neg']
            
        relevant_exp = [e for e in all_examples if e.head.functor==s.clause.head.functor]
        options = [chr(int("1F534",base=16)+(c in expl_covered))+' '+str(c) for c in relevant_exp]
        w = widgets.Dropdown(
            options=options,
            description='Examples:',
            layout = widgets.Layout(height='auto', width='auto'),
        )
        layout = widgets.Layout(height='auto', width='auto')
        l = widgets.Button(description='%d/%d' % (len(expl_covered), len(relevant_exp)), layout=layout)
        l.tooltip = '#examples covered/#relevant examples'
        
        def explanation_button(button):
            if self.focus==button:
                self._clear_grid_explanation(grid)
                self.remove_focus()
            else:
                grid[0,:5] = w
                grid[0, 5] = l
                self.put_focus(button)
                            
        return explanation_button        
            
    def remove_focus(self):
        if self.focus is None:
            return
        self.focus.style.button_color = self.focus_default_color
        self.focus = None
        self.focus_default_color = None

    def put_focus(self, button):
        self.remove_focus()
        self.focus = button
        self.focus_default_color = button.style.button_color
        button.style.button_color = 'blue'

            