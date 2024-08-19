from src.modules.invoice.invoice_dtos import CreateInvoiceBody, UpdateInvoiceBody


class InvoiceService:

    @staticmethod
    def create(body: CreateInvoiceBody):
        return f"create Invoice"

    @staticmethod
    def get_one(id):
        return "get one Invoice"

    @staticmethod
    def get_all():
        return "get all invoices"

    @staticmethod
    def update_one(id, body: UpdateInvoiceBody):
        return "update one Invoice"

    @staticmethod
    def delete_one(id):
        return "delete one Invoice"

    @staticmethod
    def delete_all():
        return "delete all invoice"
