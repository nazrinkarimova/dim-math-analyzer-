import pdfplumber
import pytesseract
import re
import pandas as pd

pdf_path = "sample.pdf"

text = ""


with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        img = page.to_image(resolution=300).original
        text += pytesseract.image_to_string(img, lang='eng') + "\n"


questions = re.split(r"\n\d+\.", text)


def classify(q):
    q = q.lower()

    if any(word in q for word in ["kvadrat", "tənlik", "funksiya", "x", "y"]):
        return "Cəbr"
    elif any(word in q for word in ["radius", "dairə", "bucaq", "sm", "uzunluq"]):
        return "Həndəsə"
    elif any(word in q for word in ["ehtimal", "faiz", "%"]):
        return "Ehtimal"
    else:
        return "Digər"

results = {}

for q in questions:
    if len(q.strip()) < 10:
        continue

    section = classify(q)
    results[section] = results.get(section, 0) + 1


df = pd.DataFrame(list(results.items()), columns=["Bölmə", "Sual sayı"])


df.to_csv("report.csv", index=False)

print("Analiz tamamlandı ✅")
print(df)
