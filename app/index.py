import os
import sys
import csv

# import magic
import boto3
import bottle
from bottle import run, template, debug, static_file, request, BaseRequest, jinja2_view, route

dirname = os.path.dirname(sys.argv[0])

app = application = bottle.Bottle()

BUCKET_NAME = "csvmanagerproject"
BaseRequest.MEMFILE_MAX = 8096 * 1024  # 8mb
debug(True)


def upload_s3(filepath=None, filename=None, bucket_name=BUCKET_NAME):
    if filename and filepath:
        s3 = boto3.client('s3')
        with open(filepath, 'rb') as data:
            s3.upload_fileobj(data, bucket_name, filename)
        return True
    else:
        return False


def fetch_s3_file(filename=None, bucket_name=BUCKET_NAME):
    s3_client = boto3.client('s3')
    save_path = "downloads/csvmanager/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path, file=filename)
    try:
        s3_client.download_file(Bucket=bucket_name,
                                Key=filename,
                                Filename=file_path)
        return file_path, True
    except Exception as e:
        return e, False


def list_s3(bucket_name=BUCKET_NAME):
    if bucket_name:
        file_list = []
        s3_client = boto3.client('s3')
        response = s3_client.list_objects(Bucket=bucket_name)
        for keys in response['Contents']:
            file_list.append(keys['Key'])
        return file_list
    else:
        return []


@app.route('/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='./static/asset/css')


@app.route('/static/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root='./static/asset/js')


@app.route('/')
def index():
    data = {"developer_name": "Mudasir Mirza",
            "developer_project": "Bottle CSV Project"}
    s3_file_list = list_s3()
    return template('index', data=data, file_list=s3_file_list)


@app.route('/upload', method='POST')
def do_upload():
    if request.method == 'POST':
        upload = request.files.get('my_upload')
        name, ext = os.path.splitext(upload.filename)
        if ext != '.csv':
            return "File extension not allowed."
        save_path = "uploads/csvmanager/"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        with open(file_path, 'wb') as open_file:
            open_file.write(upload.file.read())
        if upload_s3(file_path, upload.filename):
            s3_message = "File Upload to S3: SUCCESS"
        else:
            s3_message = "File Upload to S3: FAILURE"
        csv_data = read_csv(file_path)
        return template('view', items=csv_data,
                        s3_message=s3_message,
                        data={"developer_name": "Mudasir Mirza", "developer_project": "Bottle CSV Project"})


@app.route("/read_file/<filename:re:.*\.csv>")
def read_file(filename):
    csv_file, bl = fetch_s3_file(filename)
    if bl:
        csv_data = read_csv(csv_file)
        s3_message = "File data from S3: SUCCESS"
    else:
        csv_data = []
        s3_message = "File data from S3: FAILURE"
    return template('view', items=csv_data,
                    s3_message=s3_message,
                    data={"developer_name": "Mudasir Mirza", "developer_project": "Bottle CSV Project"})


def read_csv(file_path, local=False):
    csvdata = []
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f, delimiter=",")
        for row in csv_reader:
            if not row[0]:
                continue
            csvdata.append(row)
    return csvdata


class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)


if __name__ == "__main__":
    bottle.run(app=StripPathMiddleware(app),
        host='0.0.0.0',
        port=8080)
