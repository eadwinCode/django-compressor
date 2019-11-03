Django Compressor with Parcel-Bundler
=====================================

.. image:: https://codecov.io/github/django-compressor/django-compressor/coverage.svg?branch=develop
    :target: https://codecov.io/github/django-compressor/django-compressor?branch=develop

.. image:: https://img.shields.io/pypi/v/django_compressor.svg
        :target: https://pypi.python.org/pypi/django_compressor

.. image:: https://secure.travis-ci.org/django-compressor/django-compressor.svg?branch=develop
    :alt: Build Status
    :target: http://travis-ci.org/django-compressor/django-compressor

.. image:: https://caniusepython3.com/project/django_compressor.svg
    :target: https://caniusepython3.com/project/django_compressor

Django Compressor with parcel-bundler_ is base on Django-Compressor, which bundles and minifies your typescript, vue, react, etc in a Django template into cacheable static files using parcel-bundler.
More information on Django-Compressor_


Quickstart
----------
Install django-compress::

    pip install git+https://github.com/eadwinCode/django-compressor/django-compressor.git
 
Install parcel-bundler::

    npm install -g parcel-bundler

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'compressor',
        ...
    )
    
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        # other finders..
        'compressor.finders.CompressorFinder',
    )

Other Configurations
--------------------

To minify your code for production, you need to set COMPRESS_ENABLED to true in settings.py

.. code-block:: python

    COMPRESS_ENABLED = True
or

.. code-block:: python

    DEBUG = False
For more information django-compressor-settings_

Usage
-----
In your template, load compress ``{% load compress %}``
then use ``{% compress parcel %} <script> {% endcompress %}`` to load a script. for example:

.. code-block:: html

    {% load static %} 
    {% load compress %}
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>Vue Django Testing</title>
      </head>
      <body>
        ....
       {% compress parcel file myts %}
        <script src="{% static 'js/index.ts' %}"></script>
       {% endcompress %}
      </body>
      ...
      
Vue example
-----------
Create a vue project in your django project root ::

    npm init --yes
    npm install -D vue-template-compiler, @vue/component-compiler-utils
    npm install vue
    
In your django project app create ::

    static/components/test.vue
    static/js/index.js
    
In static/components/test.vue,

.. code-block:: vue

    <template>
      <div>
        <h1>{{ message }}</h1>
      </div>
    </template>

    <script>
        export default {
          name: "app",
          components: {},
          data: {
            message: "Hello Vue",
          },
          computed: {}
        };
        </script>

    <style lang="scss">
    </style>
In static/js/index.js,

.. code-block:: javascript

    import Vue from "vue";
    import test  from "../components/test.vue";
    new Vue(test).$mount("#components-demo");

In your django template,

.. code-block:: html
    
    {% load static %} 
    {% load compress %}
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>Vue Django Testing</title>
      </head>
      <body>
        ....
       <div id="components-demo"></div>
       {% compress parcel file myts %}
         <script src="{% static 'js/index.js' %}"></script>
       {% endcompress %}
      </body>
      ...

Run ``runserver`` ::

    python manage.py runserver

You have successfully bundled your vue app into your django template.  
    
.. _Django-Compressor: https://github.com/django-compressor/django-compressor
.. _parcel-bundler: https://parceljs.org
.. _django-compressor-settings: https://django-compressor.readthedocs.io/en/latest/settings/