**last updated**

Mon May 21 08:03:49 CDT 2018
----------------------------

WIP
---

* add feature to save petri-net designs
  * require auth to save (on s3? / filesystem)
  * allow user-created schemata

BACKLOG
-------

* ACL on schema creation / all RPC commands

* update brython app enhance PetriNet  editor
  * edit update properties on select
  * support clickable handles on arcs
  * allow arc creation with > 1 token weight

ICEBOX
-------

* add E-Tags for all responses - set proper 304 status instead of 200
  * NOTE: could this be done by an upstream websever like nginx instead?

* remove all other string substitions from ./storage/postgres.py
  in favor of using composable features of psycopg2 :
  http://initd.org/psycopg/docs/sql.html#psycopg2.sql.SQL.join
  http://initd.org/psycopg/docs/sql.html#psycopg2.sql.Placeholder

* allow users to run only the API serving w/ twisted (production mode)
  * consider making the editor into an Admin UI

* re-examine use of 'roles' - leveraging inhibitor arcs
  * enhance or remove feature
