from __future__ import unicode_literals
import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.utils import InvalidTemplateEngineError

from appconf import AppConf


default_filters = dict(
    css=['compressor.filters.css_default.CssAbsoluteFilter'],
    js=['compressor.filters.jsmin.JSMinFilter'],
    parcel=['compressor.filters.parceljs.ParserFilterJS'])


class CompressorConf(AppConf):
    # Main switch
    ENABLED = not settings.DEBUG
    # Allows changing verbosity from the settings.
    VERBOSE = False
    # GET variable that disables compressor e.g. "nocompress"
    DEBUG_TOGGLE = None
    # the backend to use when parsing the JavaScript or Stylesheet files
    PARSER = 'compressor.parser.AutoSelectParser'
    OUTPUT_DIR = 'CACHE'
    STORAGE = 'compressor.storage.CompressorFileStorage'
    PRIVATE_DIRS = ()

    COMPRESSORS = dict(
        css='compressor.css.CssCompressor',
        js='compressor.js.JsCompressor',
        parcel='compressor.parceljs.ParcelJsCompressor'
    )

    URL = None
    ROOT = None

    # Filters are resolved in configure()
    FILTERS = {}
    CSS_FILTERS = None
    JS_FILTERS = None
    PARCEL_FILTERS = None

    CSS_HASHING_METHOD = 'mtime'

    PRECOMPILERS = (
        # ('text/coffeescript', 'coffee --compile --stdio'),
        # ('text/less', 'lessc {infile} {outfile}'),
        # ('text/x-sass', 'sass {infile} {outfile}'),
        # ('text/stylus', 'stylus < {infile} > {outfile}'),
        # ('text/x-scss', 'sass --scss {infile} {outfile}'),
    )
    CACHEABLE_PRECOMPILERS = ()
    CLOSURE_COMPILER_BINARY = 'java -jar compiler.jar'
    CLOSURE_COMPILER_ARGUMENTS = ''
    YUI_BINARY = 'java -jar yuicompressor.jar'
    YUI_CSS_ARGUMENTS = ''
    YUI_JS_ARGUMENTS = ''
    YUGLIFY_BINARY = 'yuglify'
    YUGLIFY_CSS_ARGUMENTS = '--terminal'
    YUGLIFY_JS_ARGUMENTS = '--terminal'
    CLEAN_CSS_BINARY = 'cleancss'
    CLEAN_CSS_ARGUMENTS = ''
    DATA_URI_MAX_SIZE = 1024

    # the cache backend to use
    CACHE_BACKEND = None
    # the dotted path to the function that creates the cache key
    CACHE_KEY_FUNCTION = 'compressor.cache.simple_cachekey'
    # rebuilds the cache every 30 days if nothing has changed.
    REBUILD_TIMEOUT = 60 * 60 * 24 * 30  # 30 days
    # the upper bound on how long any compression should take to be generated
    # (used against dog piling, should be a lot smaller than REBUILD_TIMEOUT
    MINT_DELAY = 30  # seconds
    # check for file changes only after a delay
    MTIME_DELAY = 10  # seconds
    # enables the offline cache -- also filled by the compress command
    OFFLINE = False
    # invalidates the offline cache after one year
    OFFLINE_TIMEOUT = 60 * 60 * 24 * 365  # 1 year
    # The context to be used when compressing the files "offline"
    OFFLINE_CONTEXT = {}
    # The name of the manifest file (e.g. filename.ext)
    OFFLINE_MANIFEST = 'manifest.json'
    # The Context to be used when TemplateFilter is used
    TEMPLATE_FILTER_CONTEXT = {}
    # Placeholder to be used instead of settings.COMPRESS_URL during offline compression.
    # Affects manifest file contents only.
    URL_PLACEHOLDER = '/__compressor_url_placeholder__/'

    # Returns the Jinja2 environment to use in offline compression.
    def JINJA2_GET_ENVIRONMENT():
        alias = 'jinja2'
        try:
            from django.template import engines
            return engines[alias].env
        except InvalidTemplateEngineError:
            raise InvalidTemplateEngineError(
                "Could not find config for '{}' "
                "in settings.TEMPLATES. "
                "COMPRESS_JINJA2_GET_ENVIRONMENT() may "
                "need to be defined in settings".format(alias))
        except ImportError:
            return None

    class Meta:
        prefix = 'compress'

    def configure_root(self, value):
        # Uses Django's STATIC_ROOT by default
        if value is None:
            value = settings.STATIC_ROOT
        if value is None:
            raise ImproperlyConfigured('COMPRESS_ROOT defaults to ' +
                                       'STATIC_ROOT, please define either')
        return os.path.normcase(os.path.abspath(value))

    def configure_private_dirs(self, value):
        if not isinstance(value, (list, tuple)):
            raise ImproperlyConfigured("The COMPRESS_PRIVATE_DIRS setting "
                                       "must be a list or tuple. Check for "
                                       "missing commas.")
        from compressor.finders import PrivateFileSystemFinder
        privatefiles = PrivateFileSystemFinder()
        errors = privatefiles.check()
        if errors:
            raise ImproperlyConfigured(errors[0])
        return value

    def configure_url(self, value):
        # Uses Django's STATIC_URL by default
        if value is None:
            value = settings.STATIC_URL
        if not value.endswith('/'):
            raise ImproperlyConfigured("URL settings (e.g. COMPRESS_URL) "
                                       "must have a trailing slash")
        return value

    def configure_cache_backend(self, value):
        if value is None:
            value = 'default'
        return value

    def configure_offline_context(self, value):
        if not value:
            value = {'STATIC_URL': settings.STATIC_URL}
        return value

    def configure_template_filter_context(self, value):
        if not value:
            value = {'STATIC_URL': settings.STATIC_URL}
        return value

    def configure_precompilers(self, value):
        if not isinstance(value, (list, tuple)):
            raise ImproperlyConfigured("The COMPRESS_PRECOMPILERS setting "
                                       "must be a list or tuple. Check for "
                                       "missing commas.")
        return value

    def configure(self):
        data = self.configured_data
        for kind in {'css', 'js', 'parcel'}:
            setting_name = '%s_FILTERS' % kind.upper()
            filters = data.pop(setting_name)
            if filters is not None:
                # filters for this kind are set using <kind>_FILTERS
                if kind in data['FILTERS']:
                    raise ImproperlyConfigured(
                        "The setting {kind_setting} "
                        "conflicts with {main_setting}['{kind}']. "
                        "Remove either setting and update the other to "
                        "the correct list of filters for {kind} resources"
                        ", we recommend you keep the latter."
                        .format(
                            kind_setting=self._meta.prefixed_name(setting_name),
                            main_setting=self._meta.prefixed_name('FILTERS'),
                            kind=kind))
                data['FILTERS'][kind] = filters
            elif kind not in data['FILTERS']:
                # filters are not defined
                data['FILTERS'][kind] = default_filters[kind]
        return data
