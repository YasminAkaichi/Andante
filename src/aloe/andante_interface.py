from aloe.program import AloeProgram
from aloe.parser  import AloeParser, AloeText
from aloe.queryinterface import QueryInterface

import ipywidgets as widgets

DEFAULT_LAYOUT   = {'height':'auto', 'width':'auto'}
TEXT_LAYOUT = {'height': '400px', 'width':'99%'}
MODE_LAYOUT = {'height': '200px', 'width':'98%'}
STYLE = {'description_width': '30px'}


class AndateInterface:
    def __init__(self, ap=None, **options):
        self.parser = AloeParser()
        self.ap = ap if ap is not None else AloeProgram(options=options)
        
        self.query_interface = QueryInterface(ap, **options).widget
        self.build_details_interface()
        
        self.widget = widgets.Tab()
        self.widget.children = [self.query_interface, self.details_interface]
        self.widget.set_title(0, 'Query program')
        self.widget.set_title(1, 'Program details')

    def build_details_interface(self):
        self.details_interface = None
        
        details_toggle_button = widgets.ToggleButtons(
            options=['Modes', 'Options'],
            button_style='info',
            tooltips=['Show modes', 'Show options'],
            layout={'height':'auto', 'width':'auto'},
        )
        def fun(option):
            if option=='Modes':
                self.details_interface.children[1].right_sidebar.children = [modes_widget]
            else:
                mode_text = modeh_widget.children[1].value + modeb_widget.children[1].value + determination_widget.children[1].value
                if mode_text:
                    self.ap.modes = self.parser.parse_rule(mode_text, 'header')['modehandler']
                self.details_interface.children[1].right_sidebar.children = [option_widget]
        details_toggle_button.observe(lambda info: fun(info['new']) if info['type']=='change' and info['name']=='value' else None)
        
        def update_modeh(text):
            text = AloeText(text)
            text.preprocess()
            all_modeh = set(text.get_clauses())
                            
        v = lambda x: '\n'.join([c for c in x])
        modeh_widget = widgets.VBox([widgets.Label('Modeh'),
                                     widgets.Textarea(placeholder='Insert modeh atoms', layout=MODE_LAYOUT)])
        modeb_widget = widgets.VBox([widgets.Label('Modeb'),
                                     widgets.Textarea(placeholder='Insert modeb atoms', layout=MODE_LAYOUT)])
        determination_widget = widgets.VBox([widgets.Label('Determinations'),
                                             widgets.Textarea(placeholder='Insert determinations', layout=MODE_LAYOUT)])
        modehb_widget = widgets.HBox([modeh_widget, modeb_widget])
        modes_widget = widgets.VBox([modehb_widget, determination_widget])
        
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
        
        pos_examples_widget = widgets.VBox([widgets.Label('Positive examples'), 
                                            widgets.Textarea(placeholder='Insert positive examples', layout=MODE_LAYOUT)])
        neg_examples_widget = widgets.VBox([widgets.Label('Negative examples'), 
                                            widgets.Textarea(placeholder='Insert negative examples', layout=MODE_LAYOUT)])
        examples_widget = widgets.VBox([pos_examples_widget, neg_examples_widget])
        
        def launch_induction():
            save_options()
            self.ap.induce(update_knowledge=False, logging=True, verbose=0)
            self.ap.learner.logs[-1].build_widget()
            self.widget.children = list(self.widget.children) + list(self.ap.learner.logs[-1].widget.children)
            
        launch_induction_button = widgets.Button(description='Induce')
        launch_induction_button.on_click(lambda x: launch_induction())
        
        right_sidebar = widgets.HBox([modes_widget])
        self.details_interface = widgets.VBox([
            widgets.HBox([launch_induction_button, 
                          details_toggle_button]), 
            widgets.AppLayout(
                right_sidebar=right_sidebar,
                center=examples_widget,
                pane_widths=[0, 5, 4.9],
            )])