from google.cloud import bigquery


# Construct a BigQuery client object.
class DataService:
    def __init__(self):
        self.client = bigquery.Client().from_service_account_json("core/mspr-454808-baf9c7d409e4.json")
        self.data = {}

    def getDWData(self):
            query = """
                   SELECT *
                   FROM `mspr-454808.Legislative.LEG_CIRC_T2_MERGE_DW`
               """
            print('COUCOU')
            if not bool(self.data):
                print("GOING TO GET DW DATA")
                try:
                    rows = self.client.query_and_wait(query)  # Make an API request.
                    for row in rows:
                        # Row values can be accessed by field name or index.
                        self.data = row
                        print(row)
                except Exception as e:
                    print(e)
                print("The query data:")
