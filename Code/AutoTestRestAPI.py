# install
# pip install flask, apispec, apispec-webframeworks, marshmallow

# run commands
# run http://127.0.0.1:5000/get_test_list
# run http://127.0.0.1:5000/docs

# links =>
# https://youtu.be/k10ILjUyWuQ?si=4BGzMRtv8PRD5V8i
# https://github.com/CodePossibility/flask-api-swagger-doc

# doc swager
# swager descriptor -> https://swagger.io/docs/specification/describing-request-body/

# example
# curl -X 'GET' 'http://127.0.0.1:5000/get_test_list' -H 'accept: application/json'

# ux + ui
# https://editor.wix.com/html/editor/web/renderer/edit/8d0eefb3-6f68-459e-8626-0858d521361c?metaSiteId=939ca1fd-8c40-48bd-be36-d63002e8a051&editorSessionId=ea894ee6-d4eb-4bdb-be5d-bc2f30bfc81e
# https://editor.wix.com/html/editor/web/renderer/edit/8d0eefb3-6f68-459e-8626-0858d521361c?metaSiteId=939ca1fd-8c40-48bd-be36-d63002e8a051&editorSessionId=ea894ee6-d4eb-4bdb-be5d-bc2f30bfc81e
import threading
import time
import PrepareTest_WEBGUI
import Global_Setting_Var
import Util
import testReadData
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory, request
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename
from flask_cors import CORS
from datetime import datetime
import multiprocessing
import MainAutoTest
import configparser
from pathlib import Path

#=======================================================================================================================
# Global Data
#=======================================================================================================================
app = Flask(__name__, template_folder='../swagger/templates')
CORS(app)

spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

#=======================================================================================================================
# Data Definition
#=======================================================================================================================
class VersionSchema(Schema):
    Main_Version = fields.Str()
    SE_Version = fields.Str()
    DBSim_Version = fields.Str()
    SimCore_Version = fields.Str()
    CGF_Version = fields.Str()
    Ownship_Version = fields.Str()
    IG_Version = fields.Str()
    CLS_Version = fields.Str()
    Motion_Version = fields.Str()
    Vibration_Version = fields.Str()
    LHD_Package_Version = fields.Str()
    AutoTest_System_Version = fields.Str()

class TestIdSchema(Schema):
    TestID = fields.Str()

class TestStepSchema(Schema):
    TestID = fields.Str()
    StepType = fields.Str()
    StepComment = fields.Str()

class ATP_PictureOptionSchema(Schema):
    TestID = fields.Str()
    WithPicture = fields.Boolean()

class ATR_PictureOptionSchema(Schema):
    PlanTestID = fields.Str()
    ResultTestID = fields.Str()
    WithPicture = fields.Boolean()
    PictureNumber = fields.Integer()

class TestSchema(Schema):
    TestID = fields.Str()
    MainVersion = fields.Str()
    Name = fields.Str()
    Summary = fields.Str()
    ResultThreshold = fields.Str()
    RunTimeout = fields.Str()
    Prerequisite = fields.Str()
    StartPoint = fields.Str()

class TestListSchema(Schema):
    list = fields.List(fields.Nested(TestSchema))

class ResultSchema(Schema):
        TestID = fields.Str()
        ResultID = fields.Str()
        FolderResultPath = fields.Str()

class ResultListSchema(Schema):
        list = fields.List(fields.Nested(ResultSchema))




#=======================================================================================================================
# Logger Last Commands
#=======================================================================================================================
def wite_to_logger_command(data, filename, write_mode):
    file = open(filename, write_mode)
    try:
        file.write(data)
    finally:
        file.close()

#=======================================================================================================================
# Swagger Route Definition
#=======================================================================================================================
@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('../swagger/static', secure_filename(path))

@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())

#=======================================================================================================================
# Create Main Version (as Gibraltar, ...)
#=======================================================================================================================
@app.route("/create_main_version", methods=["POST"])
def create_main_version():
    """Post create_main_version
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: VersionSchema
          """
    print('start -> create_main_version')
    _timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.is_json:
        request_json = request.get_json()

        # prepare data
        data = str('\n')
        data = '[create_main_version]\n'
        data = data + 'Topic                      = create_main_version \n'
        data = data + 'Timestamp                  = ' + str(_timestamp) + '\n'
        data = data + 'AutoTest_System_Version    = ' + request_json["AutoTest_System_Version"] + '\n'
        data = data + 'AutoTest_System_Version    = ' + request_json["AutoTest_System_Version"] + '\n'
        data = data + 'CGF_Version                = ' + request_json["CGF_Version"] + '\n'
        data = data + 'CLS_Version                = ' + request_json["CLS_Version"] + '\n'
        data = data + 'DBSim_Version              = ' + request_json["DBSim_Version"] + '\n'
        data = data + 'IG_Version                 = ' + request_json["IG_Version"] + '\n'
        data = data + 'LHD_Package_Version        = ' + request_json["LHD_Package_Version"] + '\n'
        data = data + 'Main_Version               = ' + request_json["Main_Version"] + '\n'
        data = data + 'Motion_Version             = ' + request_json["Motion_Version"] + '\n'
        data = data + 'Ownship_Version            = ' + request_json["Ownship_Version"] + '\n'
        data = data + 'SE_Version                 = ' + request_json["SE_Version"] + '\n'
        data = data + 'SimCore_Version            = ' + request_json["SimCore_Version"] + '\n'
        data = data + 'Vibration_Version          = ' + request_json["Vibration_Version"] + '\n'
        data = data + '\n'

        # dump to console
        print(data)

        # write to file
        wite_to_logger_command(data, 'D:\\ATH-AutoTestingSystem\\AutoTestingSystem_TempData\\request_create_main_version_file.ini', 'w')
        wite_to_logger_command(data, 'D:\\ATH-AutoTestingSystem\\AutoTestingSystem_TempData\\request_last_commands.ini', 'a')

        print(request_json)
        print('finish -> create_main_version')

        myfile = Path('D:\\ATH-AutoTestingSystem\\AutoTestingSystem_TempData\\Income_data.ini')
        config = configparser.ConfigParser()
        config.read(myfile)
        config.set('Update_Data_From_WEB', 'CreateMainVersion', 'True')
        config.write(myfile.open("w"))


        print('finish -> create_main_version')
        return request_json, 201

    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Create Test
