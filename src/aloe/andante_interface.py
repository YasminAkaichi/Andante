from aloe.program import AloeProgram
from aloe.parser  import AloeParser, AloeText
from aloe.queryinterface import QueryInterface
from aloe.collections import OrderedSet

import itertools

import ipywidgets as widgets

HEIGHT = '300px'

DEFAULT_LAYOUT   = {'height':'auto', 'width':'auto'}
TEXT_LAYOUT = {'height': HEIGHT, 'width':'360px'}
MODE_LAYOUT = {'height': HEIGHT, 'width':'270px'}
DETE_LAYOUT = {'height': HEIGHT, 'width':'545px'}
STYLE = {'description_width': '30px'}

class AndateInterface:
    def __init__(self, ap=None, **options):
        self.parser = AloeParser()
        self.ap = ap if ap is not None else AloeProgram(options=options)
        
        self.qi = QueryInterface(ap, **options)
        self.di = DetailsInterface(self)
        self.induction_count = 0
        
        self.query_interface   = self.qi.widget
        self.details_interface = self.di.widget
        
        self.widget = widgets.Tab()
        self.widget.children = [self.query_interface, self.details_interface]
        self.widget.set_title(0, 'Query program')
        self.widget.set_title(1, 'Program details')
        
    def add_tab(self, widget, title):
        self.widget.children = list(self.widget.children) + [widget]
        self.widget.set_title(len(self.widget.children)-1, title)
        
    def add_induction_tab(self, widget):
        self.add_tab(widget, 'Induction #%d' % self.induction_count)
        self.induction_count += 1


DETAILS_CATEGORIES =  ['modeh', 'modeb', 'pos_examples', 'neg_examples', 'determination']
PARSER_CATEGORIES = {'modeh':'modeh', 'modeb':'modeb', 'pos_examples':'hornclause', 'neg_examples':'hornclause', 'determination':'determination'}
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
        self.old_details['modeh'].update(str(m) for _, m in self.ap.modes.modeh.items())
        self.old_details['modeb'].update(str(m) for _, m in self.ap.modes.modeb.items())
        self.old_details['determination'].update('determination(%s,%s).' % (modeh, modeb) for modeh in self.ap.modes.determinations for modeb in self.ap.modes.determinations[modeh])
        
    def update_details(self):
        to_remove = dict()
        to_add = dict()
        for category in DETAILS_CATEGORIES:
            at = AloeText(getattr(self, category+'_widget').children[1].value)
            at.preprocess()
            new = OrderedSet()
            new.update(at.get_clauses())
            old = self.old_details[category]
            
            to_remove[category] = [self.parser.parse_rule(c, PARSER_CATEGORIES[category]) for c in old if c not in new]
            to_add[category]    = [self.parser.parse_rule(c, PARSER_CATEGORIES[category]) for c in new if c not in old]
            
            self.old_details[category] = new
        
        for e in to_add['pos_examples']:
            self.ap.examples['pos'].add(e)
        for e in to_add['neg_examples']:
            self.ap.examples['neg'].add(e)
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
        details_toggle_button = widgets.ToggleButtons(
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
        
        def update_modeh(text):
            text = AloeText(text)
            text.preprocess()
            all_modeh = set(text.get_clauses())
                            
        v = lambda x: '\n'.join([c for c in x])
        self.modeh_widget = widgets.VBox([widgets.Label('Modeh'),
                                     widgets.Textarea(placeholder='Insert modeh atoms', layout=MODE_LAYOUT)])
        self.modeb_widget = widgets.VBox([widgets.Label('Modeb'),
                                     widgets.Textarea(placeholder='Insert modeb atoms', layout=MODE_LAYOUT)])
        self.determination_widget = widgets.VBox([widgets.Label('Determinations'),
                                             widgets.Textarea(placeholder='Insert determinations', layout=DETE_LAYOUT)])
        modehb_widget = widgets.HBox([self.modeh_widget, self.modeb_widget])
        modes_widget = widgets.VBox([modehb_widget, self.determination_widget])
        
        def save_options():
            for w in all_options_widget:
                try:
                    value = int(w.value)
                except:
                    value = w.value
                self.ap.set(w.description, value)
        save_options_button = widgets.Button(description='Save options')
        save_options_button.on_click(lambda x: save_options())
        all_options_widget = [widgets.Text(
            value=str(getattr(self.ap.options, attr)),
            placeholder='Insert a %s type' % type(attr),
            description=attr,) for attr in self.ap.options]
        option_widget = widgets.VBox(all_options_widget + [save_options_button])
        
        self.pos_examples_widget = widgets.VBox([widgets.Label('Positive examples'), 
                                            widgets.Textarea(placeholder='Insert positive examples', layout=TEXT_LAYOUT)])
        self.neg_examples_widget = widgets.VBox([widgets.Label('Negative examples'), 
                                            widgets.Textarea(placeholder='Insert negative examples', layout=TEXT_LAYOUT)])
        examples_widget = widgets.VBox([self.pos_examples_widget, self.neg_examples_widget])
        
        def launch_induction():
            self.save()
            save_options()
            self.ap.induce(update_knowledge=False, logging=True, verbose=0)
            self.ap.learner.logs[-1].build_widget()
            self.ai.add_induction_tab(self.ap.learner.logs[-1].widget)
            
        launch_induction_button = widgets.Button(description='Induce')
        launch_induction_button.on_click(lambda x: launch_induction())
        
        right_sidebar = widgets.HBox([modes_widget])
                
        save_button = widgets.Button(description='Save options')
        save_button.on_click(lambda x: self.save())
        header = widgets.HBox([
            widgets.HBox([save_button, launch_induction_button]), 
            details_toggle_button])
        header.layout.justify_content='space-between'
        self.widget = widgets.VBox([
            header, 
            widgets.AppLayout(
                right_sidebar=right_sidebar,
                center=examples_widget,
                pane_widths=[0, 4, 5.9],
            )],)
        

