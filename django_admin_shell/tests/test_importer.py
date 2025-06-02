from unittest import mock
from django.test import TestCase
from django_admin_shell.views import Importer
from django_admin_shell.tests.models import TestModel
from django.apps import apps


class ImporterTest(TestCase):

    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", False)
    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", False)
    def test_autoimport_disable(self):
        imp = Importer()
        assert imp.get_modules() == {}
        assert imp.get_scope() == {}

    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", True)
    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", False)
    @mock.patch(
        "django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO_MODULES",
        {
            'django.conf': ['settings', 'non_exist_attr'],
            'non_exist_mod': ['foo_bar_baz'],
        }
    )
    def test_autoimport_django(self):
        from django.conf import settings
        imp = Importer()
        assert imp.get_modules() == {'django.conf': ['settings']}
        assert imp.get_scope() == {'settings': settings}

    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", False)
    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", True)
    def test_autoimport_models(self):
        imp = Importer()
        assert imp.get_modules()['django_admin_shell.tests.models'] == ['TestModel']
        assert issubclass(imp.get_scope()['TestModel'], TestModel)

    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", True)
    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", False)
    @mock.patch(
        "django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO_MODULES",
        {
            'django_admin_shell.views': ['Importer', 'Runner', 'ShellView', 'XYZ'],
            'non_exist_mod': ['foo_bar_baz'],
        }
    )
    def test_autoimport_str(self):
        imp = Importer()
        assert str(imp) == "from django_admin_shell.views import Importer, Runner, ShellView\n"

    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", False)
    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", True)
    def test_dynamic_models(self):
        """
        Test that the importer handles dynamic models gracefully.

        This simulates a situation where a model is registered with Django's app registry
        but doesn't exist as an attribute in its declared module.
        """
        # Create a fake dynamic model class and register it with Django's app registry
        class Meta:
            app_label = 'django_admin_shell'

        dynamic_model_name = 'DynamicTestModel'
        module_name = 'django_admin_shell.tests.models'

        DynamicTestModel = type(
            dynamic_model_name,
            (TestModel,),
            {'Meta': Meta, '__module__': module_name}
        )
        original_get_models = apps.get_models

        def mock_get_models():
            return list(original_get_models()) + [DynamicTestModel]

        with mock.patch('django.apps.apps.get_models', side_effect=mock_get_models):
            imp = Importer()

            modules = imp.get_modules()
            assert dynamic_model_name in modules[module_name]

            # Get scope should not crash even though the model doesn't exist in the module
            scope = imp.get_scope()
            # Our dynamic model shouldn't be in the scope since it's not in the module
            assert dynamic_model_name not in scope
            # But the TestModel should still be there
            assert 'TestModel' in scope
