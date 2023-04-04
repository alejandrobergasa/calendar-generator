import datetime
import sys
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
	desc = f'\n \n \n \n \n \n Año: {year},  Mes: {meses[month]}\n \n \n \n'
	week_days_str = '    Lunes        Martes     Miércoles     Jueves       Viernes       Sábado      Domingo    \n \n'
	horiz = '+------------+------------+------------+------------+------------+------------+------------+\n'
	verti = '|            |            |            |            |            |            |            |\n'

	first_day = datetime.datetime(year, month, 1)
	first_w_day = (int(first_day.strftime('%w')) - 1)%7

	tot = 30

	if month in (1, 3, 5, 7, 8, 10, 12):
		tot = 31

	if month == 2:
		if year%4 == 0:
			tot = 29
			if year%100 == 0:
				tot = 28
				if year%400 != 0:
					tot = 29

	w = 1
	d = 1
	w_d = first_w_day
	offset = 2+12*(w_d)

	horiz_first = list(horiz)
	for i in range(0,w_d*13):
		horiz_first[i] = ' '

	calendar = desc + week_days_str + to_string(horiz_first)

	while d <= tot:
		v = list(verti)
		h = list(horiz)
		if w == 1:
			for i in range(0,w_d):
				v[13*i] = ' '
		vv = list(to_string(v))
		for w in range(w_d, 7):
			if d <= tot:
				offset = 2+13*(w)
				dd = list(str(d))
				v[offset:offset+len(dd)] = dd
				d += 1
		w_d = 0
		w += 1
		if d > tot:
			for j in range(7):
				if v[2+13*j] == ' ':
					v[13*(j+1)] = ' '
					vv[13*(j+1)] = ' '
					h[13*(j)+1:13*(j)+14] = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
		calendar += to_string(v)
		calendar += 7*(to_string(vv))
		calendar += to_string(h)

	return calendar

def add_month_to_pdf(pdf, calendar):
	pdf.add_page()
	calendar = calendar.split('\n')
	for r in calendar:
		pdf.cell(0, 0, txt=r, align='C')
		pdf.ln(3.5)

def pdf_calendar(year):
	pdf = FPDF()
	pdf.set_font('Courier', '', 8)
	for m in range(1, 13):
		add_month_to_pdf(pdf, calendar(year, m))
	pdf.output(f'calendar_{year}.pdf', 'F')
	print(f'Calendar generated: calendar_{year}.pdf')

def main():
	if len(sys.argv) == 0:
		year = int(input('Year: '))
		pdf_calendar(year)
	else:
		for i in range(1, len(sys.argv)):
			year = int(sys.argv[i])
			pdf_calendar(year)

main()
