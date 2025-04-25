from django.http import JsonResponse
from django.db import connection
from django.utils.dateparse import parse_date
import json
from django.views.decorators.csrf import csrf_exempt
def get_patient_amount_owed(request, user_id):
    try:
        with connection.cursor() as cursor:
            total_billed_query = """
                SELECT COALESCE(SUM(total), 0)
                FROM accountant_bill
                WHERE pat_id = %s
            """
            cursor.execute(total_billed_query, [user_id])
            total_billed = cursor.fetchone()[0]

            total_paid_query = """
                SELECT COALESCE(SUM(total), 0)
                FROM accountant_bill ab
                JOIN accountant_payment ap ON ab.pay_id = ap.id
                WHERE ab.pat_id = %s
            """
            cursor.execute(total_paid_query, [user_id])
            total_paid = cursor.fetchone()[0]

        amount_owed = total_billed - total_paid

        return JsonResponse({
            "user_id": user_id,
            "total_billed": total_billed,
            "total_paid": total_paid,
            "amount_owed": amount_owed
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_top_5_expensive_bills(request, user_id):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id AS bill_id, purpose AS bill_purpose, total AS bill_total
                FROM accountant_bill
                WHERE pat_id = %s
                ORDER BY total DESC
                LIMIT 5;
            """
            cursor.execute(query, [user_id])
            bills = cursor.fetchall()
        
        top_bills = [
            {"bill_id": row[0], "purpose": row[1], "total": row[2]} for row in bills
        ]
        
        return JsonResponse({"user_id": user_id, "top_bills": top_bills})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def get_average_payment_per_bill(request, user_id):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT AVG(ab.total) AS average_payment
                FROM accountant_bill ab
                JOIN accountant_payment ap ON ab.pay_id = ap.id
                WHERE ab.pat_id = %s;
            """
            cursor.execute(query, [user_id])
            result = cursor.fetchone()
            average_payment = result[0] if result[0] is not None else 0
        
        return JsonResponse({"user_id": user_id, "average_payment": average_payment})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_bills_in_timeframe(request, user_id):
    try:
        data = json.loads(request.body)
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if not start_date or not end_date:
            return JsonResponse({"error": "Missing start_date or end_date"}, status=400)

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    ab.id AS bill_id, ab.purpose AS bill_purpose, ab.total AS bill_total,
                    ap.type AS payment_type, ap.date AS payment_date
                FROM accountant_bill ab
                LEFT JOIN accountant_payment ap ON ab.pay_id = ap.id
                WHERE ab.pat_id = %s
                  AND ap.date BETWEEN %s AND %s;
            """
            cursor.execute(query, [user_id, start_date, end_date])
            records = cursor.fetchall()
        
        bills = [
            {
                "bill_id": row[0],
                "purpose": row[1],
                "total": row[2],
                "payment_type": row[3],
                "payment_date": row[4].strftime("%Y-%m-%d") if row[4] else None
            }
            for row in records
        ]
        
        return JsonResponse({"user_id": user_id, "bills": bills, "start_date": str(start_date), "end_date": str(end_date)})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_payment_record(request):
    try:
        data = json.loads(request.body)
        payment_id = data.get("payment_id")

        if not payment_id:
            return JsonResponse({"error": "Missing payment_id"}, status=400)
        
        with connection.cursor() as cursor:
            check_query = """
                SELECT COUNT(*)
                FROM accountant_payment
                WHERE id = %s
            """
            cursor.execute(check_query, [payment_id])
            count = cursor.fetchone()[0]

            if count == 0:
                return JsonResponse({"error": f"No payment found with ID {payment_id}"}, status=404)

            delete_query = """
                DELETE FROM accountant_payment
                WHERE id = %s
            """
            cursor.execute(delete_query, [payment_id])

        return JsonResponse({"message": f"Payment record with ID {payment_id} has been deleted successfully."})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)