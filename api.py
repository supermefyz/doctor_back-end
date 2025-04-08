import os
import csv
import re

from flask import Flask, request, jsonify, session
import requests
from flask_cors import CORS
from openai import OpenAI
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash
import datetime
from sqlalchemy import or_
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=30)  # 设置会话过期时间为 30 分钟
app.config['SESSION_PERMANENT'] = True
# app.config["SESSION_COOKIE_SAMESITE"] = "None" # 设置前后端为相同地址的不同端口
# app.config["SESSION_COOKIE_SECURE"] = True  # 开启后必须启用 HTTPS，否则无法保持session
# app.config["SESSION_COOKIE_DOMAIN"] = "None"  # 设置 Cookie 的 Domain
app.config["SESSION_COOKIE_PATH"] = "/"           # 设置 Cookie 的 Path
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/medical_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app, supports_credentials=True)

# 数据库模型
class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    medical_history = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    suggestion = db.Column(db.Text, nullable=True)
    recommendation = db.Column(db.Text, nullable=True)        # 新增字段：推荐医生信息
    time = db.Column(db.Date, nullable=False)

class DoctorRecord(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)  # 关键改进6：密码哈希存储


class AdminRecord(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)  # 关键改进6：密码哈希存储


# 创建数据库表（如果尚不存在）
with app.app_context():
    db.create_all()

# API 配置
KIMI_API_KEY = 'sk-rq2IjpECMygXCXTzrBLz68Y21y42ful6l70QKobifqi1hfWy'
KIMI_API_URL = 'https://api.moonshot.cn/v1/chat/completions'
OPENAI_API_KEY = "sk-b5878471f7ff4f43b2bde9cbe3e12994"
openai_client = OpenAI(api_key=OPENAI_API_KEY, base_url="https://api.deepseek.com")

BLOCKED_WORDS = ['#', '-', '*']

