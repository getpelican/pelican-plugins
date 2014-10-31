from pelican import signals
from .mdx_liquid_tags import LiquidTags, LT_CONFIG


def addLiquidTags(gen):
    if not gen.settings.get('MD_EXTENSIONS'):
        from pelican.settings import DEFAULT_CONFIG
        gen.settings['MD_EXTENSIONS'] = DEFAULT_CONFIG['MD_EXTENSIONS']

    if LiquidTags not in gen.settings['MD_EXTENSIONS']:
        configs = dict()
        for key,value in LT_CONFIG.items():
            configs[key]=value
        for key,value in gen.settings.items():
            if key in LT_CONFIG:
                configs[key]=value
        gen.settings['MD_EXTENSIONS'].append(LiquidTags(configs))


def register():
    signals.initialized.connect(addLiquidTags)
