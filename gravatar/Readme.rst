Gravatar
--------

This plugin assigns the ``author_gravatar`` variable to the Gravatar URL and
makes the variable available within the article's context. You can add
``AUTHOR_EMAIL`` to your settings file to define the default author's email
address. Obviously, that email address must be associated with a Gravatar
account.

Alternatively, you can provide an email address from within article metadata::

    :email:  john.doe@example.com

If the email address is defined via at least one of the two methods above,
the ``author_gravatar`` variable is added to the article's context.
