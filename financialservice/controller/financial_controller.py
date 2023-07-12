from flask import Blueprint, request, send_file
from financialservice.pdfgenerators.invoice_generator import PDFInvoice
from api_reponse import get_error_response

financial_bp = Blueprint('financial', __name__)

'''
{
   "company_details" : {
        "company_name":"",
        "company_contact_number":"",
        "company_address": {
            "line1":"",
            "line2":"",
            "line3":"",
            "line4":""
        }
   },

   "customer_details": {
        "customer_name":"",
        "customer_address":{
            "line1":"",
            "line2":"",
            "line3":"",
            "line4":""
        }
   },

   "invoice_details": {
        "invoice_number":"",
        "invoice_date":"",
        "invoice_due_date":"",
        "sub_total":"",
        "total_tax":"",
        "total_amount":"",
        "total_discount":"",
        "invoice_lines":[
            {
                "description":"",
                "rate":"",
                "qty":"",
                "amount":""
            },
        ]
   },
    "footer_details1":{
        "header":"",
        "line1":"",
        "line2":"",
        "line3":"",
        "line4":""
    },
    "footer_details2":{
        "header":"",
        "line1":"",
        "line2":"",
        "line3":"",
        "line4":""
    },
}
'''


@financial_bp.route('/financial-service/create_invoice', methods=['POST'])
def create_invoice():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        pdf_output = 'invoice.pdf'
        pdf = PDFInvoice()
        try:
            pdf = pdf.generate_invoice_from_request(request)
            pdf.output(pdf_output)

            return send_file(pdf_output)

            # # Create an in-memory BytesIO object
            # pdf_stream = BytesIO()
            #
            # # Save the PDF to the BytesIO object
            # pdf.output(pdf_stream, 'S').encode('latin-1')
            #
            # # Save the PDF file to the database
            # pdf_data = pdf_stream.getvalue()
            # # pdf_file = PDFFile(file_data=pdf_data)
            # # db.session.add(pdf_file)
            # # db.session.commit()
            #
            # # Seek to the beginning of the BytesIO stream
            # pdf_stream.seek(0)
            #
            # # Send the PDF file as a response
            # response = send_file(
            #     pdf_stream,
            #     mimetype='application/pdf',
            #     as_attachment=True,
            #     download_name='invoice.pdf'
            # )
            #
            # # Close the BytesIO stream
            # pdf_stream.close()
            #
            # return response

        except Exception as e:
            return get_error_response(str(e), "")
        finally:
            pdf.close()
            #os.remove(pdf_output)

    else:
        return 'Content-Type not supported!'
