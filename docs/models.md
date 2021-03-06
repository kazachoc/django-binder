# Using models

## Extra fields

Binder provides some extra fields you can use for your models.

- `UpperCaseCharField`
- `LowerCaseCharField`

```python
from binder.models import BinderModel, UpperCaseCharField

class Animal(BinderModel):
	name = UpperCaseCharField()
```

### BinderFileField / BinderImageField


When a model has a file attached to it, the url normally becomes something like this:

`/api/some_model/123/some_file_name/`

In this case, the frontend has to hit the file endpoint to know if the file has changes. When using BinderFileField / BinderImageField, the url will contain extra info encoded in the url:

`/api/some_model/123/some_file_name/?h=0759a35e9983833ce52fe433d2326addf400f344&content_type=image/jpeg`

- `h`: The sha1 of the file.
- `content_type`: The content type of the file.

You can upgrade from default Django FileField / ImageField as follows:

Old: `picture = models.FileField(blank=True, null=True)`
New: `picture = BinderFileField(blank=True, null=True)`

Old: `picture = models.ImageField(blank=True, null=True)`
New: `picture = BinderImageField(blank=True, null=True)`

Then, run `manage.py makemigrations` to add the required migrations.


## Enums

Binder makes it easy to use enums.

TODO: what exactly is the advantage of this over using `choices` directly?

```python
from binder.models import BinderModel, ChoiceEnum

class Animal(BinderModel):
	GENDER = ChoiceEnum('male', 'female')

	gender = models.CharField(max_length=6, choices=GENDER.choices())
```

## History

Binder can keep track of all mutations in a model.
Enabling this is very easy;

```python
from binder.models import BinderModel

class Animal(BinderModel):
	...

	class Binder:
		history = True
```

Saving the model will result in one changeset. With a changeset, the user that changed it and datetime is saved.

A changeset contains changes for each field that has been changed to a new value. For each change, you can see the old value and the new value.

Saving a new model also results in a changeset. It is possible to detect if a model is new by searching for the `id` column where the old value is `null`.

### Viewing the history

There are two ways to view the history; through the database, and via a built-in API endpoint.

Via the database, you can use the table `binder_changeset` to find a changeset you want to check. Note the ID, and open the `binder_change` table to view the exact changes.

To view the history through an API endpoint, add the following to your `urls.py`;

```python
import binder.views

urlpatterns = [
	url(r'^history/$',, binder.views.debug_changesets_24h, name='history'),
]
```

TODO: verify if this actually works.

Also make sure that `ENABLE_DEBUG_ENDPOINTS = True` in your `settings.py`.
