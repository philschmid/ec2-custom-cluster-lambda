

def create_user_data(iam_profil,count):
    return '''#!/bin/bash
export PYTHONIOENCODING=utf8 &&
export AWS_ACCESS_KEY_ID=$(curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/'''+iam_profil+''' | \
                python -c "import sys, json; print json.load(sys.stdin)['AccessKeyId']") &&
export AWS_SECRET_ACCESS_KEY=$(curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/'''+iam_profil+''' | \
                python -c "import sys, json; print json.load(sys.stdin)['SecretAccessKey']")
for i in {1..'''+count+'''}
do
  docker run --name translator_"$i" -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e region=eu-central-1 -d philschmi/insight-translator-gpu
done
'''

