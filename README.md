# hera_mc

[![Build Status](https://travis-ci.org/HERA-Team/hera_mc.svg?branch=master)](https://travis-ci.org/HERA-Team/hera_mc)
[![Coverage Status](https://coveralls.io/repos/github/HERA-Team/hera_mc/badge.svg?branch=master)](https://coveralls.io/github/HERA-Team/hera_mc?branch=master)

This is the main repository for HERA's monitor and control subsystems.
Installation instructions may be found in [INSTALL.md](./INSTALL.md).

# CM-only users
*Note:  if you are only using hera_mc to locally use configuration management (cm) info via sqlite, you may ignore most of this.
        if this is the case, follow the simplified instructions in INSTALL.md*



# Adding a new table

To add a new table into the M&C database:

First, ensure that the database is configured correctly by running `alembic upgrade head`. If this fails, refer to the direction in [INSTALL.md](./INSTALL.md).

Be sure to do all your work on a branch off of master.

1. Create a new module under `hera_mc`, basing on e.g. `subsystem_error.py` or `observation.py`.
2. Add `from . import my_new_module` line in `__init__.py`.
3. Add methods to interact with your new table. This is most commonly done in `mc_session.py`, and there are many examples there to refer to.
4. Add testing code to cover these methods. -- Be sure to `python setup.py install` before the next step.
5. Run `alembic revision --autogenerate -m 'version description'` to create a new alembic revision file that will reflect the changes to the database schema you just introduced. Inspect the resulting file carefully -- alembic's autogeneration is very clever but it's certainly not perfect. It tends to make more mistakes with table or column alterations than with table creations.
4. Run `alembic upgrade head` to apply your schema changes -- be sure to `python setup.py install` first. At this point it's a very good idea to inspect the database table (using the psql command line) to make sure the right thing happened. It's also a very good idea to run `alembic downgrade -1` to back up to before your revision and check that the database looks right (of course you then need to re-run the upgrade command to get back to where you meant to be.)
5. Run `nosetests` to check that all the tests pass.
6. git add the alembic/version that was created and commit your work.
7. When you're satisfied that everything works as expected, add a description of your new table to the documentation -- to cm.tex if it's a configuration management table or to mc_definition.tex otherwise.
8. Create a pull request on github to ask for a code review and to get your changes integrated into master.
9. Once the changes have been incorporated into master, you can log onto site, pull the master branch and run `alembic upgrade head` to update the onsite database to the new schema.

# Deleting all the tables in a database (in psql shell)
This can be useful to do on your local machine if your database is in a weird state. Never do this on site!!!
```
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```
If you get an error like `no schema has been selected to create in...` it means that you need to fix permissions like this:
```
grant usage on schema public to public;
grant create on schema public to public;
```

# Deleting a database
This can be useful to do on your local machine if your database is in a weird state. Never do this on site!!!
`dropdb hera_mc`

# Using alembic for the first time with an existing (non-empty) database
If you already have a database filled out with tables but have never run alembic before, you have two choices to start using alembic:

Option 1) Drop all the tables (if you don't care about the data in the database this is easiest, see instructions above) and then run `alembic upgrade head`.

Option 2) identify which alembic version your database schema corresponds to and add a new table to your database called `alembic_version` with one column called 'version_num'. Fill this table with one row with the alembic version number that corresponds to your schema version to tell alembic where to start trying to upgrade from. Then run `alembic upgrade head`.

# Running psql on qmaster

This runs under the HERA conda environment on qmaster.  

To check environments: `conda info --envs`

To change environments:  `source activate HERA`

To run psql:  `psql -U hera -h qmaster hera_mc`

# Restoring a database backup

We are now regularly backing up the database to the Librarian and copying it to NRAO. The database backup files can be found by searching for them on the librarian using `obsid-is-null`. The files are named like `maint.YYYYMMDD.karoo.mandc.dbbackup.pgdump`.

Once you've downloaded the files, you can create the database (using postgres) like this:

`pg_restore -cCOx  -d hera_mc  maint.20180213.karoo.mandc.dbbackup.pgdump`
