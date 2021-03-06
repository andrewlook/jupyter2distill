from __future__ import absolute_import

import os
import sys

import pytest

from ipynblog.config import *
from ipynblog.utils import load_yaml
from ipynblog.utils import dump_yaml

author_email = 'andrew.m.look@gmail.com'
author_name = 'Andrew Look'
colab_url = 'https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO'
dt = '2018-04-05'
project_name = 'deepdream--startup-breakfast--final'
project_slug = 'deepdream__startup_breakfast__final'

notebook_yaml = u"""
!NotebookMetadata
author_email: {author_email}
author_name: {author_name}
colab_url: {colab_url}
dt: '{dt}'
project_name: {project_name}
project_slug: {project_slug}
""".format(author_email=author_email,
           author_name=author_name,
           colab_url=colab_url,
           dt=dt,
           project_name=project_name,
           project_slug=project_slug)

nbconvert_template = './nbconvert/distill_v2_svelte.tpl'
nbconvert_input = './notebooks/test.ipynb'
nbconvert_output = './public/index.html'
images_dir = './public/images/'

default_template_yaml = u"""
!TemplateConfig
ipynblog_template: !IpynbTemplate
  nbconvert_template: {nbconvert_template}
  nbconvert_input: {nbconvert_input}
  nbconvert_output: {nbconvert_output}
  images_dir: {images_dir}
""".format(nbconvert_template=nbconvert_template,
           nbconvert_input=nbconvert_input,
           nbconvert_output=nbconvert_output,
           images_dir=images_dir)

updated_nbconvert_input = os.path.join('./notebooks', project_name)
colab_template_yaml = u"""
!TemplateConfig
ipynblog_template: !IpynbTemplate
  nbconvert_template: {nbconvert_template}
  nbconvert_input: {nbconvert_input}
  nbconvert_output: {nbconvert_output}
  images_dir: {images_dir}
  colab_url: {colab_url}
""".format(nbconvert_template=nbconvert_template,
           nbconvert_input=updated_nbconvert_input,
           nbconvert_output=nbconvert_output,
           images_dir=images_dir,
           colab_url=colab_url)


def __load_dump(y):
    """
    For testing purposes, sometimes the test fixture has different spacing/etc.
    So load & dump the expected result to obtain consistently-formatted data.

    :param y:   input YAML
    :return:    output YAML (w/ canonical formatting)
    """
    return dump_yaml(load_yaml(y))


def test_dump_notebook():
    nb = NotebookMetadata(author_email, author_name, colab_url,
                          dt, project_name, project_slug)
    assert __load_dump(notebook_yaml) == nb.dump()


def test_load_notebook():
    n = load_yaml(notebook_yaml)
    assert n.author_email == author_email


def test_dump_template_config():
    c = TemplateConfig(ipynblog_template=IpynbTemplate(
        nbconvert_template=nbconvert_template,
        nbconvert_input=updated_nbconvert_input,
        nbconvert_output=nbconvert_output,
        images_dir=images_dir,
        colab_url=colab_url,
    ))
    assert __load_dump(colab_template_yaml) == c.dump()


def test_load_and_dump_template_config():
    c = load_yaml(default_template_yaml)
    t = c.ipynblog_template
    assert t.nbconvert_template == nbconvert_template
    assert t.nbconvert_input == nbconvert_input
    assert t.nbconvert_output == nbconvert_output
    assert t.images_dir == images_dir
    assert t.colab_url == None

    t.colab_url = colab_url
    t.nbconvert_input = updated_nbconvert_input

    # assert __load_dump(colab_template_yaml) == c.dump()
    assert c.dump().strip() == """
ipynblog_template:
  colab_url: https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO
  images_dir: ./public/images/
  nbconvert_input: ./notebooks/deepdream--startup-breakfast--final
  nbconvert_output: ./public/index.html
  nbconvert_template: ./nbconvert/distill_v2_svelte.tpl
""".strip()


@pytest.mark.skipif(sys.version_info.major >= 3, reason="py2 only")
def test_no_unicode_preamble():
    """
    pyYAML is pretty verbose about datatypes, and if a unicode string is used this is what happens:

        !TemplateConfig
        ipynblog_template: !IpynbTemplate
          colab_url: https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO
          images_dir: ./public/images/
          nbconvert_input: !!python/unicode './notebooks/deepdream--startup-breakfast--final'
          nbconvert_output: ./public/index.html
          nbconvert_template: ./nbconvert/distill_v2_svelte.tpl

    Instead, I want this:

        !TemplateConfig
        ipynblog_template: !IpynbTemplate
          colab_url: https://colab.research.google.com/drive/1fjv0zVC0l-81QI7AtJjZPMfYRiynOJCB#scrollTo=Kp3QKj1KIaaO
          images_dir: ./public/images/
          nbconvert_input: ./notebooks/deepdream--startup-breakfast--final
          nbconvert_output: ./public/index.html
          nbconvert_template: ./nbconvert/distill_v2_svelte.tpl
    """
    c = load_yaml(default_template_yaml)
    t = c.ipynblog_template

    # explicitly change some props to unicode type (py2 only)
    t.colab_url = unicode(colab_url)
    t.nbconvert_input = unicode(updated_nbconvert_input)

    assert __load_dump(colab_template_yaml) == c.dump()

