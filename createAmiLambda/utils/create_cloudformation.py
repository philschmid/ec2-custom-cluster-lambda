import boto3

def create_cloudformation(image_id,cf_stack):
    template =  {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Stack 1",
        "Conditions": {
            "Never": {  
                "Fn::Equals": [
                    'true', 'false'
                ]} 
          
        },
        "Resources": {
            "NullResource": {
                "Type": "Custom::Null",
                "Condition":"Never"
        }
        },
        "Outputs": {
            "Nothing": {
                "Description": "Empty placeholder",
                "Value": image_id,
                "Export": {
                    "Name": "AMI-ID"
                }
            }
        }
    }
    template_json = json.dumps(template)
    cf_conn = boto3.client('cloudformation', region_name='eu-central-1')
    try:
        cf_conn.create_stack(
            StackName=cf_stack,
            TemplateBody=template_json,
        )
    except:
        cf_conn.update_stack(
            StackName=cf_stack,
            TemplateBody=template_json,
        )
    return True