import pymysql
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

pymysql.install_as_MySQLdb()


#paypal https://developer.paypal.com/docs/checkout/reference/server-integration/setup-sdk/#set-up-the-environment
# Creating Access Token for Sandbox
client_id = "AQhmiJx4prLV2BbSfIx17acEmxGmyJt5hb8WmlH9807YGSzIC5QtovKc6ZqSBusNSdoIzY2DfWZLCjrR"
client_secret = "EGeSsHtlzAfRy-iGJr_KAlUMgdG-IYrU1fVubmqD8KCy_iUIq468_jjXhbYa2H3WBUsugxhJlNA5Go3j"
# Creating an environment
environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)