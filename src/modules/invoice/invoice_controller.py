from flask import Blueprint
from flask_pydantic import validate
from src.modules.invoice.invoice_service import InvoiceService
from src.modules.invoice.invoice_dtos import CreateInvoiceBody, UpdateInvoiceBody
from src.utils.responder import Responder
from flask_pydantic_docs import openapi_docs

invoice_controller = Blueprint('invoices', __name__)


@invoice_controller.post('/')
@openapi_docs()
@validate()
def create_invoice(body: CreateInvoiceBody):
    return InvoiceService.create(body)

@invoice_controller.get('/<id>')
@openapi_docs()
@validate()
def get_one_invoice(id):
    return InvoiceService.get_one(id)

@invoice_controller.get('/')
@openapi_docs()
@validate()
def get_all_invoices():
    return InvoiceService.get_all()

@invoice_controller.put('/<id>')
@openapi_docs()
@validate()
def update_one_invoice(id, body: UpdateInvoiceBody):
    return InvoiceService.update_one(id, body)

@invoice_controller.delete('/<id>')
@openapi_docs()
@validate()
def delete_one_invoice(id):
    return InvoiceService.delete_one(id)

@invoice_controller.delete('/')
@openapi_docs()
@validate()
def delete_all_invoices():
    return InvoiceService.delete_all()

