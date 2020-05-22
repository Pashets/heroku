from wtforms import Form, StringField, TextAreaField, SelectField, FieldList, SelectMultipleField


class ProjectForm(Form):
    name = StringField('Name')
    description = TextAreaField('Description')
    quantity_participants = SelectField(u'Quantity of participants',
                                        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])


class TaskForm(Form):
    title = StringField('Title')
    description = TextAreaField('Description')
