from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields =('owner', ) #le decimos que el campo owner es de solo lectura
                                        #es decir, que si no lo envío en la petición no pasa nada


class PostListSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):  # el PostSerializer.Meta dice que herede la clase Meta también del
                                # PostSerializer. Si no se pone, por defecto no la hereda
        fields = ("id", "title", "url", "introduction")
