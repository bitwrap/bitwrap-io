**last updated**

Tue Jul  3 09:52:55 CDT 2018
----------------------------

WIP
---

* add octofree schema

BACKLOG
-------
* require authentication

* ACL on schema creation / all RPC commands

* consider if we need to refactor github auth to make it optional

  * use case is: I want to host an API server to just use JWT bearer tokens

* add a way to change schemata names when uploading pnml

ICEBOX
-------

* fork to create gitwrap.com - hosted editing and testing of petri-nets

  * enforce Auth via rest API & socketio connections
  * allow user-created schemata - ( saved in db or s3 )
  * add feature to save petri-net designs
  * require auth to save (on s3? / filesystem)
  * no guarenteed db storage (maybe publish events to s3 bucket)
  * allow end users to bind listeners to specific schema/oid combos
  * POC feature to save petri-net designs (no auth)

* perhaps change cursor style for various objects when editor changes modes

* remove all other string substitions 

    from ./storage/postgres.py
    in favor of using composable features of psycopg2:
    http://initd.org/psycopg/docs/sql.html#psycopg2.sql.SQL.join
    http://initd.org/psycopg/docs/sql.html#psycopg2.sql.Placeholder

