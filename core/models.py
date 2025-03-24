from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL,  
        null=True,  
        blank=True  
    )

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles') 

    def __str__(self):
        return self.title
    
class GeneratedImage(models.Model):
    id = models.AutoField(primary_key=True)  
    image = models.ImageField(upload_to='generated_images/')  
    date_created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Image {self.id} créée le {self.date_created}"