@app.route('/api/submit_user_info', methods=['POST'])
def submit_user_info():
    session['user_info'] = request.json
    print(session['user_info'])
    session['question_count'] = 0
    session['chat_history'] = []

    # 插入用户信息到数据库
    new_record = MedicalRecord(
        name=session['user_info']['name'],
        age=int(session['user_info']['age']),
        gender=session['user_info']['gender'],
        height=int(session['user_info']['height']),
        weight=int(session['user_info']['weight']),
        phone=session['user_info']['phone'],
        medical_history=session['user_info'].get('medicalHistory', ''),
        diagnosis=session['user_info'].get('diagnosis', ''),
        suggestion=session['user_info'].get('suggestion', ''),
        recommendation=None,
        time=session['user_info'].get('time', datetime.datetime.now())  # 默认时间
    )
    db.session.add(new_record)
    db.session.commit()
    print(f'id:{new_record.id}')
    session['record_id'] = new_record.id
    return jsonify({"message": "用户信息已保存"}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    user_info = session.get('user_info')
    print(user_info)
    user_message = request.json.get('message')
    print(user_message)
    question_count = session.get('question_count', 0)  # 获取当前问题计数
    chat_history = session.get('chat_history', [])

    if not user_info:
        return jsonify({"error": "用户信息缺失"}), 400

    # 更新问题计数
    session['question_count'] = question_count + 1

    # 添加用户消息到历史记录
    chat_history.append({'user': user_message})

    # 前三次调用 Kimi API
    if question_count < 3:
        return chat_with_kimi(user_info, user_message, question_count, chat_history)
    # 第四次及以后调用 Deepseek + 知识库
    else:
        return chat_with_openai(user_message, chat_history)

def contains_blocked_words(message):
    return any(word in message for word in BLOCKED_WORDS)

def filter_response(response):
    for word in BLOCKED_WORDS:
        response = response.replace(word, '*' * len(word))
    return response

def chat_with_kimi(user_info, user_message, question_count, chat_history):
    system_message = (
        "你是一位专业医生，正在通过问诊收集信息。每次回复必须包含1个关键问题，问题应：\n"
        "1. 聚焦可能病因\n2. 按优先级排序\n3. 使用'是否有...''请描述...'等引导句式\n"
        "示例格式：\n"
        "1. 是否有头痛症状？\n2. 症状持续多久了？\n3. 是否有过敏史？"
    )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user",
         "content": f"患者档案：{user_info['name']}，{user_info['age']}岁，{user_info['gender']}，身高{user_info['height']}，体重{user_info['weight']}，病史：{user_info['medicalHistory']}"},
        {"role": "user", "content": user_message}
    ]

    try:
        response = requests.post(
            KIMI_API_URL,
            json={
                "model": "moonshot-v1-8k",
                "messages": messages,
                "temperature": 0.3
            },
            headers={'Authorization': f'Bearer {KIMI_API_KEY}'}
        ).json()

        print(response)  # 打印API返回内容

        assistant_message = response['choices'][0]['message']['content']
        assistant_message = filter_response(assistant_message)

        chat_history.append({'assistant': assistant_message})
        session['chat_history'] = chat_history

        return jsonify({"choices": [{"message": {"content": assistant_message},"isOver":False}]}), 200
    except KeyError as ke:
        return jsonify({"error": f"KeyError: {ke}. API response: {response}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def read_csv_file(file_path):
    """读取1.csv文件的内容"""
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # 使用 DictReader 读取 CSV 文件
            content = []
            for row in reader:
                content.append(", ".join([f"{key}: {value}" for key, value in row.items()]))
            return "\n".join(content)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return ""

def query_knowledge_base(query):
    try:
        with open("output_data.txt", "r", encoding="utf-8") as f:
            entries = [line.strip() for line in f if line.strip()]

        # 简单关键词匹配（实际应使用向量搜索等更复杂方法）
        keywords = set(query.lower().split())
        return "\n".join([entry for entry in entries
                          if any(kw in entry.lower() for kw in keywords)][:3]) or "无相关知识库记录"
    except:
        return "知识库暂不可用"

def update_database(record_id: int, diagnosis: str, suggestion: str, recommendation: str):
    """
    更新数据库中的诊断结果、建议和推荐的科室及医生信息。
    :param record_id: 数据库记录的主键 ID
    :param diagnosis: 诊断结果
    :param suggestion: 诊断建议
    :param recommendation: 推荐科室和医生
    """
    # 查询数据库中的记录
    record = MedicalRecord.query.get(record_id)
    if not record:
        raise ValueError(f"未找到 ID 为 {record_id} 的记录")

    # 更新记录字段
    record.diagnosis = diagnosis
    record.suggestion = suggestion
    record.recommendation = recommendation

    # 提交更改
    db.session.commit()

    print(f"Updated database - Record ID: {record_id}, Diagnosis: {diagnosis}, Suggestion: {suggestion}, recommendation: {recommendation}")

def chat_with_openai(user_message, chat_history):
    try:
        # 构建诊断上下文
        user_info = session.get('user_info', {})
        medical_context = (
                f"患者信息：{user_info.get('name')}，{user_info.get('age')}岁，{user_info.get('gender')}，"
                f"身高{user_info.get('height')}，体重{user_info.get('weight')}，病史：{user_info.get('medicalHistory')}\n"
                "问诊记录：\n" +
                "\n".join([f"{i + 1}. 患者：{h.get('user', '无用户消息')}\n   医生：{h.get('assistant', '无医生回复')}"
                           for i, h in enumerate(chat_history)])
        )

        # 知识库查询（示例实现）
        knowledge = query_knowledge_base(medical_context + "\n" + user_message)
        print(f"Knowledge Base Query Result: {knowledge}")  # 打印知识库查询结果

        # 读取1.csv文件的内容
        csv_file_content = read_csv_file("1.csv")  # 假设文件路径为当前目录下的1.csv
        if not csv_file_content:
            csv_file_content = "未找到排班表或推荐信息。"

        # 构建深度求索请求
        response = openai_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": (
                    "你是一位临床医生，请根据以下信息进行诊断。\n"
                    "请以固定格式返回结果：\n"
                    "------\n"
                    "诊断结果:\n"
                    "------\n"
                    "诊断建议\n"
                    "------\n"
                    "推荐科室和医生（根据排班表推荐），并给出理由\n"
                    "注意：必须严格按照上述格式返回，不能省略或更改分隔符。"
                )},
                {"role": "user", "content": (
                    f"知识库信息：\n{knowledge}\n"
                    f"患者信息及问诊记录：\n{medical_context}\n"
                    f"当前症状：{user_message}\n"
                    f"排班表及推荐信息：\n{csv_file_content}\n"
                    "提示词：请根据排班表中的实际科室和医生安排，推荐最适合患者的科室和医生。"
                )}
            ]
        )
        print("OpenAI API Response:", response)  # 打印OpenAI API返回内容

        diagnosis = response.choices[0].message.content
        diagnosis = filter_response(diagnosis)
                # 调用解析函数
        checkMessage(diagnosis, session.get('record_id'))
        # 将诊断结果存入对话历史
        chat_history.append({'assistant': diagnosis})
        session['chat_history'] = chat_history

        return jsonify({"choices": [{"message": {"content": diagnosis},"isOver":True,"id":session.get('record_id')}]}), 200
    except KeyError as ke:
        return jsonify({"error": f"KeyError: {ke}. OpenAI API response: {response if 'response' in locals() else 'No response received'}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/submit_diagnosis', methods=['POST'])
def submit_diagnosis():
    try:
        # 获取请求中的 AI 返回消息和记录 ID
        data = request.json
        ai_message = data.get('ai_message')
        record_id = data.get('record_id')

        if not ai_message or not record_id:
            return jsonify({"error": "缺少必要参数"}), 400

        # 调用解析函数
        checkMessage(ai_message, record_id)

        return jsonify({"message": "诊断信息已保存"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def checkMessage(message: str, record_id: int):
    try:
        # 使用正则表达式分割不同部分
        parts = re.split(r'\*{6}', message.strip())
        print(parts)
        if len(parts) < 4:
            raise ValueError("消息格式错误，缺少必要部分")

        # 提取各部分内容
        diagnosis = parts[1].strip().replace("诊断结果:", "").strip()
        suggestion = parts[2].strip().replace("诊断建议:", "").strip()
        recommendation = parts[3].strip()


        # 更新数据库
        update_database(
            record_id=record_id,
            diagnosis=diagnosis,
            suggestion=suggestion,
            recommendation=recommendation,
        )

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise  # 传递异常给调用者


@app.route('/api/user_info', methods=['GET'])
def get_user_info():
    return jsonify(session.get('user_info', {}))


# 根据 ID 获取记录
@app.route('/api/get_record_by_id', methods=['GET'])
def get_record_by_id():
    print('get_record_by_id')
    # 从查询参数中获取 ID
    record_id = request.args.get('id')
    print(record_id)
    if not record_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    try:
        # 将 ID 转换为整数
        record_id = int(record_id)
    except ValueError:
        return jsonify({"error": "Invalid 'id' parameter"}), 400

    try:
        # 查询数据库
        record = MedicalRecord.query.get(record_id)

        if record is None:
            return jsonify({"error": "Record not found"}), 404

        # 将记录转换为字典
        record_data = {
            "id": record.id,
            "name": record.name,
            "age": record.age,
            "gender": record.gender,
            "height": record.height,
            "weight": record.weight,
            "phone": record.phone,
            "medical_history": record.medical_history,
            "diagnosis": record.diagnosis,
            "suggestion": record.suggestion,
            "recommendation": record.recommendation,
            "time": record.time.isoformat() if record.time else None,  # 处理日期格式
        }

        # 返回记录信息
        return jsonify(record_data), 200

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({"error": str(e)}), 500

# 获取分页病人信息
@app.route('/api/get_records', methods=['GET'])
def get_records():
    # 获取请求参数
    page = request.args.get('page', 1, type=int)
    record_id = request.args.get('id', type=int)
    name = request.args.get('name')
    per_page = 10

    # 参数有效性验证
    if 'id' in request.args and record_id is None:
        return jsonify({"error": "Invalid id format, must be integer"}), 400

    # 构建基础查询（按时间倒序）
    records_query = MedicalRecord.query.order_by(MedicalRecord.time.desc())

    # 添加过滤条件
    if record_id is not None:
        records_query = records_query.filter(MedicalRecord.id == record_id)
    if name:
        records_query = records_query.filter(MedicalRecord.name.ilike(f"%{name}%"))  # 模糊匹配

    # 计算分页数据
    total_records = records_query.count()
    total_pages = (total_records + per_page - 1) // per_page
    paginated = records_query.paginate(page=page, per_page=per_page, error_out=False)

    # 构建响应数据
    return jsonify({
        "current_page": page,
        "total": total_records,  # 返回实际总数而非计算值
        "records": [{
            "id": rec.id,
            "name": rec.name,
            "time": rec.time.strftime('%Y-%m-%d')
        } for rec in paginated.items]
    }), 200


# 医生登录
@app.route('/doctor/login', methods=['POST'])
def doctor_login():
    # 参数校验
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "status": 400,
            "message": "缺少必要参数: username 或 password",
            "data": None
        }), 400

    username = data['username']
    password = data['password']

    try:
        # 使用.first()提高查询效率
        doctor = DoctorRecord.query.filter_by(name=username).first()

        # 密码哈希验证
        if doctor and check_password_hash(doctor.password_hash, password):
            return jsonify({
                "status": 200,
                "message": "登录成功",
                "data": {
                    "user_id": doctor.id,
                    "status": doctor.status
                }
            })

        return jsonify({
            "status": 401,
            "message": "用户名或密码错误",
            "data": None
        }), 401

    except Exception as e:  # 关键改进5：异常捕获
        app.logger.error(f"登录异常: {str(e)}")
        return jsonify({
            "status": 500,
            "message": "服务器内部错误",
            "data": None
        }), 500


# 重置医生密码
@app.route('/doctor/update-password', methods=['POST'])
def update_password():
    data = request.get_json()

    # 参数校验
    if not data or 'username' not in data or 'new_password' not in data:
        return jsonify({"status": 400, "message": "缺少必要参数"}), 400

    try:
        doctor = DoctorRecord.query.filter_by(name=data['username']).first()
        if not doctor:
            return jsonify({"status": 404, "message": "用户不存在"}), 404

        doctor.password = data['new_password']  # 自动触发哈希存储
        db.session.commit()

        return jsonify({
            "status": 200,
            "message": "密码已更新",
            "data": {"user_id": doctor.id}
        })

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"密码更新失败: {str(e)}")
        return jsonify({"status": 500, "message": "服务器错误"}), 500

# 管理员登陆
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    print(data)
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"status": 400,"message": "缺少必要参数","data": None}),400

    username = data['username']
    password = data['password']

    try:
        # 使用.first()提高查询效率
        admin = AdminRecord.query.filter_by(username=username).first()

        # 密码哈希验证
        if admin and check_password_hash(admin.password_hash, password):
            return jsonify({
                "status": 200,
                "message": "登录成功",
                "data": {
                    "user_id": admin.id,
                }
            })

        return jsonify({
            "status": 401,
            "message": "用户名或密码错误",
            "data": None
        }), 401

    except Exception as e:  # 关键改进5：异常捕获
        app.logger.error(f"登录异常: {str(e)}")
        return jsonify({
            "status": 500,
            "message": "服务器内部错误",
            "data": None
        }), 500


