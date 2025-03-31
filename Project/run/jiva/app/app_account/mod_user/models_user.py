from jiva.app.app_web.imports.all_model_imports import *
from jiva.app.app_web.models import *

class Profile(AppWebBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)

    roles = models.ManyToManyField(Role,  blank=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        # Custom save logic here
        super(Profile, self).save(*args, **kwargs)  # Ensure this is called
  