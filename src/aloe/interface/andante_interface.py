from aloe.program import AloeProgram
from aloe.parser  import Parser
from aloe.knowledge import Knowledge, MultipleKnowledge
from aloe.collections import OrderedSet

import itertools
import math

from ipywidgets import Label, HBox, VBox, Button, ToggleButtons, Dropdown, Text, Textarea, Tab, AppLayout, Output, GridspecLayout, Layout

#-----------------------------------------------#
#                  Constants
#-----------------------------------------------#

HEIGHT = '300px'

DEFAULT_LAYOUT   = {'height':'auto', 'width':'auto'}
TEXT_LAYOUT_1 = {'height': '400px', 'width':'99%'}
TEXT_LAYOUT_2 = {'height': HEIGHT, 'width':'360px'}
MODE_LAYOUT = {'height': HEIGHT, 'width':'270px'}
DETE_LAYOUT = {'height': HEIGHT, 'width':'545px'}
STYLE = {'description_width': '30px'}

RULES = 'rules'
FACTS = 'facts'
ALL   = 'all'
CATEGORIES = [ALL, FACTS, RULES]

DETAILS_CATEGORIES =  ['modeh', 'modeb', 'pos_examples', 'neg_examples', 'determination']
PARSER_CATEGORIES = {'modeh':'modeh', 'modeb':'modeb', 'pos_examples':'hornclause', 'neg_examples':'hornclause', 'determination':'determination'}


#-----------------------------------------------#
#              Andante Interface
#-----------------------------------------------#

class AndateInterface:
    def __init__(self, ap=None, **options):
        self.parser = Parser()
        self.ap = ap if ap is not None else AloeProgram(options=options)
        
        self.qi = QueryInterface(self.ap, **options)
        self.di = DetailsInterface(self)
        self.iis = []
        self.induction_count = 0
        
        self.query_interface   = self.qi.widget
        self.details_interface = self.di.widget
        
        self.widget = Tab()
        self.widget.children = [self.query_interface, self.details_interface]
        self.widget.set_title(0, 'Query program')
        self.widget.set_title(1, 'Program details')
        
    def add_tab(self, widget, title):
        self.widget.children = list(self.widget.children) + [widget]
        self.widget.set_title(len(self.widget.children)-1, title)
        
    def add_induction_tab(self, widget):
        self.add_tab(widget, 'Induction #%d' % self.induction_count)
        self.induction_count += 1

        
#-----------------------------------------------#
#              Details Interface
#-----------------------------------------------#
        
