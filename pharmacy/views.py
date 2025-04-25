from django.http import JsonResponse
from django.db import connection

def get_prescriptions(request, patient_id):
    sort_by = request.GET.get("sort_by", "date")
    order = request.GET.get("order", "desc")

    valid_sort_columns = {"date": "p.date", "time": "p.time", "doctor_name": "d.name"}
    sort_column = valid_sort_columns.get(sort_by, "p.date")

    order_by = "DESC" if order == "desc" else "ASC"

    with connection.cursor() as cursor:
        query = f"""
            SELECT p.id, d.name AS doctor_name, p.date, p.time
            FROM pharmacy_prescription p
            JOIN doctor_doctor d ON p.doctor_id = d.id
            WHERE p.patient_id = %s
            ORDER BY {sort_column} {order_by}
        """
        cursor.execute(query, [patient_id])
        prescriptions = [
            {"id": row[0], "doctor_name": row[1], "date": row[2], "time": row[3]}
            for row in cursor.fetchall()
        ]
    return JsonResponse(prescriptions, safe=False)

def get_prescription_details(request, prescription_id):
    sort_by = request.GET.get("sort_by", "name")
    order = request.GET.get("order", "asc")

    valid_sort_columns = {
        "name": "m.name",
        "company": "m.company",
        "expiry_date": "m.expiry_date",
        "price": "m.price",
    }
    sort_column = valid_sort_columns.get(sort_by, "m.name")

    order_by = "DESC" if order == "desc" else "ASC"

    with connection.cursor() as cursor:
        query = f"""
            SELECT m.id, m.name, m.company, m.expiry_date, m.price
            FROM pharmacy_prescribedmedicines pm
            JOIN pharmacy_medicine m ON pm.medicine_id = m.id
            WHERE pm.prescription_id = %s
            ORDER BY {sort_column} {order_by}
        """
        cursor.execute(query, [prescription_id])
        medicines = [
            {"id": row[0], "name": row[1], "company": row[2], "expiry_date": row[3], "price": float(row[4])}
            for row in cursor.fetchall()
        ]
    return JsonResponse({"medicines": medicines})
