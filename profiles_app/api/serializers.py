from rest_framework import serializers

from profiles_app.models import Profile


class BaseProfileSerializer(serializers.ModelSerializer):
    """Base serializer exposing username and user type."""

    username = serializers.CharField(source="user.username")
    type = serializers.CharField(source="user.type")

    class Meta:
        abstract = True


class ProfileDetailSerializer(BaseProfileSerializer):
    """Serialize full profile detail including contact and account fields."""

    username = serializers.CharField(source="user.username")
    type = serializers.CharField(source="user.type")
    email = serializers.EmailField(source="user.email")
    created_at = serializers.DateTimeField(source="user.created_at", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]

    def update(self, instance, validated_data):
        """Update profile and nested user fields from validated data."""

        user_data = validated_data.pop("user", {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProfileListSerializer(BaseProfileSerializer):
    """Serialize profile for list views with minimal fields."""

    username = serializers.CharField(source="user.username")
    type = serializers.CharField(source="user.type")

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]


class ProfileDetailSerializer(BaseProfileSerializer):

    username = serializers.CharField(source='user.username')
    type = serializers.CharField(source='user.type')
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(source='user.created_at', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 
                  'file', 'location','tel', 'description','working_hours', 'type', 'email', 'created_at'
                  ]
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class ProfileListSerializer(BaseProfileSerializer):

    username = serializers.CharField(source='user.username')
    type = serializers.CharField(source='user.type')

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 
                  'file', 'location','tel', 'description','working_hours', 'type'
                  ]  