class DetailsInterface:
    def __init__(self, ai):
        self.ai = ai
        self.ap = self.ai.ap
        self.parser = self.ai.parser
        
        self.init_details()
        self.build_widget()
        self.refresh_details()
        
        
    def init_details(self):
        self.old_details = {category:OrderedSet() for category in DETAILS_CATEGORIES}
        self.old_details['pos_examples'].update(str(e) for e in self.ap.examples['pos'])
        self.old_details['neg_examples'].update(str(e) for e in self.ap.examples['neg'])
        self.old_details['modeh'].update(str(m) for _, m in self.ap.modes.map_to_modeh.items())
        self.old_details['modeb'].update(str(m) for _, m in self.ap.modes.map_to_modeb.items())
        self.old_details['determination'].update('determination(%s,%s).' % (modeh, modeb) for modeh in self.ap.modes.determinations for modeb in self.ap.modes.determinations[modeh])
        
    def get_detail(self, category):
        displayed_text = getattr(self, category+'_widget').children[1].value
        return self.parser.split_on_dots(displayed_text)
        
    def update_details(self):
        to_remove = dict()
        to_add = dict()
        for category in DETAILS_CATEGORIES:
            new = OrderedSet(self.get_detail(category))
            old = self.old_details[category]
            
            to_remove[category] = [self.parser.parse(c, PARSER_CATEGORIES[category]) for c in old if c not in new]
            to_add[category]    = [self.parser.parse(c, PARSER_CATEGORIES[category]) for c in new if c not in old]
            
            self.old_details[category] = new
        
        for e in to_add['pos_examples']:
            self.ap.examples['pos'].append(e)
        for e in to_add['neg_examples']:
            self.ap.examples['neg'].append(e)
        for c in itertools.chain(to_add['modeh'], to_add['modeb'], to_add['determination']):
            self.ap.modes.add(c)

        for e in to_remove['pos_examples']:
            self.ap.examples['pos'].remove(e)
        for e in to_remove['neg_examples']:
            self.ap.examples['neg'].remove(e)
        for c in itertools.chain(to_remove['modeh'], to_remove['modeb'], to_remove['determination']):
            self.ap.modes.remove(c)
            
    def refresh_details(self):
        for category in DETAILS_CATEGORIES:
            getattr(self, category+'_widget').children[1].value = '\n'.join(self.old_details[category])
            
    def save(self):
        self.update_details()
        self.init_details() # Re-init details to take into account outside modifications of self.ap
        self.update_details()
            
    def build_widget(self):
        details_toggle_button = ToggleButtons(
            options=['Modes', 'Options'],
            button_style='info',
            tooltips=['Show modes', 'Show options'],
            layout={'height':'auto', 'width':'auto'},
        )
        def fun(option):
            if option=='Modes':
                self.widget.children[1].right_sidebar.children = [modes_widget]
            else:
                self.widget.children[1].right_sidebar.children = [option_widget]
        details_toggle_button.observe(lambda info: fun(info['new']) if info['type']=='change' and info['name']=='value' else None)
        
        v = lambda x: '\n'.join([c for c in x])
        self.modeh_widget = VBox([Label('Modeh'),
                                     Textarea(placeholder='Insert modeh atoms', layout=MODE_LAYOUT)])
        self.modeb_widget = VBox([Label('Modeb'),
                                     Textarea(placeholder='Insert modeb atoms', layout=MODE_LAYOUT)])
        self.determination_widget = VBox([Label('Determinations'),
                                             Textarea(placeholder='Insert determinations', layout=DETE_LAYOUT)])
        modehb_widget = HBox([self.modeh_widget, self.modeb_widget])
        modes_widget = VBox([modehb_widget, self.determination_widget])
        
        def save_options():
            for w in all_options_widget:
                try:
                    value = int(w.value)
                except:
                    value = w.value
                self.ap.set(w.description, value)
        save_options_button = Button(description='Save options')
        save_options_button.on_click(lambda x: save_options())
        all_options_widget = [Text(
            value=str(getattr(self.ap.options, attr)),
            placeholder='Insert a %s type' % type(attr),
            description=attr,) for attr in self.ap.options]
        option_widget = VBox(all_options_widget + [save_options_button])
        
        self.pos_examples_widget = VBox([Label('Positive examples'), 
                                            Textarea(placeholder='Insert positive examples', layout=TEXT_LAYOUT_2)])
        self.neg_examples_widget = VBox([Label('Negative examples'), 
                                            Textarea(placeholder='Insert negative examples', layout=TEXT_LAYOUT_2)])
        examples_widget = VBox([self.pos_examples_widget, self.neg_examples_widget])
        
        def launch_induction():
            self.save()
            save_options()
            self.ap.induce(update_knowledge=False, logging=True, verbose=0)
            log = self.ap.learner.logs[-1]
            self.ai.iis.append(LearningInterface(log))
            self.ai.add_induction_tab(self.ai.iis[-1].widget)
            
        launch_induction_button = Button(description='Induce')
        launch_induction_button.on_click(lambda x: launch_induction())
        
        right_sidebar = HBox([modes_widget])
                
        save_button = Button(description='Save options')
        save_button.on_click(lambda x: self.save())
        header = HBox([
            HBox([save_button, launch_induction_button]), 
            details_toggle_button])
        header.layout.justify_content='space-between'
        self.widget = VBox([
            header, 
            AppLayout(
                right_sidebar=right_sidebar,
                center=examples_widget,
                pane_widths=[0, 4, 5.9],
            )],)
        
