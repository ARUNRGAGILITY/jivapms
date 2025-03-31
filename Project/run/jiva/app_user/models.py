from app_web.imports.all_model_imports import *
from app_web.models import *
# Create your models here.
  
# class Role(AppWebBaseModel):
#     start_date = models.DateField(null=True, blank=True, default=None)
#     end_date = models.DateField(null=True, blank=True, default=None)

#     def __str__(self):
#         return self.title

class Profile(AppWebBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)
    test = models.BooleanField(default=False)
    # roles = models.ManyToManyField(Role,  blank=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        # Custom save logic here
        super(Profile, self).save(*args, **kwargs)  # Ensure this is called
  

class RegCode(AppWebBaseModel):
    reg_code = models.CharField(max_length=250, default='a1A1B1B2C1C3N4', null=False, blank=False)    
    def __str__(self):
        return str(self.reg_code)
    

class CustomGroup(Group):    
    active = models.BooleanField(default=True, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, related_name="custom_group_user")

    def __str__(self):
        return self.name
