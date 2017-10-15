"""
Generic Tag
-----------
This implements a tag that that is mostly useful for testing.

This tag does not implement anything useful, but is a place that can be
used for testing liquid_tags infrastructure, in situations that need
a full lifecycle test.

The first use case is a test of a tag that will pull out data from
the configuration file and make it available during the test.

A tag of
{% generic config <config file variable> %>
will be replaced with the value of that config file in html

Not all config file variables are exposed - the set
of variables are from the LIQUID_CONFIGS setting, which is a list of 
variables to pass to the liquid tags.
"""
from .mdx_liquid_tags import LiquidTags

@LiquidTags.register('generic')
def generic(preprocessor, tag, markup):
    (cmd, args) = markup.split(' ', 1)
    if cmd.lower() == 'config':
        config_param = args.split()[0].upper()
        config_val = preprocessor.configs.getConfig(config_param)	
        return(config_val)
    else:
        return 'generic: %s ' % markup

#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register