# 管理员注册
@app.route('/admin/register', methods=['POST'])
def admin_register():
    """
    管理员注册接口
    请求JSON格式：
    {
        "username": "管理员用户名",
        "password": "明文密码"
    }
    """
    data = request.get_json()

    # 参数校验
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "status": 400,
            "message": "必需参数: username 和 password",
            "data": None
        }), 400

    # 清理输入
    username = data['username'].strip()
    password = data['password'].strip()

    try:
        # 检查用户名唯一性
        if AdminRecord.query.filter_by(username=username).first():
            return jsonify({
                "status": 409,
                "message": "用户名已存在",
                "data": None
            }), 409

        # 创建新管理员
        new_admin = AdminRecord(username=username)
        new_admin.password = password  # 触发哈希存储

        db.session.add(new_admin)
        db.session.commit()

        return jsonify({
            "status": 200,
            "message": "管理员创建成功",
            "data": {
                "id": new_admin.id,
                "username": new_admin.username
            }
        }), 200

    except ValueError as e:
        # 捕获密码策略错误（如需）
        return jsonify({
            "status": 400,
            "message": str(e),
            "data": None
        }), 400

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"注册失败: {str(e)}")
        return jsonify({
            "status": 500,
            "message": "服务器内部错误",
            "data": None
        }), 500


