# Display solver
from aloe.program import AloeProgram
from aloe.knowledge import Knowledge
from aloe.parser import AloeParser, AloeText
import ipywidgets as widgets

from aloe.collections import OrderedSet

DEFAULT_LAYOUT   = {'height':'auto', 'width':'auto'}
TEXT_LAYOUT = {'height': '400px', 'width':'99%'}
RULES = 'rules'
FACTS = 'facts'
ALL   = 'all'
CATEGORIES = [ALL, FACTS, RULES]

def get_category(clause):
    return RULES if ':-' in clause else FACTS

class QueryInterface:
    def __init__(self, ap=None, **options):
        self.parser = AloeParser()
        self.ap = ap if ap is not None else AloeProgram(options=options)
            
        # update options
        for field, value in options.items():
            self.ap.set(field, value)

        self.init_clauses()
        self.build_widgets()
        
    def init_clauses(self):
        self._clauses = {category:OrderedSet() for category in CATEGORIES}
        for c in self.ap.knowledge.clauses:
            c = str(c)
            self._clauses[ALL].add(c)
            self._clauses[get_category(c)].add(c)
        
    def update_clauses(self, clauses=None, category=None):
        if category is None:
            category = self.current_category()
        if clauses is None:
            clauses = self.text_widget[category].value
        if isinstance(clauses, str):
            at = AloeText(clauses)
            at.preprocess()
            clauses = at.get_clauses()
        
        depr_clauses = [c for c in self._clauses[category] if c not in set(clauses)]
        new__clauses = [c for c in clauses if c not in self._clauses[category]]
        
        for c in depr_clauses:
            self._clauses[ALL].remove(c)
            self._clauses[get_category(c)].remove(c)
            self.ap.knowledge.remove(self.parser.parse_rule(c, 'hornclause'))
            
        for c in new__clauses:
            self._clauses[ALL].add(c)
            self._clauses[get_category(c)].add(c)
            self.ap.knowledge.add(self.parser.parse_rule(c, 'hornclause'))
            
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
        self.category_widget = widgets.ToggleButtons(
            options=CATEGORIES,
            button_style='info',
            tooltips=['All clauses (facts+rules)', 'Only facts', 'Only rules'],
            layout=DEFAULT_LAYOUT,
        )
        self.category_widget.observe(self.click_category)
        
        self.text_widget = {category:widgets.Textarea(placeholder='Type %s here' % ('clauses' if category==ALL else category), 
                                                      layout=TEXT_LAYOUT,
                                                     ) for category in CATEGORIES}
        for category in CATEGORIES:
            self.update_clauses_widget(category=category)
        self.category_text_widget = widgets.HBox([])
        self.switch_category(self.current_category(), self.current_category())
        
        
        self.editability_widget = widgets.Button(
            button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
            layout = {'height':'auto', 'width':'100px'},
        )
        self.unable_knowledge_editability()
        self.editability_widget.on_click(lambda x: self.switch_knowledge_editability())
        
        self.save_widget = widgets.Button(
            button_style='',
            layout = {'height':'auto', 'width':'100%'},
            description='Save',
        )
        def save():
            self.save()
            self.update_clauses_widget()        
        self.save_widget.on_click(lambda x: save())
        
        hbox = widgets.HBox([self.category_widget, self.editability_widget])
        hbox.layout.display = 'flex'
        hbox.layout.align_items = 'stretch'
        self.knowledge_widget = widgets.VBox([hbox, self.category_text_widget])
        self.output_widget = widgets.Output(layout = {
#                                                        'width': '100%',
#                                                        'height': '100%',
                                                        'border': '1px solid black'
                                                    })

        self.query_text_widget = widgets.Textarea(
            placeholder='Your query',
            layout=TEXT_LAYOUT,
        )
        self.launch_query_widget = widgets.Button(description='Launch query', layout=DEFAULT_LAYOUT)
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
        
        self.query_widget = widgets.VBox([self.query_text_widget, self.launch_query_widget])
        
        self.widget = widgets.VBox([
            widgets.HBox(
                [self.save_widget],
                layout={'width':'100%','align-self':'end'}
            ),
            widgets.AppLayout(
                left_sidebar=self.query_widget,
                center=self.knowledge_widget,
                pane_widths=[4, 6, 0]
            ),
            self.output_widget],
        )
        
    def interact(self):
        display(self.widget)
        
    def get_AloeProgram(self): return self.ap
