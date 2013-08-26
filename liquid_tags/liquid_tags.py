from pelican import signals
from mdx_liquid_tags import LiquidTags
from pelican.readers import EXTENSIONS

def addLiquidTags(gen):
    if not gen.settings.get('MD_EXTENSIONS'):
        MDReader = EXTENSIONS['markdown']
        gen.settings['MD_EXTENSIONS'] = MDReader.default_extensions
    
    if LiquidTags not in gen.settings['MD_EXTENSIONS']:
        configs = dict(settings=gen.settings)
        gen.settings['MD_EXTENSIONS'].append(LiquidTags(configs))
 
def register():
    signals.initialized.connect(addLiquidTags)