# 患者统计接口
@app.route('/api/get_patient_count', methods=['GET'])
def get_patient_count():
    try:
        total = MedicalRecord.query.count()
        finished = MedicalRecord.query.filter(
            MedicalRecord.suggestion.isnot(None),
            MedicalRecord.suggestion != ''
        ).count()

        return jsonify({
            "patientCount": total,
            "finishPatientCount": finished,
            "unFinishPatientCount": total - finished
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 医生统计接口
@app.route('/api/get_doctor_count', methods=['GET'])
def get_doctor_count():
    try:
        total = DoctorRecord.query.count()

        return jsonify({
            "doctorCount": total,
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 分页获取医生信息
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        # 解析请求参数
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '')

        # 参数校验
        if page < 1:
            page = 1

        # 构建基础查询
        query = DoctorRecord.query

        # 添加搜索条件
        if search:
            query = query.filter(
                or_(
                    DoctorRecord.name.ilike(f'%{search}%'),
                    DoctorRecord.department.ilike(f'%{search}%')
                )
            )

        # 执行分页查询
        pagination = query.paginate(page=page, per_page=10, error_out=False)

        # 构建返回数据
        doctors = [{
            "id": doctor.id,
            "name": doctor.name,
            "department": doctor.department,
            "phone":doctor.phone,
            "status":doctor.status
        } for doctor in pagination.items]

        return jsonify({
            "data": doctors,
            "pagination": {
                "page": page,
                "total_items": pagination.total,
                "total_pages": pagination.pages
            }
        }), 200

    except Exception as e:
        return jsonify({
            "error": "服务器内部错误",
            "message": str(e)
        }), 500


# 根据id删除医生
@app.route('/api/doctors', methods=['DELETE'])
def delete_doctor():
    doctor_id=request.args.get('doctor_id')
    try:
        # 检查医生是否存在
        doctor = DoctorRecord.query.get(doctor_id)
        if not doctor:
            return jsonify({
                "error": "资源不存在",
                "message": f"医生ID {doctor_id} 未找到"
            }), 404

        # 执行删除
        db.session.delete(doctor)
        db.session.commit()

        return jsonify({
            "code": 204,
            "message": "删除成功",
            "data": {
                "deleted_id": doctor_id
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "删除失败",
            "message": str(e)
        }), 500

# 更新医生信息
@app.route('/api/doctors', methods=['PUT'])
def update_doctor():
    try:
        # 参数校验
        if request.json['id']=='':
            print(request.json)
            # 创建新医生
            new_doctor = DoctorRecord(
                name=request.json['name'],
                department=request.json.get('department'),
                phone=request.json.get('phone'),
                password=request.json['password'],  # 自动触发哈希
                status=request.json.get('status'),
            )

            db.session.add(new_doctor)
            db.session.commit()

            return jsonify({
                "message": "Doctor created successfully",
                "data": {
                    "id": new_doctor.id,
                    "name": new_doctor.name,
                    "department": new_doctor.department,
                    "phone": new_doctor.phone,
                    "status": new_doctor.status
                }
            }), 201  # 注意使用201 Created状态码

        doctor_id = request.json['id']
        doctor = DoctorRecord.query.get(doctor_id)

        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        # 更新字段处理
        update_fields = []
        if 'name' in request.json:
            doctor.name = request.json['name']
            update_fields.append('name')

        if 'department' in request.json:
            doctor.department = request.json['department']
            update_fields.append('department')

        if 'phone' in request.json:
            doctor.phone = request.json['phone']
            update_fields.append('phone')

        # 密码单独处理
        if 'password' in request.json:
            if len(request.json['password']) < 6:
                return jsonify({"error": "Password must be at least 6 characters"}), 400
            doctor.password = request.json['password']  # 自动触发password.setter
            update_fields.append('password')

        # 权限处理
        if 'status' in request.json:
            doctor.status = bool(request.json['status'])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        # 保存修改
        db.session.commit()

        return jsonify({
            "message": "Doctor updated successfully",
            "data": None
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": str(e)
        }), 500

@app.route('/api/delete_record', methods=['DELETE'])
def delete_record():
    id=request.args.get('id')
    try:
    # 检查医生是否存在
        record = MedicalRecord.query.get(id)
        if not record:
            return jsonify({
                "error": "资源不存在",
                "message": f"ID {id} 未找到"
            }), 404

        # 执行删除
        db.session.delete(record)
        db.session.commit()

        return jsonify({
            "code": 204,
            "message": "删除成功",
            "data": None
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "删除失败",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