def get_category(clause):
    return RULES if ':-' in clause else FACTS


#-----------------------------------------------#
#              Query Interface
#-----------------------------------------------#

class QueryInterface:
    def __init__(self, ap=None, **options):
        self.parser = Parser()
        self.ap = ap if ap is not None else AloeProgram(options=options)
            
        # update options
        for field, value in options.items():
            self.ap.set(field, value)

        self.init_clauses()
        self.build_widgets()
        
    def init_clauses(self):
        self._clauses = {category:OrderedSet() for category in CATEGORIES}
        for c in self.ap.knowledge:
            c = str(c)
            self._clauses[ALL].add(c)
            self._clauses[get_category(c)].add(c)
        
    def update_clauses(self, clauses=None, category=None):
        if category is None:
            category = self.current_category()
        if clauses is None:
            clauses = self.text_widget[category].value
        if isinstance(clauses, str):
            clauses = self.parser.split_on_dots(clauses)
        
        depr_clauses = [c for c in self._clauses[category] if c not in set(clauses)]
        new__clauses = [c for c in clauses if c not in self._clauses[category]]
        
        for c in depr_clauses:
            self._clauses[ALL].remove(c)
            self._clauses[get_category(c)].remove(c)
            self.ap.knowledge.remove(self.parser.parse(c, 'hornclause'))
            
        for c in new__clauses:
            self._clauses[ALL].add(c)
            self._clauses[get_category(c)].add(c)
            self.ap.knowledge.add(self.parser.parse(c, 'hornclause'))
            
    def update_clauses_widget(self, category=None):
        category = category if category is not None else self.current_category()
        facts = self._clauses[FACTS] if category in (ALL, FACTS) else []
        rules = self._clauses[RULES] if category in (ALL, RULES) else []
        
        s_facts = '  '.join(list(facts))
        s_rules = '\n'.join(list(rules))
        if s_facts and s_rules:
            s = s_facts + '\n\n' + s_rules
        else:
            s = s_facts + s_rules
        self.text_widget[category].value = s
    
    def current_category(self):
        return self.category_widget.value
    
    def save(self, category=None):
        category = category if category is not None else self.current_category()
        self.update_clauses(category=category)
        self.init_clauses() # To take into account clauses added to ap from elsewhere
    
    def switch_category(self, old, new):
        self.save(category=old)
        self.category_text_widget.children = [self.text_widget[new]]
        self.update_clauses_widget(category=new)
            
    def click_category(self, info):
        if info['type'] == 'change' and info['name'] == 'value':
            self.switch_category(info['old'], info['new'])
            
    def unable_knowledge_editability(self):
        self.editability_widget.description='Editable'
        self.editability_widget.tooltip='Click to disable knowledge edition'
        self.editability_widget.icon='check'
        for _, tw in self.text_widget.items():
            tw.disabled=False
    
    def disable_knowledge_editability(self):
        self.editability_widget.description='Not editable'
        self.editability_widget.tooltip='Click to enable knowledge edition'
        self.editability_widget.icon='times'
        for _, tw in self.text_widget.items():
            tw.disabled=True
    
    def switch_knowledge_editability(self):
        if self.editability_widget.description=='Editable':
            self.disable_knowledge_editability()
        else:
            self.unable_knowledge_editability()

    def build_widgets(self):
        self.category_widget = ToggleButtons(
            options=CATEGORIES,
            button_style='info',
            tooltips=['All clauses (facts+rules)', 'Only facts', 'Only rules'],
            layout=DEFAULT_LAYOUT,
        )
        self.category_widget.observe(self.click_category)
        
        self.text_widget = {category:Textarea(placeholder='Type %s here' % ('clauses' if category==ALL else category), 
                                                      layout=TEXT_LAYOUT_1,
                                                     ) for category in CATEGORIES}

        for category in CATEGORIES:
            self.update_clauses_widget(category=category)
        self.category_text_widget = HBox([])
        self.switch_category(self.current_category(), self.current_category())


        self.editability_widget = Button(
            button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
            layout = {'height':'auto', 'width':'100px'},
        )
        self.unable_knowledge_editability()
        self.editability_widget.on_click(lambda x: self.switch_knowledge_editability())
        
        self.save_widget = Button(
            button_style='',
            layout = {'height':'auto', 'width':'100%'},
            description='Save',
        )
        def save():
            self.save()
            self.update_clauses_widget()        
        self.save_widget.on_click(lambda x: save())
        
        hbox = HBox([self.category_widget, self.editability_widget])
        hbox.layout.display = 'flex'
        hbox.layout.align_items = 'stretch'
        self.knowledge_widget = VBox([hbox, self.category_text_widget])
        self.output_widget = Output(layout = {
#                                                        'width': '100%',
#                                                        'height': '100%',
                                                        'border': '1px solid black'
                                                    })

        self.query_text_widget = Textarea(
            placeholder='Your query',
            layout=TEXT_LAYOUT_1,
        )
        self.launch_query_widget = Button(description='Launch query', layout=DEFAULT_LAYOUT)
        def launch_query(button):
            self.output_widget.clear_output()
            if not self.query_text_widget.value:
                return
            
            with self.output_widget:
                success, df = self.ap.query(self.query_text_widget.value)
                print(success)
                if success and len(df):
                        print(df)
        self.launch_query_widget.on_click(launch_query)
        
        self.query_widget = VBox([self.query_text_widget, self.launch_query_widget])
        
        self.widget = VBox([
            HBox(
                [self.save_widget],
                layout={'width':'100%','align-self':'end'}
            ),
            AppLayout(
                left_sidebar=self.query_widget,
                center=self.knowledge_widget,
                pane_widths=[4, 6, 0]
            ),
            self.output_widget],
        )
        
    def interact(self):
        display(self.widget)
        
    def get_AloeProgram(self): return self.ap
    
    
