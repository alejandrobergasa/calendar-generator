import datetime
from fpdf import FPDF

def to_string(l):
	s = ''
	for w in l:
		s += w
	return s

meses = {
	1: 'Enero',
	2: 'Febrero',
	3: 'Marzo',
	4: 'Abril',
	5: 'Mayo',
	6: 'Junio',
	7: 'Julio',
	8: 'Agosto',
	9: 'Septiembre',
	10: 'Octubre',
	11: 'Noviembre',
	12: 'Diciembre'
}

def calendar(year, month):
	desc = f'\n \n \n Año: {year},  Mes: {meses[month]}\n \n'
	week_days_str = '    Lunes        Martes     Miércoles     Jueves       Viernes       Sábado      Domingo    \n'
	horiz = '+------------+------------+------------+------------+------------+------------+------------+\n'
	verti = '|            |            |            |            |            |            |            |\n'

	calendar = desc + week_days_str + horiz

	first_day = datetime.datetime(year, month, 1)
	first_w_day = (int(first_day.strftime('%w')) - 1)%7

	tot = 30

	if month in (1, 3, 5, 7, 8, 10, 12):
		tot = 31

	if month == 2:
		if year%4 == 0:
			tot = 28
			if year%100 == 0:
				tot = 28
				if year%400 != 0:
					tot = 29

	w = 1
	d = 1
	w_d = first_w_day
	offset = 2+12*(w_d)

	while d <= tot:
		v = list(verti)
		for w in range(w_d, 7):
			if d <= tot:
				offset = 2+13*(w)
				dd = list(str(d))
				v[offset:offset+len(dd)] = dd
				d += 1
		w_d = 0
		calendar += to_string(v)
		calendar += 6*verti
		calendar += horiz

	return calendar

def add_month_to_pdf(pdf, calendar):
	pdf.add_page()
	calendar = calendar.split('\n')
	for r in calendar:
		pdf.cell(0, 0, txt=r, align='C')
		pdf.ln(4)

def pdf_calendar(year):
	pdf = FPDF()
	pdf.set_font('Courier', '', 8)
	for m in range(1, 13):
		add_month_to_pdf(pdf, calendar(year, m))
	pdf.output(f'calendar_{year}.pdf', 'F')

def main():
	year = int(input('Year: '))
	pdf_calendar(year)
	print(f'Calendar generated: calendar_{year}.pdf')

main()