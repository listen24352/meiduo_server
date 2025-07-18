from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from datetime import date, timedelta

today = date.today()


class DailyActiveAPIView(APIView):
    """日活跃用户统计"""

    def get(self, request):
        count = User.objects.filter(last_login__gte=today).count()
        return Response({"count": count})


class DailyOrderCountAPIView(APIView):
    """用户下单统计"""

    def get(self, request):
        count = User.objects.filter(orderinfo__create_time__gte=today).count()
        return Response({'count': count})


class MonthCountAPIView(APIView):
    """月增用户趋势图"""

    def get(self, request):
        before_date = today - timedelta(days=30)
        data = []
        for i in range(30):
            start_date = before_date + timedelta(days=i)
            end_date = before_date + timedelta(days=(i + 1))
            count = User.objects.filter(date_joined__gte=start_date, date_joined__lt=end_date).count()
            data.append({
                'count': count,
                'date': start_date
            })
        return Response(data)


class TotalCountAPIView(APIView):
    """总人数"""

    def get(self, request):
        count = User.objects.all().count()
        return Response({'count': count})


class DayIncrementCountAPIView(APIView):
    """新增用户"""

    def get(self, request):
        count = User.objects.filter(date_joined__gte=today).count()
        return Response({'count': count})


class GoodsCountAPIView(APIView):
    def get(self, request):
        return Response({})
