from rest_framework import serializers

from OnlineShopBackEnd.products.models import Product, ProductRating


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ('user', 'score')
        read_only_fields = ('user',)

class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('ratings', )

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        scores = [rating.score for rating in ratings]
        if scores:
            return sum(scores) / len(scores)
        return None

    def to_representation(self, instance):
        print('5')
        ratings = instance.ratings.all()
        scores = [rating.score for rating in ratings]
        instance.average_rating = sum(scores) / len(scores) if scores else None
        return super().to_representation(instance)






