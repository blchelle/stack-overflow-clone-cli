from controllers import authController
import sys

# Validates that the user passed a correct amount of parameters
if (len(sys.argv) != 2):
	print('Incorrect amount of command-line parameters... Exiting')
	exit(-1)

# Gets the path to the db specified by the user
pathToDb = sys.argv[1]

# Runs the auth controller until either the user exits
# or has successfully authenticated
authController.AuthController(pathToDb).run()