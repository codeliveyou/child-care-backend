from flask import Blueprint, request, jsonify
from src.modules.company.company_service import CompanyService
from src.modules.company.company_dtos import CreateCompanyBody, UpdateCompanyBody, FilterCompanyByAdminEmail
from pydantic import ValidationError
from src.modules.user.user_service import UserService

company_controller = Blueprint('companys', __name__)

@company_controller.route('/', methods=['POST'])
def create_company():
    try:
        data = request.get_json()
        body = CreateCompanyBody(**data)
        company_id = CompanyService.create(body)
        return jsonify({"_id": company_id}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

# New endpoint for filtering by company_admin_email
@company_controller.route('/filter-by-admin-email', methods=['POST'])
def get_companies_by_admin_email():
    try:
        data = request.get_json()
        body = FilterCompanyByAdminEmail(**data)

        # Fetch companies by admin email
        companies = CompanyService.get_by_admin_email(body.company_admin_email)

        return jsonify(companies), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@company_controller.route('/<company_id>', methods=['GET'])
def get_company(company_id):
    company = CompanyService.get_one(company_id)
    if company:
        return jsonify(company), 200
    return jsonify({"error": "Company not found"}), 404

@company_controller.route('/<company_id>', methods=['PUT'])
def update_company(company_id):
    try:
        data = request.get_json()
        body = UpdateCompanyBody(**data)
        updated_company = CompanyService.update_one(company_id, body)
        if updated_company:
            updated_company['_id'] = str(updated_company['_id'])
            return jsonify(updated_company), 200
        return jsonify({"error": "Company not found"}), 404
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@company_controller.route('/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    success = CompanyService.delete_one(company_id)
    if success:
        return jsonify({"message": "Company deleted successfully"}), 200
    return jsonify({"error": "Company not found"}), 404

@company_controller.route('/delete-all', methods=['DELETE'])
def delete_all_companies():
    CompanyService.delete_all()
    return jsonify({"message": "All companies deleted successfully"}), 200
