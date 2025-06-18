from rest_framework import serializers
from user.models import CustomUser, Agent

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'is_active']

class UserSerializer(serializers.ModelSerializer):
    agent = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        # fields = ['id', 'first_name', 'last_name']
        exclude = ['password', 'groups', 'user_permissions']

    def get_agent(self, obj):
        if obj.user_role == 'agent':
            try:
                agent = Agent.objects.get(user=obj)
                return AgentSerializer(agent).data
            except Agent.DoesNotExist:
                return None
        
        return None