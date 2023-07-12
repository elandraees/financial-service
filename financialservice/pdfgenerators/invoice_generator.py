from fpdf import FPDF


class PDFInvoice(FPDF):
    title = ""
    company_name = ""
    company_address = ""
    customer_details = ""
    invoice_date = ""
    invoice_number = ""
    invoice_due = ""
    invoice_lines = []

    def initialize(self, title, company_name, company_address, customer_details, invoice_date, invoice_number,
                   invoice_due, invoice_lines):
        super()
        self.add_page()
        PDFInvoice.title = title
        PDFInvoice.company_name = company_name
        PDFInvoice.company_address = company_address
        PDFInvoice.customer_details = customer_details
        PDFInvoice.invoice_date = invoice_date
        PDFInvoice.invoice_number = invoice_number
        PDFInvoice.invoice_due = invoice_due
        PDFInvoice.invoice_lines = invoice_lines

    def company_details(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        self.cell(10, 10, PDFInvoice.title)

        # Move to x position
        self.set_x(150)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, PDFInvoice.company_name, 0, 0, 'R')
        self.ln()
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 5, PDFInvoice.company_address, 0, 'R')
        self.ln()

    def customer_invoice_details(self):
        self.set_x(10)
        self.set_font('Arial', 'B', 12)
        y_before = self.get_y()
        self.cell(10, 5, "Billed To")
        self.ln()
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 5, PDFInvoice.customer_details, 0, 'L')
        y_after = self.get_y()
        self.set_y(y_before)
        self.set_x(120)
        self.set_font('Arial', 'B', 10)
        self.cell(self.get_string_width("Date Issued") + 6, 5, "Date Issued")
        self.cell(self.get_string_width("Invoice Number") + 6, 5, "Invoice Number")
        self.cell(self.get_string_width("Date Due") + 6, 5, "Date Due")
        self.ln()
        self.set_x(120)
        self.set_font('Arial', '', 9)
        self.cell(self.get_string_width("Date Issued") + 9, 5, PDFInvoice.invoice_date)
        self.cell(self.get_string_width("Invoice Number") + 10, 5, PDFInvoice.invoice_number)
        self.cell(self.get_string_width("Date Due") + 9, 5, PDFInvoice.invoice_due)
        self.set_y(y_after)
        self.ln()
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())

    def invoice_items_header(self):
        self.set_font('Arial', 'B', 10)
        self.set_x(10)
        self.cell(100, 10, "DESCRIPTION")
        self.set_x(120)
        self.cell(20, 10, "RATE")
        self.set_x(150)
        self.cell(30, 10, "QTY")
        self.set_x(183)
        self.cell(100, 10, "AMOUNT")
        self.ln()

    def add_invoice_line_item(self, description, rate, qty, amount):
        self.set_font('Arial', '', 8)
        self.set_x(10)
        y_before = self.get_y()
        self.multi_cell(100, 5, description, align='L')
        y_after = self.get_y()

        self.set_y(10) if y_before > 270 else self.set_y(y_before)

        self.set_x(120)
        self.cell(12, 5, rate, 0, 0, 'R')
        self.set_x(150)
        self.cell(10, 5, qty, 0, 0, 'C')
        self.set_x(183)
        self.cell(17, 5, amount, 0, 0, 'R')
        self.set_y(y_after)
        self.set_draw_color(163, 163, 163)
        self.set_line_width(0.01)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln()
        self.ln()

    def add_totals_section(self, sub_total, total_tax, total_amount, total_discount):
        self.set_font('Arial', '', 8)
        self.set_x(130)
        self.cell(12, 5, "SubTotal", 0, 0, 'R')
        self.set_x(183)
        self.cell(17, 5, sub_total, 0, 0, 'R')
        self.ln()
        self.set_x(130)
        self.cell(12, 5, "Discount", 0, 0, 'R')
        self.set_x(183)
        self.cell(17, 5, total_discount, 0, 0, 'R')
        self.ln()
        self.set_x(130)
        self.cell(12, 5, "Tax", 0, 0, 'R')
        self.set_x(183)
        self.cell(17, 5, total_tax, 0, 0, 'R')
        self.ln()
        self.set_draw_color(0, 0, 0)
        self.line(100, self.get_y(), 200, self.get_y())
        self.ln()
        self.set_x(130)
        self.cell(12, 5, "Total", 0, 0, 'R')
        self.set_x(183)
        self.cell(17, 5, total_amount, 0, 0, 'R')
        self.ln()
        self.set_line_width(0.5)
        self.set_draw_color(0, 0, 0)
        self.line(100, self.get_y(), 200, self.get_y())

    def add_footer1_section(self, footer1_header, footer1_details, footer2_header, footer2_details):
        self.set_y(self.get_y() + 50)
        self.set_x(10)
        self.set_font('Arial', 'B', 7)
        y_before = self.get_y()
        self.cell(50, 5, footer1_header, 0, 0)
        self.ln()
        self.set_x(10)
        self.set_font('Arial', '', 7)
        self.multi_cell(50, 5, footer1_details, 0)
        self.set_y(y_before)
        self.set_x(100)
        self.set_font('Arial', 'B', 7)
        self.cell(50, 5, footer2_header, 0, 0)
        self.ln()
        self.set_x(100)
        self.set_font('Arial', '', 7)
        self.multi_cell(50, 5, footer2_details, 0)

    def generate_invoice_from_request(self, request):
        json = request.json
        title = "INVOICE"
        company_details = json['company_details']
        company_name = company_details['company_name']
        company_address = '\n'.join(str(value) for value in company_details['company_address'].values())
        customer_details = json['customer_details']
        customer_name = customer_details['customer_name']
        customer_address = '\n'.join(str(value) for value in customer_details['customer_address'].values())
        customer_details = customer_name + '\n' + customer_address
        invoice_details = json['invoice_details']
        invoice_date = invoice_details['invoice_date']
        invoice_number = invoice_details['invoice_number']
        invoice_due = invoice_details['invoice_due_date']
        sub_total = invoice_details['sub_total']
        total_tax = invoice_details['total_tax']
        total_amount = invoice_details['total_amount']
        total_discount = invoice_details['total_discount']
        invoice_lines = invoice_details['invoice_lines']

        footer_details1 = json['footer_details1']
        footer_details1_header = footer_details1['header']
        footer_details1.pop('header', None)
        footer1 = "\n".join([f"{value}" for key, value in footer_details1.items()])

        footer_details2 = json['footer_details2']
        footer_details2_header = footer_details2['header']
        footer_details2.pop('header', None)
        footer2 = "\n".join([f"{value}" for key, value in footer_details2.items()])

        pdf = PDFInvoice()
        pdf.initialize(title, company_name, company_address, customer_details, invoice_date, invoice_number,
                       invoice_due, invoice_lines)

        pdf.header()
        pdf.company_details()
        pdf.customer_invoice_details()
        pdf.invoice_items_header()

        for line in pdf.invoice_lines:
            pdf.add_invoice_line_item(line['description'], line['rate'], line['qty'], line['amount'])

        pdf.add_totals_section(sub_total, total_tax, total_amount, total_discount)

        pdf.add_footer1_section(footer_details1_header, footer1, footer_details2_header, footer2)

        return pdf
