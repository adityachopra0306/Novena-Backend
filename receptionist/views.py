from django.http import JsonResponse
from django.db import connection

def fetch_staff(category):
    """Fetch staff data based on category."""
    queries = {
        "doctors": """
            SELECT d.id, d.name, d.designation, d1.name as deptname
            FROM doctor_doctor d INNER JOIN doctor_department d1 ON d.department_id=d1.id
        """,
        "nurses": """
            SELECT id, name AS name, age AS age, work_shift, experience
            FROM nurse_nurse
        """,
        "receptionists": """
            SELECT id, name, age, mobile
            FROM receptionist_receptionist
        """,
        "accountants": """
            SELECT id, name, age, working_time, mobile
            FROM accountant_accountant
        """,
    }

    query = queries.get(category.lower())
    if not query:
        return []

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    return [dict(zip(columns, row)) for row in rows]

def staff_list(request, category):
    """API endpoint to fetch staff based on category."""
    staff_data = fetch_staff(category)
    if not staff_data:
        return JsonResponse({"error": "Invalid category or no data found"}, status=404)

    return JsonResponse(staff_data, safe=False)
