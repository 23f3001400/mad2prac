from flask_restful import Api, Resource, reqparse
from .models import *
from .database import db
from flask_security import auth_required,roles_accepted,roles_required,current_user

api = Api()

def roles_list(roles):
    role_list = []
    for role in roles:
        role_list.append(role.name)
    return role_list

parser = reqparse.RequestParser()

parser.add_argument('name')
parser.add_argument('type')
parser.add_argument('date')
parser.add_argument('source')
parser.add_argument('destination')
parser.add_argument('description')

class TransApi(Resource):

    @auth_required('token')
    @roles_accepted('user','admin')
    def get(self):
        transaction = []
        trans_json = []
        if "admin" in roles_list(current_user.roles):
            transaction = Transaction.query.all()
        else:
            transaction = current_user.trans
        for trans in transaction:
            trans_json.append({
                "id": trans.id,
                "name": trans.name,
                "type": trans.type,
                "date": trans.date,
                "delivery": trans.delivery,
                "source": trans.source,
                "destination": trans.destination,
                "internal_status": trans.internal_status,
                "delivery_status": trans.delivery_status,
                "description": trans.description,
                "amount": trans.amount,
                "user": trans.bearer.username
            })
        if trans_json:
            return trans_json

        return {
            "message": "No transactions found"
        }, 404

    @auth_required('token')
    @roles_required('user')
    def post(self):
        args = parser.parse_args()
        try:
            transaction = Transaction(name = args["name"],
                                    type = args["type"],
                                    date = args["date"],
                                    source = args["source"],
                                    destination = args["destination"],
                                    description = args["description"],
                                    user_id = current_user.id)
            db.session.add(transaction)
            db.session.commit()
            return {
                "message": "Transaction created successfully"
            }
        except:
            return {
                "message": "One or more required fields are missing"
            }, 400

    @auth_required('token')
    @roles_required('user')
    def put(self,trans_id):
        args = parser.parse_args()
        try:
            transaction = Transaction.query.get(trans_id)
            transaction.name = args["name"]
            transaction.type = args["type"]
            transaction.date = args["date"]
            transaction.source = args["source"]
            transaction.destination = args["destination"]
            transaction.description = args["description"]
            db.session.commit()
            return {
                "message": "Transaction updated successfully"
            }
        except:
            return {
                "message": "One or more required fields are missing"
            }, 400
        
    @auth_required('token')
    @roles_required('user')
    def delete(self,trans_id):
        transaction = Transaction.query.get(trans_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
            return {
                "message": "Transaction deleted successfully"
            }
        else:
            return {
                "message": "Transaction not found"
            }, 404
api.add_resource(TransApi, '/api/get','/api/create','/api/update/<int:trans_id>','/api/delete/<int:trans_id>')