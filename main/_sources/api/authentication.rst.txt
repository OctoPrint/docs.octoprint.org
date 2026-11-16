.. _sec-api-authentication:

**************
Authentication
**************

.. _sec-api-authentication-login:

Login
=====

.. http:post:: /api/login

   Creates a login session or retrieves information about the currently existing session ("passive login").

   Can be used in one of two ways: to login a user via username and password and create a persistent session (usually
   from a UI in the browser), or to retrieve information about the active user (from an existing session or an API key)
   via the ``passive`` flag.

   Will return a :http:statuscode:`200` with a :ref:`login response <sec-api-authentication-datamodel-login>` on successful
   login, whether active or passive. The active (username/password) login may also return a :http:statuscode:`403` in
   case of a username/password mismatch, unknown user or a deactivated account.

   .. warning::

      Previous versions of this API endpoint did return a :http:statuscode:`401` in case of a username/password
      mismatch or an unknown user. That was incompatible with basic authentication since it was a wrong use of
      the :http:statuscode:`401` code and got therefore changed as part of a bug fix.

   .. note::

      You cannot use this endpoint to login from a third party page via CORS, see above. You can however use it
      to retrieve user information via passive login with an API key (e.g. if you need the ``session`` to authenticate
      on the web socket.

   :json passive:  If present, performs a passive login only, returning information about the current user that's
                   active either through an existing session or the used API key
   :json user:     (active login only) Username
   :json pass:     (active login only) Password
   :json remember: (active login only) Whether to set a "remember me" cookie on the session
   :status 200:    Successful login
   :status 403:    Username/password mismatch, unknown user or deactivated account

.. _sec-api-authentication-logout:

Logout
======

.. http:post:: /api/logout

   Ends the current login session of the current user.

   Only makes sense in the context of browser based workflows.

   Will return a :http:statuscode:`204`.

   :status 204: No error

.. _sec-api-authentication-currentuser:

Current User
============

.. http:get:: /api/currentuser

   Retrieves information about the current user.

   Will return a :http:statuscode:`200` with a :ref:`current user object <sec-api-authentication-datamodel-currentuser>`
   as body.

   :status 200: No error

.. _sec-api-authentication-datamodel:

Data model
==========

.. _sec-api-authentication-datamodel-login:

Login response
--------------

The Login response is a :ref:`user record <sec-api-datamodel-access-users>` extended by the following fields:

.. list-table::
   :widths: 15 5 10 30
   :header-rows: 1

   * - Name
     - Multiplicity
     - Type
     - Description
   * - ``session``
     - 1
     - string
     - The session key, can be used to authenticate with the ``auth`` message on the :ref:`push API <sec-api-push>`.
   * - ``_is_external_client``
     - 1
     - boolean
     - Whether the client that made the request got detected as external from the local network or not.

.. _sec-api-authentication-datamodel-currentuser:

Current user
------------

.. list-table::
   :widths: 15 5 10 30
   :header-rows: 1

   * - Name
     - Multiplicity
     - Type
     - Description
   * - ``name``
     - 1
     - string
     - The id of the current user. Unset if guest.
   * - ``permissions``
     - 0..n
     - List of :ref:`permission records <sec-api-datamodel-access-permissions>`
     - The effective list of permissions assigned to the user
   * - ``groups``
     - 0..n
     - List of :ref:`permission records <sec-api-datamodel-access-groups>`
     - The list of groups assigned to the user
