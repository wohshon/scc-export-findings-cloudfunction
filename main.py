from google.cloud import securitycenter
import os
import json
from google.protobuf import field_mask_pb2
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
import datetime
from google.cloud import storage

# Env variables
organization_id = os.environ['ORG_ID'] 
project_id = os.environ['PROJECT_ID'] 
time_window = os.environ['TIME_WINDOW_MINUTES']
#bucket name without the prefixes
bucket_name = os.environ['BUCKET']

# Create a client.
scc_client = securitycenter.SecurityCenterClient()
storage_client = storage.Client()
org_name = "organizations/{org_id}".format(org_id=organization_id)
result_list = []

def save_findings(contents, destination_blob_name):
    print('uploading findings')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents)
    print('uploaded ...{}'.format(destination_blob_name))

def get_findings():
    # all_sources = "{org_name}/sources/-".format(org_name=org_name)
    source_name = "projects/{project_id}/sources/-".format(project_id=project_id)

    # end_time = datetime.datetime.now(tz=timezone.utc)
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(minutes=int(time_window))
    print("current time {now}".format(now=end_time))
    print("filter event time from {start} to {end}".format(end=end_time, start=start_time))
    # print("filter event time from {start}".format(start=start_time))
    # convert to eppoch millisec 
    # filter = "event_time > {start} AND event_time<{end}".format(end=round(end_time.timestamp()), start=round(start_time.timestamp()))
    # epoch in ms
    filter = "event_time > {start}".format(start=round(start_time.timestamp()*1000))
    print(filter)
    finding_result_iterator = scc_client.list_findings(
        request={"parent": source_name, "filter": filter}
        )
    for i, finding_result in enumerate(finding_result_iterator):
        # string , use MessageToDict if dict is required
        json_str = MessageToJson(finding_result._pb ,preserving_proto_field_name=True)
        result_list.append(json_str)
        # json_dict = MessageToDict(finding_result._pb ,preserving_proto_field_name=True)
        #print(json_dict["finding"]["event_time"])
        # print(json_str)
        results = ",".join(result_list)
        return "["+results+"]"


def start(request):
    findings = get_findings()
    print("found {count} results".format(count=str(len(result_list))))
    filename = "findings-{timestamp}.json".format(timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
    save_findings(findings,filename)  
    return f'Completed'
