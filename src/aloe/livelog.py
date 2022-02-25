import ipywidgets as widgets
from collections import OrderedDict
from aloe.utils import bcolors
import math

class LiveLog:
    """ """
    def __init__(self, parent=None):
        self._data = OrderedDict()
        self.pointer = self
        self.parent = parent
        
    @property
    def data(self): return self.pointer._data
        
    def beg_child(self, name, point_to_child=True):
        child = LiveLog(self.pointer)
        self.add_eventlog(name, child)
        if point_to_child:
            self.pointer = child
            
    def end_child(self):
        self.pointer = self.pointer.parent
        
    def add_eventlog(self, event_id, value):
        self.data[event_id] = value
        
    def __repr__(self):
        header = self.__class__.__name__        
        tab = ' '*3
        data = '\n'.join([tab+'%s: %s' % (repr(key), repr(value)) for key, value in self._data.items()])
        return '%s\n%s' % (header, data)

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
        if not hasattr(self, 'widget'):
            self.build_widget()
        display(self.widget)
        #return widgets.interact(lambda e: self.interactions_widget[e], e=self.eg_widget)
        
    def build_widget(self):
        self.widget = widgets.Tab()
        
        iterations_widget = self._iterations_details(self.data['Iterations'])
        query_tab = self._query_tab(self.data['Options'], self.data['Knowledge'], self.data['Learned knowledge'])
        
        self.widget.children = [iterations_widget, query_tab]
        for i, title in enumerate(['Iteration details', 'Query tab']):
            self.widget.set_title(i, title)
        
    def _learning_info_tab(self, data):
        pass
        
    def _query_tab(self, options, old_knowledge, learned_knowledge):
        from aloe.program import AloeProgram
        from aloe.knowledge import MultipleKnowledge
        from aloe.queryinterface import QueryInterface
        
        new_knowledge = MultipleKnowledge(old_knowledge, learned_knowledge, options=options)
        
        self.knowledge_widget = widgets.ToggleButtons(
            options=[('Old knowledge', QueryInterface(AloeProgram(options=options, knowledge=old_knowledge))), 
                     ('New knowledge', QueryInterface(AloeProgram(options=options, knowledge=new_knowledge)))],
            index=1,
            button_style='info',
            tooltips=['Knowledge before learning', 'Knowledge after learning'],
        )
        for _, qi in self.knowledge_widget.options:
            qi.disable_knowledge_editability()

        def knowledge_change():
            self.qi_widget.children = [self.knowledge_widget.value.widget]
            
        self.qi_widget = widgets.HBox([])
        knowledge_change()
        self.knowledge_widget.observe(lambda info: knowledge_change() if info['type']=='change' and info['name']=='value' else None)
                
        tab = widgets.VBox([self.knowledge_widget, self.qi_widget])
        return tab
        
    def _iterations_details(self, data_iterations):
        # Example generalized widget
        iteration_input_widget = widgets.Dropdown(
            options=list(data_iterations.data),
            description='Example:',
            disabled=False,
        )
        def iteration_change(info):
            if info['type'] == 'change' and info['name'] == 'value':
                example = info['new']
                iteration_box.children = (iteration_widgets[example],)
                
        iteration_input_widget.observe(iteration_change)
        iteration_widgets = {e:self._iteration_details(data_iteration) for e, data_iteration in data_iterations.data.items()}
        
        
        iteration_box = widgets.VBox((iteration_widgets[iteration_input_widget.value],))
        iterations_widget = widgets.VBox([iteration_input_widget, iteration_box])
        
        return iterations_widget
                
    def _iteration_details(self, data_iteration):
        
        bottom_i_details = self._bottom_i_details(data_iteration.data['Bottom_i'])
        states_details   = self._states_details(  data_iteration.data['States'], data_iteration.data['Clause'])
        
        iteration_details = widgets.VBox([bottom_i_details, states_details])
        
        return iteration_details

    
    def _bottom_i_details(self, data_bottom_i):
        bottom_i = data_bottom_i
        
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

        
    def _states_details(self, data_states, data_clause):
        best_clause = data_clause
        
        states = [s for _, s in data_states.data.items()]
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
                if s.clause==best_clause:
                    grid[i+2, j].style.button_color = '#964B00'

        # Clause part
        attr = 'clause'
        clause_widget = widgets.GridspecLayout(n_states+2, 1)
        clause_widget[1, 0] = self._state_button(grid, attr)
        for i, s in enumerate(states):
            clause_widget[i+2, 0] = self._state_button(grid, attr, s)
            if s.clause==best_clause:
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

            