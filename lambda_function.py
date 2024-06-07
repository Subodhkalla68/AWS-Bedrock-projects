import json
import base64
#1. import boto3
import boto3
import random
#2. Create client connection with Bedrock and S3 Services
client_bedrock = boto3.client('bedrock-runtime')
client_s3 = boto3.client('s3')
#3. Store the input data (prompt) in a variable
def lambda_handler(event, context):
    input_prompt = event["prompt"]
    print(input_prompt)
#4. Create a Request Syntax to access the Bedrock Service 
    response_bedrock = client_bedrock.invoke_model(contentType = 'application/json', accept = 'application/json', modelId = 'stability.stable-diffusion-xl-v1', 
        body = json.dumps ({"text_prompts": [{ "text": input_prompt }], 'seed': 0}))
    print(response_bedrock)
#5. 5a. Retrieve from Dictionary, 5b. Convert Streaming Body to Byte using json load 5c. Print
    response_bedrock_byte = json.loads(response_bedrock['body'].read())
    print(response_bedrock_byte)
#6. 6a. Retrieve data with artifact key, 6b. Import Base 64, 6c. Decode from Base64
    response_bedrock_base64=response_bedrock_byte['artifacts'][0]['base64']
    response_bedrock_finalimage = base64.b64decode(response_bedrock_base64)
    print(response_bedrock_finalimage)
#7. 7a. Upload the File to S3 using Put Object Method – Link 7b. Import datetime 7c. Generate the image name to be stored in S3 - Link
    img_name = 'dogimage' + str(random.random())
    
    response_s3 = client_s3.put_object(
        Bucket = 'mys3buck12',
        Body = response_bedrock_finalimage,
        Key = img_name)
#8. Generate Pre-Signed URL
    generate_presigned_url = client_s3.generate_presigned_url('get_object', Params={'Bucket': 'mys3buck12', 'Key': img_name}, ExpiresIn=3600, HttpMethod=None)
    print(generate_presigned_url)
    return {
        'statusCode': 200,
        'body': (generate_presigned_url)
    }