#-----------------------------------------------#
#              Learning Interface
#-----------------------------------------------#

STATE_ATTRIBUTES = ['f', 'g', 'p', 'n', 'c', 'h']
ATTR_DESCRIPTION = {
    'p':'Number of positive examples covered',
    'n':'Number of negative examples covered',
    'f':'Fitness value\nf=p-(n+c+h)',
    'g':'Upper bound on fitness value\ng=p-(c+h)',
    'h':'Optimistic estimate of atoms needed',
    'c':'Number of atoms in the body',
}            

class LearningInterface:
    focus = None
    focus_default_color = None
    
    def __init__(self, log):
        self.log = log
        self.data = log.data
        self.build_widget()
    
    def interact(self):
        display(self.widget)
        
    def build_widget(self):
        iterations_widget = self._iterations_details(self.data['Iterations'])
        query_tab = self._query_tab(self.data['Options'], self.data['Knowledge'], self.data['Learned knowledge'])
        
        self.togglebutton = ToggleButtons(
            options=[('Induction details', 1), ('Challenge new knowledge', 2)],
            layout={'height':'auto', 'width':'auto'},
        )
        
        self.widget1 = VBox(
            [self.togglebutton, iterations_widget]
        )
        h = HBox([self.togglebutton, self.knowledge_widget])
        h.layout.justify_content='space-between'
        self.widget2 = VBox(
            [h, query_tab]
        )            

        self.widget = VBox([self.widget1])


        self.togglebutton.observe(lambda x: toggle() if x['type']=='change' and x['name']=='value' else None)
        def toggle():
            if self.togglebutton.value==1:
                self.widget.children = [self.widget1]
            else: #self.togglebutton.value==2:
                self.widget.children = [self.widget2]

    def _learning_info_tab(self, data):
        pass
        
    def _query_tab(self, options, old_knowledge, learned_knowledge):
        new_knowledge = MultipleKnowledge(old_knowledge, learned_knowledge, options=options)
        
        self.knowledge_widget = ToggleButtons(
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
            
        self.qi_widget = HBox([])
        knowledge_change()
        self.knowledge_widget.observe(lambda info: knowledge_change() if info['type']=='change' and info['name']=='value' else None)
                
        tab = self.qi_widget
        return tab
        
    def _iterations_details(self, data_iterations):
        # Example generalized widget
        iteration_input_widget = Dropdown(
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
        
        
        iteration_box = VBox((iteration_widgets[iteration_input_widget.value],))
        iterations_widget = VBox([iteration_input_widget, iteration_box])
        
        return iterations_widget
                
    def _iteration_details(self, data_iteration):
        
        bottom_i_details = self._bottom_i_details(data_iteration.data['Bottom_i'])
        states_details   = self._states_details(  data_iteration.data['States'], data_iteration.data['Clause'])
        
        iteration_details = VBox([bottom_i_details, states_details])
        
        return iteration_details

    
    def _bottom_i_details(self, data_bottom_i):
        bottom_i = data_bottom_i
        
        layout1 = Layout(display="flex", justify_content="flex-start", height='auto', width='auto')
        layout2 = Layout(display="flex", justify_content="flex-start", height='auto', width='auto')
        
        # To display bottom_i on multiple lines
        k = 3
        body_grouped_by_k = [', '.join([str(b) for b in bottom_i.body[k*i:k*(i+1)]]) for i in range(math.ceil(len(bottom_i.body)/k))]
        head_string = str(bottom_i.head) + ' :- '
        head_tab = '\n'+(' '*int(len(head_string)*1.75))
        center_ttip = head_string + head_tab.join(body_grouped_by_k)
        
        bottom_widget = AppLayout(
            left_sidebar= Button(description='Bottom i:',  button_style='success', layout=layout1), 
            center      = Button(description=str(bottom_i), button_style='warning', layout=layout2, tooltip=center_ttip), 
            pane_widths = (.15,.85,0)
        )
        return bottom_widget

        
    def _states_details(self, data_states, data_clause):
        best_clause = data_clause
        
        states = [s for _, s in data_states.data.items()]
        n_states = len(states)

        # Fn measure part    
        n_attributes = len(STATE_ATTRIBUTES)

        grid = GridspecLayout(n_states+2, n_attributes)

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
        clause_widget = GridspecLayout(n_states+2, 1)
        clause_widget[1, 0] = self._state_button(grid, attr)
        for i, s in enumerate(states):
            clause_widget[i+2, 0] = self._state_button(grid, attr, s)
            if s.clause==best_clause:
                clause_widget[i+2, 0].style.button_color = '#964B00'

        # States_widget
        states_widget = AppLayout(left_sidebar=clause_widget, center=grid, pane_widths=(.6,.4,0))

        return states_widget    
    
    def _state_button(self, grid, attr, s=None):        
        if s is None:
            descr = attr
            b_style = 'success'
        else:
            descr = str(getattr(s, attr))
            b_style = 'warning'

        if attr=='clause':
            layout = Layout(display="flex", justify_content="flex-start", height='auto', width='auto')
        else:
            layout = Layout(height='auto', width='auto')

        button = Button(description=descr, button_style=b_style, layout=layout)

        if s is not None:
            if   attr=='p'or attr=='n':
                button.on_click(self._explain_pos_neg_button(attr, s, grid))
        return button
    
    def _clear_grid_explanation(self, grid):
        grid[0,:] = Label('')

    def _explain_pos_neg_button(self, label, s, grid):
        if label=='p':
            expl_covered = set(s.E_cov['pos'])
            all_examples = s.hm.E['pos']
        else: #label=='n'
            expl_covered = set(s.E_cov['neg'])
            all_examples = s.hm.E['neg']
            
        relevant_exp = [e for e in all_examples if e.head.symbol==s.clause.head.symbol]
        options = [chr(int("1F534",base=16)+(c in expl_covered))+' '+str(c) for c in relevant_exp]
        w = Dropdown(
            options=options,
            description='Examples:',
            layout = Layout(height='auto', width='auto'),
        )
        layout = Layout(height='auto', width='auto')
        l = Button(description='%d/%d' % (len(expl_covered), len(relevant_exp)), layout=layout)
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

                    
