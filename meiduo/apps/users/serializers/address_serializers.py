# # from rest_framework import serializers
# # from apps.users.models import Address
# #
# #
# # class AddressSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Address
# #         fields = ['id', 'title', 'receiver', 'province', 'city', 'district',
# #                   'place', 'mobile', 'tel', 'email']
# # serializers.py
# from rest_framework import serializers
# from apps.users.models import Address
#
#
# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = [
#             'id', 'title', 'receiver', 'province_id', 'city_id',
#             'district_id', 'place', 'mobile', 'tel', 'email'
#         ]
#         extra_kwargs = {
#             'province_id': {'write_only': True},
#             'city_id': {'write_only': True},
#             'district_id': {'write_only': True},
#         }