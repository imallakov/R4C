from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from .models import Robot
from django.views.decorators.csrf import csrf_exempt
import json


@method_decorator(csrf_exempt, name='dispatch')
class RobotView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            model = data.get('model')
            version = data.get('version')
            created = data.get('created')

            if not Robot.objects.filter(model=model).exists():
                return JsonResponse({"error": "Такой модели роботов не существует."}, status=400)

            serial = f"{model}-{version}"
            robot = Robot(serial=serial, model=model, version=version, created=created)
            robot.save()

            return JsonResponse({"serial": robot.serial, "model": robot.model, "version": robot.version}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный формат JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
