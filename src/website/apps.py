from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = "website"

    def ready(self):
        from django.db.backends.signals import connection_created
        from django.dispatch import receiver

        @receiver(connection_created)
        def setup_sqlite(connection, **kwargs):
            if connection.vendor != "sqlite":
                return
            with connection.cursor() as cursor:
                cursor.execute("pragma journal_mode = WAL;")
                cursor.execute("pragma synchronous = NORMAL;")
                cursor.execute("pragma busy_timeout = 10000;")
                cursor.execute("pragma temp_store = memory;")
                cursor.execute("pragma mmap_size = 256000000;")
