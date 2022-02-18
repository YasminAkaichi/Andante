# Display solver
from aloe.program import AloeProgram
from aloe.knowledge import Knowledge
from aloe.parser import AloeParser, AloeText
import ipywidgets as widgets

DEFAULT_LAYOUT = {'height':'auto', 'width':'auto'}
TEXT_LAYOUT = {'height': '400px', 'width':'99%'}

class QueryInterface:
    def __init__(self, **options):
        self.ap = AloeProgram(options=options)
        self.parser = AloeParser()
        self.text_clauses = {'all':set(), 'facts':set(), 'rules':set()}
        self.build_widgets()

    def update(self, clauses, category):
        if isinstance(clauses, str):
            at = AloeText(clauses)
            at.preprocess()
            clauses = at.get_clauses()
        
        depr_clauses = [c for c in self.text_clauses[category] if c not in set(clauses)]
        new__clauses = [c for c in clauses if c not in self.text_clauses[category]]
        
        for c in depr_clauses:
            self.text_clauses['all'].remove(c)
            if category=='all':
                _category = 'rules' if ':-' in c else 'facts'
            else:
                _category = category
            self.text_clauses[_category].remove(c)
            self.ap.knowledge.remove(self.parser.parse_rule(c, 'hornclause'))
            
        for c in new__clauses:
            self.text_clauses['all'].add(c)
            if category=='all':
                _category = 'rules' if ':-' in c else 'facts'
            else:
                _category = category
            self.text_clauses[_category].add(c)
            self.ap.knowledge.add(self.parser.parse_rule(c, 'hornclause'))
            
    def switch_category(self, category):
        new_text_widget = self.text_widget[category]
        text = ''
        if category in ('all', 'facts'):
            text += ' '.join(self.text_clauses['facts'])
            if text: text+='\n'
        if category in ('all', 'rules'):
            if self.text_clauses['rules']: text+='\n'
            text += '\n'.join(self.text_clauses['rules'])
            if text: text+='\n'
        new_text_widget.value = text
        self.category_text_widget.children = [new_text_widget]
            
    def click_category(self, info):
        if info['type'] == 'change' and info['name'] == 'value':
            self.update(self.category_text_widget.children[0].value, info['old'])
            self.switch_category(info['new'])

    def build_widgets(self):
        self.category_widget = widgets.ToggleButtons(
            options=['all', 'facts', 'rules'],
            button_style='info',
            tooltips=['All clauses (facts+rules)', 'Only facts', 'Only rules'],
            layout=DEFAULT_LAYOUT,
        )
        self.category_widget.observe(self.click_category)
        
        self.text_widget = {category:widgets.Textarea(placeholder='Type %s here' % ('clauses' if category=='all' else category), 
                                                      layout=TEXT_LAYOUT,
                                                     ) for category in ['all', 'facts', 'rules']}
        self.category_text_widget = widgets.HBox([self.text_widget[self.category_widget.value]])
        
        self.knowledge_widget = widgets.VBox([self.category_widget, self.category_text_widget])
        
        self.output_widget = widgets.Output(layout={'border': '1px solid black'})

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
        
        self.widget = widgets.AppLayout(
            left_sidebar=self.query_widget,
            center=self.knowledge_widget,
            footer=self.output_widget,
            pane_widths=[4, 6, 0],
            pane_heights=[0,1,'100px']
        )
        
    def interact(self):
        display(self.widget)
        
    def get_AloeProgram(self): return self.ap