#=======================================================================================================================
@app.route("/create_test", methods=["POST"])
def create_test():
    """Post create_test_plan
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: TestSchema
          """
    print('start -> create_test')
    _timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.is_json:
        request_json = request.get_json()

        # prepare data
        data = str('\n')
        data = '[create_test]\n'
        data = data + 'Topic       = create_test \n'
        data = data + 'TestID      = ' + str(request_json["TestID"]) + '\n'
        data = data + 'Timestamp   = ' + str(_timestamp) + '\n'
        data = data + 'MainVersion = ' + request_json["MainVersion"] + '\n'
        data = data + 'Name        = ' + request_json["Name"] + '\n'
        data = data + 'StartPoint  = ' + request_json["StartPoint"] + '\n'
        data = data + 'Summary     = ' + request_json["Summary"] + '\n'

        data = data + '\n'

        # dump to console
        print(data)


        # update the data for the creation of test
        WEB_Create_Test = "D:\ATH-AutoTestingSystem\AutoTestingSystem_TempData\create_test.ini"

        Util.replace_line(WEB_Create_Test, 5, "Name        ="+ data.split("\n")[5][-1])
        Util.replace_line(WEB_Create_Test, 6, "StartPoint        =" + data.split("\n")[6][-1])
        Util.replace_line(WEB_Create_Test, 7, "Summary        =" + data.split("\n")[7][-1])

        Income_data = "D:\ATH-AutoTestingSystem\AutoTestingSystem_TempData\Income_data.ini"
        Util.replace_line(Income_data, 2, "CurrectCommand      =2") # 2 = create test

        # update the data for the creation of test
        # write to file
        # wite_to_logger_command(data,'C:\\ATH\ATH-AutoTestingSystem\\AutoTestingSystem_TempData\\create_test.ini','w')
        # wite_to_logger_command(data,'C:\\ATH\ATH-AutoTestingSystem\\AutoTestingSystem_TempData\\request_last_commands.ini','a')
        wite_to_logger_command(data,'D:\\ATH-AutoTestingSystem\\AutoTestingSystem_TempData\\create_test.ini','w')
        wite_to_logger_command(data,'D:\\ATH-AutoTestingSystem\\AutoTestingSystem_TempData\\request_last_commands.ini','a')
        print('type is ', type(request))

        request_json = request.get_json()
        print('type is ', type(request_json))

        # main_c_mini()

        print(request_json)
        print('finish -> create_test')
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Run Test
#=======================================================================================================================
@app.route("/run_test", methods=["POST"])
def run_test():
    """Post run_test
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: TestIdSchema
          """
    print('start -> run_test')
    print(request)
    if request.is_json:
        request_json = request.get_json()
        testID = request_json["TestID"]
        print('ToDo Run Test ID ->', testID)
        print(request_json)
        print('finish -> run_test')

        PrepareTest_WEBGUI.arangeTheData(testID)

        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Stop Test
#=======================================================================================================================
@app.route("/stop_test", methods=["POST"])
def stop_test():
    """Post run_test
          ---
          post:
             requestBody:
                required: true
                content:
                    application/json:
                        schema: TestIdSchema
          """
    print('start -> stop_test')
    if request.is_json:
        request_json = request.get_json()
        print(request_json)
        print('finish -> stop_test')
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Preview Test
#=======================================================================================================================
@app.route("/preview_test", methods=["POST"])
def preview_test():
    """Post run_test
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: TestIdSchema
          """
    print('start -> preview_test')
    if request.is_json:
        request_json = request.get_json()
        print(request_json)
        print('finish -> preview_test')
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

