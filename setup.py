#!/usr/bin/env python

from distutils.core import setup

import twoauth

setup(name='twoauth',
      version = twoauth.__version__,
      description  = 'Python OAuth support Twitter REST API library',
      author  = 'Hirotaka Kawata',
      author_email ='info@techno-st.net',
      url     = twoauth.__url__,
      license = twoauth.__license__,
      packages=['twoauth']
      )
