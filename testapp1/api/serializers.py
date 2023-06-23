from dataclasses import fields
from rest_framework import serializers
from testapp1.models import Consultant, Recruiter, Submissions
from django.contrib.auth.models import User



class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = ['C_Id', 'C_Name', 'C_Email', 'C_Number', 'C_Dob', 'C_Yoe', 'C_JobTitles']

class RecruiterSerializer(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(many=True, view_name='recruiter-list', read_only=True)
    class Meta:
        model = Recruiter
        fields = '__all__'

class Submissions_Serializer(serializers.HyperlinkedModelSerializer):
    #id = serializers.IntegerField(read_only = True)
    S_DOS = serializers.DateField(format='%Y-%m-%d')
    #S_RecruiterId = serializers.PrimaryKeyRelatedField(queryset=Recruiter.objects.all())
    #S_RecruiterId = serializers.PrimaryKeyRelatedField(queryset=Recruiter.objects.all())
    S_RecruiterId = serializers.PrimaryKeyRelatedField(queryset=Recruiter.objects.all(),required = True)
    S_ConsultantId = serializers.PrimaryKeyRelatedField(queryset=Consultant.objects.all(),required = True)
    #S_RecruiterId = serializers.SerializerMethodField()
    S_ConsultantJobTitle = serializers.CharField(required = True)
    S_ImplementationPartner = serializers.CharField(required = True)
    S_EndClient = serializers.CharField(required = True)
    S_EndClientLocation = serializers.CharField(required = True)
    S_ImplementationPartner_Name = serializers.CharField(required = True)
    S_ImplementationPartner_Contact = serializers.IntegerField()
    url = serializers.HyperlinkedIdentityField(view_name='submission-highlight', format='html')


    class Meta:
        model = Submissions
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['S_RecruiterId'] = instance.S_RecruiterId.R_Name
        rep['S_ConsultantId'] = instance.S_ConsultantId.C_Name
        return rep
    '''
    def get_S_RecruiterId(self, obj):
        recruiter = obj.S_RecruiterId
        if recruiter:
            return recruiter.R_Name
        return None

    def get_S_ConsultantId(self, obj):
        consultant = obj.S_ConsultantId
        if consultant:
            return consultant.C_Id
        return None
    '''

    def create(self, validated_data):
        '''
        Create and return a new Submissions instance, given the validated data
        '''
        return Submissions.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''
        Update and return an existing submissions instance, given the validated data
        '''
        instance.S_DOS = validated_data.get('S_DOS', instance.S_DOS)
        instance.S_RecruiterId = validated_data.get('S_RecruiterId', instance.S_RecruiterId)
        instance.S_ConsultantId = validated_data.get('S_ConsultantId', instance.S_ConsultantId)
        instance.S_ConsultantJobTitle = validated_data.get('S_ConsultantJobTitle', instance.S_ConsultantJobTitle)
        instance.S_ImplementationPartner = validated_data.get('S_ImplementationPartner', instance.S_ImplementationPartner)
        instance.S_EndClient = validated_data.get('S_EndClient', instance.S_EndClient)
        instance.S_EndClientLocation = validated_data.get('S_EndClientLocation', instance.S_EndClientLocation)
        instance.S_ImplementationPartner_Name = validated_data.get('S_ImplementationPartner_Name', instance.S_ImplementationPartner_Name)
        instance.S_ImplementationPartner_Contact = validated_data.get('S_ImplementationPartner_Contact', instance.S_ImplementationPartner_Contact)
        print(instance)
        instance.save()
        return instance

