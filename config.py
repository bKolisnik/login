import os
#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_file = "mysql://username:password@localhost/{}".format(os.path.join(project_dir, "dbname"))

#database_directory = "mysql+mysqldb://root:brendan@localhost/test"
#must manually create the mysql database above is only connection for tables

class Config(object):
	#database_directory = "mysql+mysqldb://root:brendan@localhost/test"
	database_directory = "postgresql://localhost/brendankolisnik"
	#heroku publishes uri to database in $DATABASE_URL environment variable.

	#SQLALCHEMY_DATABASE_URI = self.database_directory
	#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #'sqlite:///' + os.path.join(basedir, 'app.db')

    #in heroku use the environment variable otherwise use my local database
	if os.environ.get('DATABASE_URL') is None:
		SQLALCHEMY_DATABASE_URI = database_directory
	else:
		print(os.environ['DATABASE_URL'])
		SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = 'p9Bv<3Eid9%$i01'
	