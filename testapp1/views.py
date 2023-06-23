'''
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
'''
from urllib import response
from testapp1.models import Submissions,Recruiter, Consultant
from testapp1.api.serializers import Submissions_Serializer, RecruiterSerializer, ConsultantSerializer
from rest_framework import mixins, generics
from django.contrib.auth.models import User
from rest_framework import permissions,renderers,status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.shortcuts import redirect
from django.views.generic import FormView
from .forms import SignupForm
from .permissions import IsOwnerOrReadOnly
from testapp1.api.serializers import Submissions_Serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
# Create your views here.



class SubmissionHighlight(generics.GenericAPIView):
    queryset = Submissions.objects.all()
    renderer_class = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        submission = self.get_object()
        serializer = Submissions_Serializer(submission,context={'request': request})
        return Response(serializer.data)







        '''
        return Response({
        'recruiters': reverse('recruiter-list', request=request, format=format),
        'submissions': reverse('submissions-list', request=request, format=format)
        })
        '''

class api_root(View):
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def success_view(request):
    return redirect('signup')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate against R_UserName and password fields
        user = authenticate(request, R_UserName=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
        else:
            return render(request, self.template_name, {'error': 'Invalid credentials'})
        '''
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
        else:
            return render(request, self.template_name, {'error': 'Invalid credentials'})
        '''
class logout_view(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        '''
        user = User.objects.create_user(
             username=form.cleaned_data['recruiter_username'],
             password=form.cleaned_data['password'])
        recruiter = Recruiter(
            R_Name=form.cleaned_data['recruiter_name'],
            R_UserName=form.cleaned_data['recruiter_username'],
            R_Password=form.cleaned_data['password'])
        recruiter.save()
        '''
        form.save()
        return super().form_valid(form)


class RecruiterListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer

class RecruiterDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer


class SubmissionsByRecruiterView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    serializer_class = Submissions_Serializer

    def get_queryset(self):
        recruiter_UserName = self.kwargs['R_UserName']
        recruiter_ = Recruiter.objects.get(R_UserName=recruiter_UserName)
        return Submissions.objects.filter(S_RecruiterId=recruiter_.R_Id)

        
    
        


class submissions_list(generics.ListCreateAPIView):
    #authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    #serializer_class = Submissions_Serializer
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'submissions_list.html'
    
    def get(self, request, *args, **kwargs):
        queryset = Submissions.objects.all()
        recruiters = []
        serialized_recruiters = ""

        if request.user.is_authenticated:
            # Get the logged-in recruiter
            recruiter = get_object_or_404(Recruiter, R_UserName=request.user.R_UserName)
            serializer = RecruiterSerializer(recruiter, context={'request': request})
            recruiters = [serializer.data]  # Add this line to store the recruiters as a list of dictionaries
            serialized_recruiters = json.dumps(recruiters)

        # Get all consultants
        consultants = Consultant.objects.all()
        serialized_consultants = ConsultantSerializer(consultants, many = True,context={'request': request})
        serialized_consultants = serialized_consultants.data
        serialized_consultants = json.dumps(serialized_consultants)
        # Create a dictionary to pass to the template context
        return Response({'submissions': queryset, 'recruiters': recruiters, 'consultants': consultants, 'json_recruiters': serialized_recruiters, 'json_consultants': serialized_consultants})

    def perform_create(self, serializer):
        # Get the logged-in recruiter
        recruiter = get_object_or_404(Recruiter, R_UserName=self.request.user.R_UserName)
        
        # Assign the recruiter to the submission
        serializer.save(S_RecruiterId=recruiter.R_Id)

    def post(self, request, *args, **kwargs):
        print("Inside the get method of submissions_list view")
        # Get the logged-in recruiter
        recruiter = get_object_or_404(Recruiter, R_UserName=request.user.R_UserName)
        # Get all consultants
        consultants = Consultant.objects.all()
        # Create a dictionary to pass to the template context
        context = {
            'recruiters': [recruiter],
            'consultants': consultants,
            'test_variable': 'Test Value'
        }
        submission = Submissions()
        submission.S_RecruiterId = recruiter
        submission.S_ConsultantId = get_object_or_404(Consultant, C_Id=request.data['consultant'])
        submission.S_ConsultantJobTitle = request.data['consultant_job_title']
        submission.S_ImplementationPartner = request.data['implementation_partner']
        submission.S_EndClient = request.data['end_client']
        submission.S_EndClientLocation = request.data['end_client_location']
        submission.S_ImplementationPartner_Name = request.data['implementation_partner_name']
        submission.S_ImplementationPartner_Contact = request.data['implementation_partner_contact']
        # Set other fields as needed
        submission.save()
        #return render(request, self.template_name, context=context)
        return redirect('submissions-list')
        '''
        submissions_serializer = Submissions_Serializer(data = request.data, context = context)
        if submissions_serializer.is_valid():
            submissions_serializer.save()
            return redirect('submissions-list')
        else:
            return Response(submissions_serializer.erros, status =status.HTTP_400_BAD_REQUEST)
        '''

class submissions_detail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    #renderer_classes = [renderers.TemplateHTMLRenderer]
    #template_name = 'submissions_detail.html'
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    #queryset = Submissions.objects.get(id = pk)
    serializer_class = Submissions_Serializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Submissions, pk = pk)

'''
@api_view(['GET', 'POST'])
def submissions_list(request, format = None):
    
    
    #List all Submissions or create a new submission
    

    if request.method == 'GET':
        submissions = Submissions.objects.all()
        serializer = Submissions_Serializer(submissions, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Submissions_Serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def submissions_detail(request,pk, format = None):
    '
     #Retrieve, update or delete a submission
    

    try:
        submission = Submissions.objects.get(pk = pk)
    except Submissions.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Submissions_Serializer(submission)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Submissions_Serializer(submission, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        submission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
