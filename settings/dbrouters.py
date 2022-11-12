class DbRouter:

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):

        if obj1._state.db == "default" or obj2._state.db == "default":
            return True
        return obj1._state.db == obj2._state.db

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if db == 'default':
            return True
        return False
