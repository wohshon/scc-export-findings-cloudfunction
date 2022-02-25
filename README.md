### Demo script for exporting scc findings to gcs bucket

Cloud Function Deployment on `Python 3.9` 

Variables:

```
organization_id = os.environ['ORG_ID'] 
project_id = os.environ['PROJECT_ID'] 
time_window = os.environ['TIME_WINDOW_MINUTES']
bucket_name = os.environ['BUCKET'] 
```