from rest_framework import serializers

from OnlineShopBackEnd.products.models import Product, ProductRating, Category, FavoriteProducts, ProductImage


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ('user', 'score')
        read_only_fields = ('user',)


class ProductSerializerOrderDetails(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('brand', 'model', 'product_price', 'discounted_price', 'slug', 'image')


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('image_url', )

    @staticmethod
    def get_image_url(obj):
        return obj.image.url

class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    search = serializers.StringRelatedField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'average_rating', 'brand', 'model', 'product_price',
                  'discounted_price', 'product_id', 'slug', 'quantity', 'image',
                  'category', 'images', 'search')
        # exclude = ('ratings',)

    @staticmethod
    def get_search(obj):
        return str(obj.product)

    @staticmethod
    def get_images(obj):
        images = obj.productimage_set.all()
        serializer = ProductImageSerializer(images, many=True)
        return serializer.data

    @staticmethod
    def get_average_rating(obj):
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


class FavoriteProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = FavoriteProducts
        fields = ('product', 'id', 'date_added', 'user')
