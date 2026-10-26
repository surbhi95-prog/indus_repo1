from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hrms.models.skill import Skill
from apps.hrms.serializers.skill_serializer import (
    SkillSerializer
)


class SkillListCreateView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        queryset = Skill.objects.filter(
            is_active=True
        ).order_by("name")

        serializer = SkillSerializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

    def post(self, request):

        serializer = SkillSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        skill = serializer.save()

        return Response(
            {
                "success": True,
                "message": "Skill created successfully.",
                "data": SkillSerializer(skill).data
            },
            status=status.HTTP_201_CREATED
        )


class SkillDetailView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self, skill_id):

        return Skill.objects.get(
            id=skill_id
        )

    def get(self, request, skill_id):

        try:

            skill = self.get_object(skill_id)

        except Skill.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Skill not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "success": True,
            "data": SkillSerializer(skill).data
        })

    def put(self, request, skill_id):

        try:

            skill = self.get_object(skill_id)

        except Skill.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Skill not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SkillSerializer(
            skill,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response({
            "success": True,
            "message": "Skill updated successfully.",
            "data": serializer.data
        })

    def delete(self, request, skill_id):

        try:

            skill = self.get_object(skill_id)

        except Skill.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Skill not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        skill.is_active = False
        skill.save(update_fields=["is_active"])

        return Response({
            "success": True,
            "message": "Skill deactivated successfully."
        })  