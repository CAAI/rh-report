# RH-Reports

RH-Reports is a lightweight tool for generating one-page PDF reports.

The report includes multiple modules:
- Text
- Demographics
- Tables
- Plots

To install this library
> `pip install git+https://github.com/CAAI/rh-reports.git`

## Dependencies
RH reports uses:
| Tool | Aim |
| --- | --- |
| numpy | calculation |
| matplotlib | visualisations|

## Example
```python
import requests
from io import BytesIO
from rhreports import rhreports

# Initialise report
report = rhreports()

# Define useful metrics
pagewidth = (1-report.margin[3]-report.margin[1])

# Set title and subtitle
report.set_title(ypos = (1-report.margin[0]), title = 'AIMS', subtitle = 'Multiple Sclerosis Lesion Evaluation')

# Set Demographics
report.set_demographics(pos = [report.margin[3], 0.895, pagewidth, 0.04],
    fields = {
        'Patient Name': 'John Doe',
        'Patient ID': '1234567890',
        'Sex': 'M',
        'Age': '70',
        'Study Date': '1970.01.01'
    }
)

# Logo Rigshospitalet
url = r'https://www.regionh.dk/til-fagfolk/Om-Region-H/regionens-design/logo-og-grundelementer/logo-til-print-og-web/PublishingImages/Logo_Rigshospitalet_png.png'
r = requests.get(url)
pngfile = BytesIO(r.content)

report.set_footer(
    data = {
        'left': {
            'type': 'img',
            'src': pngfile,
        },
        'center': {
            'type': 'text',
            'content': f'AIMS: v. 1.0\nReport created at: {date.today()}',
            'color': (0.6,0.6,0.6),
            'fontsize': 6,
        },
        'right' :{
            'type': 'text',
            'content' : 'Rigshospitalet\nDEPICT\nAfdeling for Klinisk Fysiologi og Nuklearmedicin\nBlegdamsvej 9, 2100 København Ø',
            'fontsize': 6,
        }
    }
)

# Store report to PDF file
report.save('rhreports.pdf')
```