# =======================================================================================================================
# Show Test
# =======================================================================================================================
@app.get("/show_test")
def show_test():
    """show_test
        ---
        get:
            description: show_test
            requestBody:
                required: true
                content:
                    application/json:
                        schema: TestIdSchema
            responses:
                200:
                    description: show_test
                    content:
                        application/json:
                            schema: TestSchema
        """
    print('start: call show test => ')
    print(str(test_list[0]))
    print('finish: call show test')
    return jsonify(test_list[0])

#=======================================================================================================================
# Duplicate Test
#=======================================================================================================================
@app.route("/duplicate_test", methods=["POST"])
def duplicate_test():
    """Post run_test
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: TestIdSchema
          """
    print('start -> duplicate_test')
    if request.is_json:
        request_json = request.get_json()
        print(request_json)
        print('finish -> duplicate_test')
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Delete Test
#=======================================================================================================================
@app.route("/delete_test", methods=["POST"])
def delete_test():
    """Post delete_test
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: TestIdSchema
          """
    print('start -> delete test')
    if request.is_json:
        request_json = request.get_json()
        print(request_json)
        print('finish -> delete test')
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Schegular Test
#=======================================================================================================================
@app.route("/schegular_test", methods=["POST"])
def schegular_test():
    """Post schegular_test
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: TestIdSchema
          """
    print('start -> schegular test')
    if request.is_json:
        request_json = request.get_json()
        print(request_json)
        print('finish -> schegular test')
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Create Test Step
#=======================================================================================================================
@app.route("/create_test_step", methods=["POST"])
def create_test_step():
    """Post run_test_step_by_type
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: TestStepSchema
          """
    print('start -> create_test_step')
    if request.is_json:
        print('type is ', type(request))

        request_json = request.get_json()
        print('type is ',  type(request_json))

        print(request_json)
        print('finish -> create_test_step')

        WEB_Income_data = "D:\ATH-AutoTestingSystem\AutoTestingSystem_TempData\Income_data.ini"
        WEB_Step_data = "D:\ATH-AutoTestingSystem\AutoTestingSystem_TempData\Step_data.ini"


        Util.replace_line(WEB_Income_data, 5, "CreateStep   		=0")
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Generate ATP
#=======================================================================================================================
@app.route("/generate_ATP", methods=["POST"])
def generate_ATP():
    """Post generate_ATP
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: ATP_PictureOptionSchema
          """
    print('start -> generate ATP')
    if request.is_json:
        request_json = request.get_json()
        print(request_json)
        print('finish -> generate ATP')
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Generate ATR
#=======================================================================================================================
@app.route("/generate_ATR", methods=["POST"])
def generate_ATR():
    """Post run_test_step_by_type
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: ATR_PictureOptionSchema
          """
    print('start -> run_test')
    if request.is_json:
        request_json = request.get_json()
        print(request_json)
        print('finish -> run_test')
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

#=======================================================================================================================
# Get All Test
#=======================================================================================================================
@app.get("/get_all_test")
def get_all_test():
    """Get Test List
        ---
        get:
            description: get_test_plan_list
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: TestListSchema
        """
    return jsonify(test_list)

#=======================================================================================================================
# Get All Result
#=======================================================================================================================
@app.get("/get_all_result")
def get_all_result():
    """Get get_all_result
        ---
        get:
            description: get_all_result
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: ResultListSchema
        """
    return jsonify(result_list)

#=======================================================================================================================
# Swagger Content
#=======================================================================================================================
with app.test_request_context():
    spec.path(view=create_main_version)
    spec.path(view=create_test)
    spec.path(view=run_test)
    spec.path(view=stop_test)
    spec.path(view=preview_test)
    spec.path(view=show_test)
    spec.path(view=duplicate_test)
    spec.path(view=get_all_test)
    spec.path(view=get_all_result)
    spec.path(view=generate_ATP)
    spec.path(view=generate_ATR)
    spec.path(view=schegular_test)
    spec.path(view=delete_test)
    spec.path(view=create_test_step)

#=======================================================================================================================
# Main
#=======================================================================================================================
def flask_run():
    print("Running RestAPI")
    app.run(debug=True, use_reloader=False)

def other_code():
    # Your other code here
    print("Running AutoTestBE")
    MainAutoTest.main()


if __name__ == '__main__':
    print(Global_Setting_Var.ParentDirTest)
    print(Global_Setting_Var.ParentDirResu)

    test_list = testReadData.returnDic(Global_Setting_Var.ParentDirTest)
    print("the test_list is ", test_list)

    result_list = testReadData.returnDic(Global_Setting_Var.ParentDirResu)
    print("the result_list is ", result_list)

    Logger_Resault = testReadData.bringLoggerData("D:\ATH-AutoTestingSystem\AutoTestingSystem_Backend\Results\currentresult.txt")
    print("the LOG_result_list is ", Logger_Resault)

    if __name__ == "__main__":
        flask_thread = threading.Thread(target=flask_run)
        other_thread = threading.Thread(target=other_code)

        flask_thread.start()

        # Allow some time for the Flask app to start before starting the other thread
        time.sleep(2)

        other_thread.start()

        flask_thread.join()  # Wait for the Flask thread to finish (when you stop the server manually)
        other_thread.join()  # Wait for the other thread to finish

