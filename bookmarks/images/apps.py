from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'  # name of application
    verbose_name = 'Image bookmarks'  # human readable name.

    def ready(self):
        # import signal handlers (loads the signals when app is ready)
        import images.signals
