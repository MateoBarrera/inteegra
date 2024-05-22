import os.path as op
import pandas as pd
from flask import request, redirect, url_for, current_app as app
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin import helpers, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.form.upload import FileUploadField
from werkzeug.utils import secure_filename
from wtforms.validators import StopValidation


class UserModelView(ModelView):
    can_delete = False
    create_modal = True
    page_size = 10

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return super(MyAdminIndexView, self).index()


class DataModelView(ModelView):
    @staticmethod
    def file_validation(form, field):
        if field.data:
            filename = field.data.filename
            print(filename)
            request_table = request.path.split("/")[2]
            if filename[-4:] == '.csv':
                df = pd.read_csv(field.data)
            elif filename[-5:] == '.xlsx':
                df = pd.read_excel(field.data, engine='openpyxl')
            else:
                raise StopValidation('File format is not supported.')

            return app.db_object.update_from_admin(table=request_table, data=df.to_dict(orient='records'))

        return False

    @staticmethod
    def prefix_name(obj, file_data):
        parts = op.splitext(file_data.filename)
        return secure_filename('file-%s%s' % parts)

    def __init__(self, model, *args, **kwargs):
        print("Se ejecuta al menos")
        self.can_export = True
        self.column_display_pk = True
        self.export_types = ['csv', 'xlsx']
        path = op.join(op.dirname(__file__), 'data')
        self.form_extra_fields = {
            'file': FileUploadField('file', namegen=self.prefix_name, base_path=path, validators=[self.file_validation], allowed_extensions=self.export_types)
        }
        # self.form_overrides = dict(file=FileUploadField('file', namegen=self.prefix_name, base_path=path, validators=[self.file_validation]))
        self.form_args = {
            'file': {
                'label': 'File',
                'base_path': path,
                'allow_overwrite': False,
                'validators': [self.file_validation]
            }
        }
        super(DataModelView, self).__init__(model, *args, **kwargs)


class MyFileAdminView(FileAdmin):
    can_delete = False
