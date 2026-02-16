.. _sec-api-version:

*******************
Version information
*******************

.. http:get:: /api/version

   Retrieve information regarding server and API version. 
   
   If no specific API version was requested, or an API version that predates 1.12.0, this returns a JSON object with three keys, ``api`` set to ``0.1``, 
   ``server`` containing the server version, ``text`` containing the server version including the prefix ``OctoPrint`` (to determine that this is indeed 
   a genuine OctoPrint instance).

   If an API version of 1.12.0 or higher was requested, this returns a JSON object with two keys, ``server`` containing the server version and
   ``text`` containing the server version including the prefix ``OctoPrint`` (to determine that this is indeed a genuine OctoPrint instance).

   **Example Request: No requested API version**

   .. sourcecode:: http

      GET /api/version HTTP/1.1
      Host: example.com
      X-Api-Key: abcdef...

   **Example Response**

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "api": "0.1",
        "server": "1.12.0",
        "text": "OctoPrint 1.12.0"
      }

   **Example Request: Requested API version of 1.12.0**

   .. sourcecode:: http

      GET /api/version HTTP/1.1
      Host: example.com
      X-OctoPrint-Api-Version: 1.12.0
      X-Api-Key: abcdef...

   **Example Response**

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "server": "1.12.0",
        "text": "OctoPrint 1.12.0"
      }

   :statuscode 200: No error

   .. changed:: 1.12.0

      Now versioned based on the :ref:`version header <>`. For requested versions of 1.12.0 or higher the ``api`` key on the response has been dropped.
