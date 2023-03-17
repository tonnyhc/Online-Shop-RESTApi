from rest_framework import serializers

from OnlineShopBackEnd.products.models import Product, ProductRating, Category


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ('user', 'score')
        read_only_fields = ('user',)


class ProductSerializerOrderDetails(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('brand', 'model', 'product_price', 'discounted_price', 'slug', 'image')


class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    search = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ('ratings',)

    def get_search(self, obj):
        return str(obj.product)

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        scores = [rating.score for rating in ratings]
        if scores:
            return sum(scores) / len(scores)
        return None

    def to_representation(self, instance):
        ratings = instance.ratings.all()
        scores = [rating.score for rating in ratings]
        instance.average_rating = sum(scores) / len(scores) if scores else None
        return super().to_representation(instance)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
