from pelican import signals
from pelican.generators import Generator

import os


class CssGenerator(Generator):

    def generate_context(self):
        pass

    def generate_output(self, writer):
        css_path = os.path.join(self.output_path, 'theme', 'css')
        for template in self.env.list_templates():
            if 'css' in template:
                # if css path not exist it gets created
                if not os.path.exists(css_path):
                    os.makedirs(css_path)
                dst = os.path.join(css_path, template)
                tpl = self.env.get_template(
                    template)
                rurls = self.settings['RELATIVE_URLS']
                writer.write_file(dst, tpl, self.context, rurls,
                                  override_output=True)


def get_generators(generators):
    return CssGenerator


def register():
    signals.get_generators.connect(get_generators)
