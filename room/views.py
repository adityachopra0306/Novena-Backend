from django.http import JsonResponse
from django.db import connection
from datetime import date, datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json

def get_available_rooms(request):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id, number, room_type, cost 
                FROM room_room
                WHERE id NOT IN (
                    SELECT room_id 
                    FROM patient_admission
                    WHERE leave_date IS NULL OR leave_date >= %s
                )
            """
            cursor.execute(query, [date.today()])
            rooms = cursor.fetchall()
            room_list = [
                {"room_id": row[0], "room_no": row[1], "room_type": row[2], "room_cost": row[3]}
                for row in rooms
            ]
            return JsonResponse({"available_rooms": room_list}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def book_room(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            room_id = data.get("room_id")
            admission_date = data.get("adm_date")

            if not room_id or not admission_date:
                return JsonResponse({"error": "Missing room_id or admission_date"}, status=400)
            current_time = datetime.now().strftime('%H:%M:%S')
            admission_date_obj = datetime.strptime(admission_date, '%Y-%m-%d')
            leave_date = (admission_date_obj + timedelta(days=30)).date()

            with connection.cursor() as cursor:
                query = """
                    INSERT INTO PATIENT_ADMISSION (adm_date, leave_date, patient_id, room_id, time)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, [admission_date, leave_date, user_id, room_id, current_time])
                return JsonResponse({"message": "Room booked successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use POST."}, status=400)

def get_admission_history(request, user_id):  # Correct parameter name
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT id, adm_date, leave_date, room_id
                    FROM patient_admission
                    WHERE patient_id = %s
                    ORDER BY adm_date DESC
                """
                cursor.execute(query, [user_id])  # Use the path parameter
                admissions = cursor.fetchall()
                admission_list = [
                    {
                        "adm_id": row[0],
                        "adm_date": row[1],
                        "leave_date": row[2],
                        "room_id": row[3],
                    }
                    for row in admissions
                ]
                return JsonResponse({"admission_history": admission_list}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use GET."}, status=400)
