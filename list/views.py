from django.shortcuts import render
from django.contrib.staticfiles import finders
from django.http import HttpRequest
import pandas as pd


from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, "")


def list_view(request: HttpRequest):
    excel_file_path = finders.find("รายชื่อต้นฉบับ.xlsx")
    if not excel_file_path:
        return render(request, "index.html", context={"data": [], "columns": []})

    df = pd.read_excel(excel_file_path, sheet_name="Sheet1")
    q = request.GET.get("q", "").strip()
    if q:
        df = df[
            df["ชื่อ"].astype(str).str.contains(q, case=False, na=False)
            | df["ทีม"].astype(str).str.contains(q, case=False, na=False)
            | df["การแข่งขัน"].astype(str).str.contains(q, case=False, na=False)
        ]
    data = df.to_dict(orient="records")
    columns = list(df.columns)[:8]
    unique_teams = len(df["ทีม"].unique())
    length = len(data)
    return render(
        request,
        "index.html",
        context={
            "data": data,
            "columns": columns,
            "length": length,
            "unique_teams": unique_teams,
        },
    )
