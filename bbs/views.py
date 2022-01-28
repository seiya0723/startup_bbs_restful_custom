from rest_framework.views import APIView
from django.shortcuts import render

from django.http.response import JsonResponse
from django.template.loader import render_to_string

from .models import Topic
from .serializer import TopicSerializer

class IndexView(APIView):

    def create_context(self):
        context     = {}
        context["topics"]       = Topic.objects.all()

        return context

    def get(self,request,*args,**kwargs):
        context     = self.create_context()

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):
        print("POST")

        serializer      = TopicSerializer(data=request.data)

        if serializer.is_valid():
            print("バリデーションOK")
            serializer.save()
        else:
            print("バリデーションNG")

        context                 = self.create_context()
        content_data_string     = render_to_string('bbs/comment.html', context ,request)
        json_data               = { "content" : content_data_string }

        return JsonResponse(json_data)

    def delete(self, request, *args, **kwargs):

        topic   = Topic.objects.filter(id=kwargs["pk"]).first()

        if topic:
            print("削除")
            topic.delete()

        context                 = self.create_context()
        content_data_string     = render_to_string('bbs/comment.html', context ,request)
        json_data               = { "content" : content_data_string }

        return JsonResponse(json_data)

index   = IndexView.as_view()
